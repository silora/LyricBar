from datetime import datetime

from PyQt5.QtCore import QAbstractAnimation, QPropertyAnimation, Qt, pyqtProperty
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QLabel

from LyricBar.ui.components.outlinedlabel import OutlinedLabel
from LyricBar.ui.components.pad import Pad
from LyricBar.ui.components.progressbar import ProgressBar
from LyricBar.ui.components.utils import convert_to_color


class LyricAnimation(QAbstractAnimation):
    def __init__(
        self,
        target,
        duration,
        parent=None,
        entering=None,
        sustaining=None,
        leaving=None,
    ):
        super().__init__(parent)
        self.target = target
        self._duration = -1
        self.setDuration(duration if duration is not None else -1)
        self.entering = self.get_interpolation_function(entering)
        self.sustaining = self.get_interpolation_function(sustaining)
        self.leaving = self.get_interpolation_function(leaving)

        self.entering_time = 150
        self.leaving_time = 150
        self.sustaining_time = 3000

        self.last_frame_type = None

    def setAnimation(self, **kwargs):
        if "entering" in kwargs:
            self.entering = self.get_interpolation_function(kwargs["entering"])
        if "sustaining" in kwargs:
            self.sustaining = self.get_interpolation_function(kwargs["sustaining"])
        if "leaving" in kwargs:
            self.leaving = self.get_interpolation_function(kwargs["leaving"])

    def start(self, direction=1):
        self.currentTime = 0
        self.direction = direction
        self.target.applyValues(reset=True)
        super().start()

    def get_interpolation_function(self, props):
        if props is None:
            return lambda x: {}

        def get_stage_value(perc):
            ret = {}
            for property_name, points in props:
                points = sorted(points)
                if perc == 0:
                    ret[property_name] = (
                        points[0][1]
                        if points[0][1] is not None
                        else self.target.__getattribute__(property_name)
                    )
                for i in range(len(points)):
                    if perc > points[i][0] and perc <= points[i + 1][0]:
                        left_v = (
                            points[i][1]
                            if points[i][1] is not None
                            else self.target.__getattribute__(property_name)
                        )
                        right_v = (
                            points[i + 1][1]
                            if points[i + 1][1] is not None
                            else self.target.__getattribute__(property_name)
                        )
                        weight = (perc - points[i][0]) / (
                            points[i + 1][0] - points[i][0]
                        )
                        ret[property_name] = weight * right_v + (1 - weight) * left_v
            return ret

        return get_stage_value

    def get_value(self, time):
        if self.duration() < 0:
            entering_time = self.entering_time
            if self.entering is not None:
                if time <= self.entering_time:
                    # logging.info("ENTERING", time / self.entering_time)
                    self.last_frame_type = "entering"
                    return self.entering(time / self.entering_time)
                else:
                    entering_time = 0
            if self.sustaining is not None:
                # logging.info("SUSTAINING")
                if self.last_frame_type != "sustaining":
                    self.target.applyValues(reset=True)
                self.last_frame_type = "sustaining"
                return self.sustaining(
                    ((time - entering_time) % self.sustaining_time)
                    / (self.sustaining_time)
                )
            else:
                return {}
        entering_time = min(self.entering_time, self.duration() / 3)
        leaving_time = min(self.leaving_time, self.duration() / 3)
        if self.entering is not None:
            if time <= entering_time:
                # logging.info("ENTERING")
                self.last_frame_type = "entering"
                return self.entering(time / entering_time)
        else:
            entering_time = 0
        if self.leaving is not None:
            if time >= self.duration() - leaving_time:
                # logging.info("LEAVING")
                self.last_frame_type = "leaving"
                return self.leaving(
                    (time - self.duration() + leaving_time) / leaving_time
                )
        else:
            leaving_time = 0
        if self.last_frame_type != "sustaining":
            self.target.applyValues(reset=True)
        self.last_frame_type = "sustaining"
        if self.sustaining is not None:
            # logging.info("SUSTAINING", self.sustaining(((time - entering_time) % self.sustaining_time)/ (self.sustaining_time)))
            return self.sustaining(
                ((time - entering_time) % self.sustaining_time) / (self.sustaining_time)
            )
        return {}

    def setDuration(self, duration):
        self._duration = duration

    def duration(self):
        return self._duration

    def updateCurrentTime(self, currentTime: int) -> None:
        value = self.get_value(currentTime)
        # logging.info(value)
        self.target.applyValues(**value)
        return


