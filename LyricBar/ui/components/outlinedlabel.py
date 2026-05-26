import math
import os
import random

from PyQt5.QtCore import (
    QByteArray,
    QFile,
    QMutex,
    QRect,
    QSize,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QFont,
    QFontDatabase,
    QFontMetrics,
    QPainter,
    QPen,
    QPixmap,
    QRegion,
)
from PyQt5.QtWidgets import QLabel

from .text import getTextPathRich, strip_tags

FONT_DB = QFontDatabase
FONT_DICT = {}

get_path_lock = QMutex()


class OutlinedLabel(QLabel):
    update_signal = pyqtSignal()

    def __init__(
        self,
        text=None,
        relative_outline=True,
        linewidth=1 / 25,
        brushcolor=QColor(255, 255, 255),
        linecolor=QColor(0, 0, 0),
        parent=None,
        **kwargs
    ):
        super().__init__(text=text, parent=parent, **kwargs)
        self.w = linewidth
        self.mode = relative_outline
        self.flip = False
        self._opacity = 1
        self._scale = 1
        self._x_pos = 0
        self._y_pos = 0

        self._font_size = 1
        self._offset = -1
        self.update_signal.connect(self.update)

        self.path = None
        self.path_offset = None
        self.qmap = None
        self.frame_counter = 0

        self.path_mutex = QMutex()
        self.qmap_mutex = QMutex()

        self._text = None

        self._indent = None

        self.right_pad = False
        self.use_scale = True

        self.blinds_enabled = False
        self._blinds_progress = 1.0

        self.blinds_slats = 14
        self.blinds_seed = 20251217
        self.blinds_min_ratio = 0.02  # 每片最小占比（2%），避免极薄
        self.blinds_gap_px = 0  # 缝隙还是用像素更直观
        self._blinds_ratios = None  # list[float], sum=1

        self.setBrush(brushcolor)
        self.setPen(linecolor)

        # global FONT_DB
        # if not FONT_DB:
        #     FONT_DB = QFontDatabase

    def setLineWidth(self, width):
        self.w = width

    def setText(self, text):
        super().setText(text)
        self._text = text
        if self.blinds_enabled:
            self._prepare_blinds_ratios()
        self.updatePath()

    def setTextRich(self, text):
        super().setText(strip_tags(text))
        self._text = text
        if self.blinds_enabled:
            self._prepare_blinds_ratios()
        self.updatePath()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        # if value < 1:
        #     self.frame_counter += 1
        # else:
        #     logging.info("Frame Counter: ", self.frame_counter)
        #     self.frame_counter = 0
        # logging.info("opacity: ", value)
        self._opacity = value
        self.update()

    @pyqtProperty(int)
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, value):
        self._x_pos = value
        self.update()

    @pyqtProperty(int)
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, value):
        self._y_pos = value
        self.update()

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    @pyqtProperty(float)
    def blinds_progress(self):
        return self._blinds_progress

    @blinds_progress.setter
    def blinds_progress(self, v):
        self._blinds_progress = max(0.0, min(1.0, float(v)))
        self.update()

    def _prepare_blinds_ratios(self):
        n = max(1, int(self.blinds_slats))
        rmin = float(self.blinds_min_ratio)
        # 保证可行：n * rmin <= 1
        rmin = min(rmin, 1.0 / n)

        rng = random.Random(int(self.blinds_seed))

        # 先给每片 rmin，剩下的按随机权重分配（Dirichlet-ish）
        rem = 1.0 - n * rmin
        weights = [rng.random() + 1e-12 for _ in range(n)]
        s = sum(weights)
        extras = [rem * w / s for w in weights]

        ratios = [rmin + e for e in extras]
        # 浮点误差兜底
        ratios[-1] += 1.0 - sum(ratios)

        self._blinds_ratios = ratios

    def _ratios_to_pixel_heights(self, total_h: int):
        ratios = self._blinds_ratios
        if not ratios:
            return None

        n = len(ratios)
        gap = int(self.blinds_gap_px)
        usable = max(1, int(total_h) - gap * (n - 1))

        raw = [r * usable for r in ratios]
        hs = [int(x) for x in raw]

        # 把舍入误差补齐到 usable（按小数部分从大到小分配像素）
        diff = usable - sum(hs)
        if diff != 0:
            frac = [raw[i] - hs[i] for i in range(n)]
            order = sorted(range(n), key=lambda i: frac[i], reverse=(diff > 0))
            step = 1 if diff > 0 else -1
            for k in range(abs(diff)):
                hs[order[k % n]] += step

        return hs

    def _make_blinds_region(self, draw_rect: QRect) -> QRegion:
        p = max(0.0, min(1.0, self._blinds_progress))
        w_open = int(draw_rect.width() * p)

        hs = self._ratios_to_pixel_heights(draw_rect.height())
        if not hs:
            return QRegion(draw_rect)

        gap = int(self.blinds_gap_px)
        r = QRegion()
        y = draw_rect.top()
        for i, h in enumerate(hs):
            r |= QRegion(draw_rect.left(), y, w_open, int(h))
            y += int(h)
            if gap and i != len(hs) - 1:
                y += gap
        return r

    @pyqtProperty(int)
    def font_size(self):
        return self.font().pixelSize()

    @font_size.setter
    def font_size(self, value):
        if value < 0:
            return
        f = self.font()
        f.setPixelSize(value)
        self.setFont(f)
        self.updatePath()
        # self.update_signal.emit()

    @pyqtProperty(object)
    def font_family(self):
        return self.font().family()

    @font_family.setter
    def font_family(self, value):
        f = QFont("Times New Roman")
        # if len(QFontDatabase.families()) != 0:
        #     QFontDatabase.removeAllApplicationFonts()
        # families = self.font_db.families()

        # for family in families:
        #     logging.info(family)

        if not any([_ in value.lower() for _ in [".ttf", ".otf", ".ttc"]]):
            f.setFamily(value)
        else:
            value = os.path.abspath(value)
            if value in FONT_DICT:
                # logging.info("font already loaded")
                id = FONT_DICT[value]
                fam = FONT_DB.applicationFontFamilies(id)[0]
                f.setFamily(fam)
            else:
                # logging.info("loading font")
                for i in range(10):
                    fontfile = QFile(value)
                    fontfile.open(QFile.OpenModeFlag.ReadOnly)
                    fontdata = QByteArray(fontfile.readAll())
                    id = FONT_DB.addApplicationFontFromData(fontdata)
                    if id != -1:
                        FONT_DICT[value] = id
                        break
                if id == -1:
                    # logging.info("failed to load font")
                    pass
                if id != -1:
                    fam = FONT_DB.applicationFontFamilies(id)[0]
                    f.setFamily(fam)
        f.setWeight(self.font().weight())
        f.setItalic(self.font().italic())
        f.setPixelSize(self.font().pixelSize())
        self.font().cleanup()
        self.setFont(f)
        self.updatePath()

    @pyqtProperty(int)
    def font_weight(self):
        return self.font().weight()

    @font_weight.setter
    def font_weight(self, value):
        f = self.font()
        f.setWeight(QFont.Weight(value))
        self.setFont(f)
        self.updatePath()

    @pyqtProperty(bool)
    def font_italic(self):
        return self.font().italic()

    @font_italic.setter
    def font_italic(self, value):
        f = self.font()
        f.setItalic(value)
        self.setFont(f)
        self.updatePath()

    def scaledOutlineMode(self):
        return self.mode

    def setScaledOutlineMode(self, state):
        self.mode = state
        self.updatePath()

    def outlineThickness(self):
        return self.w * self.font().pointSize() if self.mode else self.w

    def setOutlineThickness(self, value):
        self.w = value
        self.updatePath()

    def setBrush(self, brush):
        if not isinstance(brush, QBrush):
            brush = QBrush(brush)
        self.brush = brush
        self.updatePixmap()

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            pen = QPen(pen)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.pen = pen
        self.updatePixmap()

    def setFontSize(self, size):
        self.font_size = size

    def setFontFamily(self, family):
        self.font_family = family

    def setFontWeight(self, weight):
        if weight == "light":
            self.font_weight = 25
        elif weight == "normal":
            self.font_weight = 50
        elif weight == "demibold":
            self.font_weight = 63
        elif weight == "bold":
            self.font_weight = 75
        elif weight == "black":
            self.font_weight = 87
        else:
            self.font_weight = weight

    def setFontItalic(self, italic):
        self.font_italic = italic

    def sizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().sizeHint() + QSize(w, w)

    def minimumSizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().minimumSizeHint() + QSize(w, w)

    def updatePath(self):
        if self._text is None or self._text == "" or self.font() is None:
            return
        if not self.path_mutex.tryLock():
            return

        # ---- rich-aware getTextPathRich ----
        ret = getTextPathRich(self.font(), self._text, self.alignment())
        if isinstance(ret, tuple) and len(ret) == 2:
            self.path, self._rich_layout = ret
        else:
            self.path = ret
            self._rich_layout = None

        if self.path is None:
            self.path_mutex.unlock()
            return

        self.path.setFillRule(Qt.FillRule.WindingFill)

        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())

        # indent init (same as your original)
        if self.indent() == -1:
            if self.frameWidth():
                self._indent = [(metrics.boundingRect("x").width() + w * 2) / 2] * 4
            else:
                self._indent = [w] * 4
        else:
            self._indent = [self.indent()] * 4

        # bearing compensation (same as your original)
        longest = max([_ for _ in self.text().split("\n")], key=len)
        try:
            self._indent[1] -= min(metrics.leftBearing(longest[0]), -2)
        except:
            self._indent[1] += 2
        try:
            self._indent[3] -= min(metrics.rightBearing(longest[-1]), -2)
        except:
            self._indent[3] += 2

        # place path (same as your original)
        x = rect.left()
        y = max(metrics.ascent(), -self.path.boundingRect().top())
        self.path.translate(x, y)

        self._indent[0] += 0

        # ---- FIX: use rich layout height if available ----
        if getattr(self, "_rich_layout", None) is not None:
            expected_h = self._rich_layout.get("height", None)
        else:
            expected_h = None

        if expected_h is None:
            expected_h = metrics.height() * len(self.text().split("\n"))

        self._indent[2] += max(expected_h - self.path.boundingRect().bottom(), 0)

        # keep your right_pad logic (optionally use rich width)
        if self.right_pad:
            if getattr(self, "_rich_layout", None) is not None:
                bw = self._rich_layout.get("width", self.path.boundingRect().width())
            else:
                bw = self.path.boundingRect().width()
            self._indent[3] += max(bw - 500, 0)

        self.path_mutex.unlock()
        self.updatePixmap()

    def updatePixmap(self):
        if not self.qmap_mutex.tryLock():
            return
        if not self.path_mutex.tryLock():
            self.qmap_mutex.unlock()
            return
        if self.path is None:
            self.path_mutex.unlock()
            self.qmap_mutex.unlock()
            return

        # self.qmap = QPixmap(self.size())
        # self.qmap.fill(Qt.GlobalColor.transparent)
        # qp = QPainter(self.qmap)

        # w = self.outlineThickness()
        # tr = self.path.boundingRect().adjusted(0, 0, int(w), int(w))
        # top = self.path.boundingRect().top()

        # logging.info(self._indent)

        w = self.outlineThickness()
        # logging.info("box size", int(self.path.boundingRect().right() + self._indent[1] + self._indent[3]), int(self.path.boundingRect().bottom() + self._indent[0] + self._indent[2]))
        self.qmap = QPixmap(
            int(self.path.boundingRect().right() + self._indent[1] + self._indent[3]),
            int(self.path.boundingRect().bottom() + self._indent[0] + self._indent[2]),
        )
        self.qmap.fill(Qt.GlobalColor.transparent)
        qp = QPainter(self.qmap)
        qp.translate(self._indent[1], self._indent[0])

        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.outlineThickness() > 0:
            self.pen.setWidthF(w * 2)
            qp.strokePath(self.path, self.pen)
        qp.fillPath(self.path, self.brush)
        qp.end()

        if (
            self.qmap.width() > self.width() or self.qmap.height() > self.height()
        ) and self.use_scale:  # or self.qmap.height() > self.height():
            scale = min(
                self.width() / self.qmap.width(), self.height() / self.qmap.height()
            )
            self.qmap = self.qmap.scaled(
                int(self.qmap.width() * scale),
                int(self.qmap.height() * scale),
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation,
            )

        self.path_mutex.unlock()
        self.qmap_mutex.unlock()

        self.update()

    def paintEvent(self, event):
        if not self.qmap_mutex.tryLock():
            return
        if self.qmap is None:
            self.qmap_mutex.unlock()
            return
        qp = QPainter(self)
        qp.setRenderHints(
            QPainter.RenderHint.Antialiasing
        )  # | QPainter.RenderHint.SmoothPixmapTransform)
        # qp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        qmap = self.qmap

        scale = self.scale
        # qp.scale(scale, scale)
        if scale != 1:
            qmap = qmap.scaled(
                int(qmap.width() * scale),
                int(qmap.height() * scale),
                transformMode=Qt.SmoothTransformation,
            )
        if self.flip:
            qp.scale(-1, 1)
            qp.translate(-self.width(), 0)
        qp.setOpacity(self.opacity)

        x, y = 0, 0
        if self.alignment() & Qt.AlignmentFlag.AlignLeft:
            x = 0
        elif self.alignment() & Qt.AlignmentFlag.AlignRight:
            x = self.width() - qmap.width()
        else:
            x = (self.width() - qmap.width()) / 2

        if self.alignment() & Qt.AlignmentFlag.AlignTop:
            y = 0
        elif self.alignment() & Qt.AlignmentFlag.AlignBottom:
            y = self.height() - qmap.height()
        else:
            y = (self.height() - qmap.height()) // 2

        if self.blinds_enabled:
            self._draw_blinds_pixmap(qp, x + self.x_pos, y + self.y_pos, qmap)
        else:
            qp.drawPixmap(int(x + self.x_pos), int(y + self.y_pos), qmap)
        qp.end()
        self.qmap_mutex.unlock()

    def _draw_blinds_pixmap(self, qp, x, y, qmap):
        # qmap 的“逻辑尺寸”（和 painter 坐标一致）
        dpr = qmap.devicePixelRatioF()
        if not dpr or dpr <= 0:
            dpr = 1.0

        w = qmap.width() / dpr
        h = qmap.height() / dpr

        # progress 控制打开宽度
        p = max(0.0, min(1.0, float(self._blinds_progress)))
        w_open = int(w * p)

        ratios = getattr(self, "_blinds_ratios", None)
        if not ratios:
            qp.drawPixmap(int(x), int(y), qmap)
            return

        gap = int(getattr(self, "blinds_gap_px", 0))
        n = len(ratios)

        # 把占比 -> 像素高度（在逻辑坐标系下）
        usable_h = max(1, int(h) - gap * (n - 1))
        raw = [r * usable_h for r in ratios]
        hs = [int(v) for v in raw]
        diff = usable_h - sum(hs)
        if diff != 0:
            frac = [raw[i] - hs[i] for i in range(n)]
            order = sorted(range(n), key=lambda i: frac[i], reverse=(diff > 0))
            step = 1 if diff > 0 else -1
            for k in range(abs(diff)):
                hs[order[k % n]] += step

        # 分片绘制：destRect 是窗口逻辑坐标；sourceRect 是 pixmap 的逻辑坐标
        yy = int(y)
        sy = 0
        for i, hh in enumerate(hs):
            if hh <= 0:
                continue

            dest = QRect(int(x), yy, w_open, hh)
            src = QRect(0, sy, w_open, hh)

            qp.drawPixmap(dest, qmap, src)

            yy += hh
            sy += hh
            if gap and i != n - 1:
                yy += gap
                sy += gap


if __name__ == "__main__":

    import sys

    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("OutlinedLabel Test")
    window.setGeometry(50, 50, 400, 100)

    container = QWidget()
    layout = QVBoxLayout()

    label = OutlinedLabel(
        text="Hello World",
        relative_outline=False,
        linewidth=5,
        brushcolor=QColor(255, 255, 255),
        linecolor=QColor(255, 0, 0),
    )

    label.setFontSize(120)
    label.setLineWidth(2)
    label.setFontFamily("Arial")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(label)
    container.setLayout(layout)
    window.setCentralWidget(container)
    window.show()

    # label.setTextRich("yyy<strike>Strikethrough</strike>")
    label.setTextRich(
        "<small>Small text</small> and\n<big>big text</big>\n<small>Small text</small> and\n<size=0.3>简单的中文翻译</size>"
    )

    sys.exit(app.exec_())