class LyricLabel(OutlinedLabel):
    @staticmethod
    def _flatten_style_kwargs(style):
        flattened = dict(style)

        nested_map = {
            "font": {
                "size": "font-size",
                "family": "font-family",
                "weight": "font-weight",
                "italic": "font-italic",
                "color": "font-color",
                "image": "font-image",
            },
            "line": {"color": "line-color", "width": "line-width"},
            "background": {"color": "background-color", "image": "background-image"},
            "foreground": {"color": "foreground-color", "image": "foreground-image"},
            "progress": {
                "image": "progress-image",
                "color": "progress-color",
                "line_color": "progress-line-color",
            },
            "shadow": {
                "enabled": "use-shadow",
                "color": "shadow-color",
                "offset": "shadow-offset",
                "radius": "shadow-radius",
            },
            "text": {"flip": "flip-text"},
            "animation": {
                "entering": "animation-entering",
                "sustaining": "animation-sustaining",
                "leaving": "animation-leaving",
            },
        }

        for group, key_map in nested_map.items():
            section = style.get(group)
            if not isinstance(section, dict):
                continue
            flattened.pop(group, None)
            for nested_key, flat_key in key_map.items():
                if nested_key in section:
                    flattened[flat_key] = section[nested_key]

        return flattened

    def __init__(self, text=None, parent=None, progress_enabled=True, **kwargs):

        self._rounded_radius = 0
        self.progress_enabled = progress_enabled

        self.back_imagepad = QLabel("", parent=parent)
        self.back_imagepad.setStyleSheet("background-color: transparent")
        self.back_imagepad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back_pad = Pad(QBrush(QColor(0, 0, 0, 0)), parent=parent)
        self.back_pad.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.animation = None
        self.entering = None
        self.sustaining = None
        self.leaving = None

        super().__init__(
            text=text,
            relative_outline=False,
            linewidth=0,
            brushcolor=QColor(0, 0, 0, 0),
            linecolor=QColor(0, 0, 0, 0),
            parent=parent,
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.front_imagepad = QLabel("", parent=parent)
        self.front_imagepad.setStyleSheet("background-color: transparent")
        self.front_imagepad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.front_pad = Pad(QBrush(QColor(0, 0, 0, 0)), parent=parent)
        self.front_pad.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressbar = ProgressBar(parent=parent)
        self.progressbar.setHidden(not self.progress_enabled)
        self.progressbar_offset = 0
        self.glow_color = QColor(0, 0, 0, 200)

        glow = QGraphicsDropShadowEffect()
        glow.setColor(self.glow_color)
        glow.setBlurRadius(15)
        glow.setOffset(0, 0)
        self.progressbar.setGraphicsEffect(glow)

        self.translation = OutlinedLabel(
            text=text,
            relative_outline=False,
            linewidth=1,
            brushcolor=QColor(255, 0, 0),
            linecolor=QColor(255, 255, 255),
            parent=parent,
        )
        self.translation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyle(**kwargs)

        self.back_pad.show()
        self.back_imagepad.show()
        self.show()
        self.front_pad.show()
        self.front_imagepad.show()

        # self.translation.show()
        # self.translation.setText("<size=0.9>simple translation here/简单的翻译</size>")

        self.left_time = -1

    @pyqtProperty(float)
    def rounded_radius(self):
        return self._rounded_radius

    @rounded_radius.setter
    def rounded_radius(self, value):
        self._rounded_radius = value
        if value > 0:
            self.back_pad.rounded_radius = value
            self.front_pad.rounded_radius = value
        else:
            # self.pad.setStyleSheet("")
            # self.imagepad.setStyleSheet("")
            self.back_pad.rounded_radius = 0
            self.front_pad.rounded_radius = 0
        self.back_pad.update()
        self.front_pad.update()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        glow = self.graphicsEffect()
        if glow is not None:
            color = QColor(self.glow_color)
            color.setAlphaF(color.alphaF() * value)
            glow.setColor(color)
        self.update()

    def setFixedSize(self, width, height):
        super().setFixedSize(width, height)
        self.back_pad.setGeometry(0, 0, width, height)
        self.back_imagepad.setGeometry(0, 0, width, height)
        self.front_pad.setGeometry(0, 0, width, height)
        self.front_imagepad.setGeometry(0, 0, width, height)
        self.progressbar.setGeometry(
            (self.width() - 400) // 2,
            self.height() - 10 + self.progressbar_offset,
            400,
            8,
        )
        self.translation.setGeometry(0, self.height() - 22, width, 22)

    def move(self, x, y):
        super().move(x, y)
        self.back_pad.move(x, y)
        self.back_imagepad.move(x, y)
        self.front_pad.move(x, y)
        self.front_imagepad.move(x, y)
        self.progressbar.move(
            x + (self.width() - 400) // 2,
            y + self.height() - 10 + self.progressbar_offset,
        )
        self.translation.move(x, y + self.height() - 22)

    def paintEvent(self, event):
        super().paintEvent(event)

    def setHidden(self, hidden):
        self.back_pad.setHidden(hidden)
        self.back_imagepad.setHidden(hidden)
        super().setHidden(hidden)
        self.front_pad.setHidden(hidden)
        self.front_imagepad.setHidden(hidden)
        if self.progress_enabled:
            self.progressbar.setHidden(hidden)
        self.translation.setHidden(hidden)

    def setStyle(self, **kwargs):
        kwargs = self._flatten_style_kwargs(kwargs)
        if "font-size" in kwargs:
            self.setFontSize(int(kwargs["font-size"].replace("px", "")))
            self.translation.setFontSize(int(kwargs["font-size"].replace("px", "")))
        if "font-family" in kwargs:
            self.setFontFamily(kwargs["font-family"])
            self.translation.setFontFamily(kwargs["font-family"])
        if "font-weight" in kwargs:
            self.setFontWeight(kwargs["font-weight"])
            self.translation.setFontWeight(kwargs["font-weight"])
        if "font-image" in kwargs:
            self.setBrush(QPixmap(kwargs["font-image"]))
            self.translation.setBrush(QPixmap(kwargs["font-image"]))
        elif "font-color" in kwargs:
            self.setBrush(
                convert_to_color(
                    kwargs["font-color"], width=self.width(), height=self.height()
                )
            )
            self.translation.setBrush(
                convert_to_color(
                    kwargs["font-color"], width=self.width(), height=self.height()
                )
            )
        if "font-italic" in kwargs:
            self.setFontItalic(kwargs["font-italic"])
            self.translation.setFontItalic(kwargs["font-italic"])
        elif "use-italic" in kwargs:
            self.setFontItalic(kwargs["use-italic"])
            self.translation.setFontItalic(kwargs["use-italic"])
        else:
            self.setFontItalic(False)
            self.translation.setFontItalic(False)

        if "flip-text" in kwargs:
            self.flip = kwargs["flip-text"]
            self.translation.flip = kwargs["flip-text"]
        else:
            self.flip = False
            self.translation.flip = False

        if "line-color" in kwargs:
            self.setPen(convert_to_color(kwargs["line-color"]))
            self.translation.setPen(convert_to_color(kwargs["line-color"]))
        if "line-width" in kwargs:
            self.setLineWidth(kwargs["line-width"])
            self.translation.setLineWidth(kwargs["line-width"])

        for key, ip, p in [
            ("background", self.back_imagepad, self.back_pad),
            ("foreground", self.front_imagepad, self.front_pad),
        ]:

            ip.clear()
            p.setStyleSheet("background-color: transparent")
            p.setColor(QColor(0, 0, 0, 0))

            if f"{key}-image" in kwargs:
                p.setColor(QColor(0, 0, 0, 0))
                px = QPixmap(kwargs[f"{key}-image"]).scaledToHeight(
                    self.height(), Qt.SmoothTransformation
                )
                if px.width() > self.width():
                    px = px.copy(
                        (px.width() - self.width()) // 2, 0, self.width(), self.height()
                    )
                if self.rounded_radius > 0:
                    path = QPainterPath()
                    path.addRoundedRect(
                        0,
                        0,
                        self.width(),
                        self.height(),
                        self.rounded_radius,
                        self.rounded_radius,
                    )
                    new_px = QPixmap(self.width(), self.height())
                    new_px.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(new_px)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    painter.setClipPath(path)
                    painter.drawPixmap(0, 0, px)
                    painter.end()
                    px = new_px
                ip.setPixmap(px)

            elif f"{key}-color" in kwargs:
                ip.clear()
                if self.rounded_radius > 0:
                    p.setStyleSheet(f"border-radius: {self.rounded_radius}px;")
                else:
                    p.setStyleSheet("")
                p.setColor(
                    convert_to_color(
                        kwargs[f"{key}-color"], width=self.width(), height=self.height()
                    )
                )

        if "progress-image" in kwargs:
            self.progressbar.progress_color = QPixmap(kwargs["progress-image"])
        elif "progress-color" in kwargs:
            self.progressbar.progress_color = convert_to_color(kwargs["progress-color"])
        elif "font-image" in kwargs:
            self.progressbar.progress_color = QPixmap(kwargs["font-image"])
        elif "font-color" in kwargs:
            self.progressbar.progress_color = convert_to_color(kwargs["font-color"])

        if "progress-line-color" in kwargs:
            self.progressbar.line_color = convert_to_color(
                kwargs["progress-line-color"]
            )
        elif "line-color" in kwargs and (
            "line-width" not in kwargs or kwargs["line-width"] > 0
        ):
            self.progressbar.line_color = convert_to_color(kwargs["line-color"])
        else:
            self.progressbar.line_color = QColor(0, 0, 0, 0)

        if "use-shadow" in kwargs and kwargs["use-shadow"]:
            glow = QGraphicsDropShadowEffect()
            self.glow_color = convert_to_color(kwargs["shadow-color"])
            glow.setColor(self.glow_color)
            glow.setBlurRadius(kwargs["shadow-radius"])
            glow.setOffset(*kwargs["shadow-offset"])
            self.setGraphicsEffect(glow)
        elif "use-shadow" in kwargs and not kwargs["use-shadow"]:
            self.setGraphicsEffect(None)

        if "animation-entering" in kwargs:
            entering = kwargs["animation-entering"]
            # self.entering = [("blinds_progress", [(0.0, 0.5), (1.0, 0.5)])]

            if entering == "fadein":
                self.entering = [("opacity", [(0, 0.1), (1, 1.0)])]
            elif entering == "leftslidein":
                self.entering = [("x_pos", [(0, -self.width()), (1, 0)])]
            elif entering == "rightslidein":
                self.entering = [("x_pos", [(0, self.width()), (1, 0)])]
            elif entering == "topslidein":
                self.entering = [("y_pos", [(0, -self.height()), (1, 0)])]
            elif entering == "bottomslidein":
                self.entering = [("y_pos", [(0, self.height()), (1, 0)])]
            elif entering == "zoomin":
                self.entering = [("scale", [(0, 0.1), (1, 1)])]
            elif entering == "zoomin_overscale":
                self.entering = [("scale", [(0, 0.1), (0.6, 1.5), (1, 1)])]
            else:
                self.entering = None
        if "animation-leaving" in kwargs:
            leaving = kwargs["animation-leaving"]
            # self.leaving = [("blinds_progress", [(0.0, 0.5), (1.0, 0.5)])]
            if leaving == "fadeout":
                self.leaving = [("opacity", [(0, None), (1, 0.1)])]
            elif leaving == "leftslideout":
                self.leaving = [("x_pos", [(0, None), (1, -self.width())])]
            elif leaving == "rightslideout":
                self.leaving = [("x_pos", [(0, None), (1, self.width())])]
            elif leaving == "topslideout":
                self.leaving = [("y_pos", [(0, None), (1, -self.height())])]
            elif leaving == "bottomslideout":
                self.leaving = [("y_pos", [(0, None), (1, self.height())])]
            elif leaving == "zoomout":
                self.leaving = [("scale", [(0, None), (1, 0.1)])]
            else:
                self.leaving = None
        if "animation-sustaining" in kwargs:
            sustaining = kwargs["animation-sustaining"]
            if sustaining == "flickering":
                self.sustaining = [("opacity", [(0, 1.0), (0.5, 0.7), (1, 1.0)])]
            elif sustaining == "hshaking":
                self.sustaining = [("x_pos", [(0, 0), (0.25, 2), (0.75, -2), (1, 0)])]
            elif sustaining == "vshaking":
                self.sustaining = [("y_pos", [(0, 0), (0.25, 2), (0.75, -2), (1, 0)])]
            elif sustaining == "zooming":
                self.sustaining = [("scale", [(0, 1), (0.5, 0.9), (1, 1)])]
            else:
                self.sustaining = None

    def applyValues(self, reset=False, **kwargs):
        if "scale" in kwargs:
            self.scale = kwargs["scale"]
        elif reset:
            self.scale = 1
        if "opacity" in kwargs:
            self.opacity = kwargs["opacity"]
        elif reset:
            self.opacity = 1
        if "x_pos" in kwargs:
            self.x_pos = kwargs["x_pos"]
        elif reset:
            self.x_pos = 0
        if "y_pos" in kwargs:
            self.y_pos = kwargs["y_pos"]
        elif reset:
            self.y_pos = 0

    def adjustLineProgress(self, line_progress):
        if self.animation is not None:
            if self.animation.state() == QPropertyAnimation.Running:
                self.animation.pause()
            else:
                self.animation.start()
                self.animation.pause()
            self.applyValues(reset=True)
            self.animation.setCurrentTime(line_progress)
            self.animation.resume()

    def setText(self, text, use_animation=True, duration=None, start_time=None):
        # logging.info(text, use_animation, duration, start_time)
        super().setTextRich(text)
        self.applyValues(reset=True)
        self.update()
        if duration is not None:
            if duration < 0:
                duration = None
            else:
                duration = int(duration)
        else:
            duration = -1

        # PYQT5
        # if self.animation is not None and self.animation.state() == QPropertyAnimation.Running:
        #     self.animation.stop()
        # PyQt5
        if (
            self.animation is not None
            and self.animation.state() == QAbstractAnimation.State.Running
        ):
            self.animation.stop()
        if use_animation:
            if self.animation is None:
                self.animation = LyricAnimation(
                    self,
                    duration,
                    entering=self.entering,
                    sustaining=self.sustaining,
                    leaving=self.leaving,
                )
            else:
                self.animation.setAnimation(
                    entering=self.entering,
                    sustaining=self.sustaining,
                    leaving=self.leaving,
                )
                self.animation.setDuration(duration)
            self.animation.start()
            if start_time is not None:
                self.animation.setCurrentTime(
                    int(datetime.now().timestamp() * 1000 - start_time)
                )
        else:
            self.animation = None

    def setProgress(self, progress):
        if not self.progress_enabled:
            return
        self.progressbar.progress = progress


if __name__ == "__main__":

    import sys

    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("LyricLabel Test")
    window.setGeometry(100, 100, 400, 100)

    layout = QVBoxLayout()

    label = LyricLabel(
        text="Test Lyric",
        parent=window,
        **{
            "font-size": "48px",
            "font-family": "Arial",
            "font-color": "#FFFFFF",
            "line-color": "#FF0000",
            "line-width": 2,
            "background-color": "#000000",
            "entering": "fadein",
            "leaving": "fadeout",
            "sustaining": "flickering",
        },
    )
    label.setFixedSize(400, 100)

    layout.addWidget(label)
    window.setLayout(layout)
    window.show()

    label.setText("<small>Small text</small> and <big>big text</big>", True, 10000)
    # label.setRichText("hello world", True, 10000)

    sys.exit(app.exec_())
