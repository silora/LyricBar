import math
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize, pyqtProperty, pyqtSignal, QMutex, QRect, QByteArray, QFile
from PyQt5.QtGui import QBrush, QFontMetrics, QPainter, QPainterPath, QPen, QColor, QPixmap, QTransform, QFontMetricsF, QFontDatabase, QFont, QFontInfo
import os



FONT_DB = QFontDatabase
FONT_DICT = {}

get_path_lock = QMutex()

def getTextPath(font, text, alignment):
    for i in range(5):
        font = QFont(font) if isinstance(font, str) else font
        font.setRawMode(True)
        # font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        metrics = QFontMetricsF(font)
        line_height = metrics.height()
        lines = text.split("\n")
        widths = [metrics.tightBoundingRect(line).width() for line in lines]
        max_width = max(widths)
        # print(lines)
        path = QPainterPath()
        for idx, line in enumerate(lines):
            if alignment & Qt.AlignmentFlag.AlignLeft:
                path.addText(0, line_height * idx, font, line)
            elif alignment & Qt.AlignmentFlag.AlignRight:
                path.addText(max_width - widths[idx], line_height * idx, font, line)
            else:
                path.addText((max_width - widths[idx]) / 2, line_height * idx, font, line)
        if path.boundingRect().height() >= 3:
            # if i > 0:
            #     output = QPixmap(math.ceil(path.boundingRect().width()), math.ceil(path.boundingRect().height()))
            #     output.fill(Qt.GlobalColor.transparent)
            #     painter = QPainter(output)
            #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            #     painter.fillPath(path.translated(-path.boundingRect().topLeft()), QColor(255, 255, 255))
            #     out_file = f"log_images/{text}_true.png"
            #     output.save(out_file, "png")
            #     painter.end()
            # print("True", {"family": QFontInfo(font).family(), "pointSize": QFontInfo(font).pointSize(), "pixelSize": QFontInfo(font).pixelSize(), "weight": QFontInfo(font).weight(), "italic": QFontInfo(font).italic(), "styleName": QFontInfo(font).styleName(), "styleHint": QFontInfo(font).styleHint(), "fixedPitch": QFontInfo(font).fixedPitch(), "exactMatch": QFontInfo(font).exactMatch(), "style": QFontInfo(font).style()})
            # get_path_lock.unlock()
            return path
        if path.boundingRect().height() < 3 or i > 0:
            # output = QPixmap(math.ceil(path.boundingRect().width()), math.ceil(path.boundingRect().height()))
            # output.fill(Qt.GlobalColor.transparent)
            # painter = QPainter(output)
            # painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            # painter.fillPath(path.translated(-path.boundingRect().topLeft()), QColor(255, 255, 255))
            # out_file = f"log_images/{text}.png"
            # output.save(out_file, "png")
            # painter.end()
            # print(lines, line_height, max_width, widths, path.boundingRect().width(), path.boundingRect().height())    
            # print((max_width - widths[0]) / 2, line_height * 0)
            print("Failed", {"family": QFontInfo(font).family(), "pointSize": QFontInfo(font).pointSize(), "pixelSize": QFontInfo(font).pixelSize(), "weight": QFontInfo(font).weight(), "italic": QFontInfo(font).italic(), "styleName": QFontInfo(font).styleName(), "styleHint": QFontInfo(font).styleHint(), "fixedPitch": QFontInfo(font).fixedPitch(), "exactMatch": QFontInfo(font).exactMatch(), "style": QFontInfo(font).style()})
            print(metrics.height(), metrics.ascent(), metrics.descent(), metrics.leading(), metrics.lineSpacing())
    # get_path_lock.unlock()
    return None
    

class OutlinedLabel(QLabel):
    update_signal = pyqtSignal()
    def __init__(self, text=None, relative_outline=True, linewidth=1/25, brushcolor=QColor(255, 255, 255), linecolor=QColor(0, 0, 0), parent=None, **kwargs):
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
        
        self._indent = None
        
        self.right_pad = False  
        self.use_scale = True

        self.setBrush(brushcolor)
        self.setPen(linecolor)
        
        # global FONT_DB
        # if not FONT_DB:
        #     FONT_DB = QFontDatabase
        
    def setLineWidth(self, width):
        self.w = width
        
    def setText(self, text):
        super().setText(text)
        self.updatePath()
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value):
        # if value < 1:
        #     self.frame_counter += 1
        # else:
        #     print("Frame Counter: ", self.frame_counter)
        #     self.frame_counter = 0
        # print("opacity: ", value)
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
        #     print(family)
        
        if not any([_ in value.lower() for _ in [".ttf", ".otf", ".ttc"]]):
            f.setFamily(value)
        else:
            value = os.path.abspath(value)
            if value in FONT_DICT:
                # print("font already loaded")
                id = FONT_DICT[value]
                fam = FONT_DB.applicationFontFamilies(id)[0]
                f.setFamily(fam)
            else:
                # print("loading font")
                for i in range(10):
                    fontfile = QFile(value)
                    fontfile.open(QFile.OpenModeFlag.ReadOnly)
                    fontdata = QByteArray(fontfile.readAll())
                    id = FONT_DB.addApplicationFontFromData(fontdata)
                    if id != -1:
                        FONT_DICT[value] = id
                        break
                if id == -1:
                    # print("failed to load font")
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
        if self.text() is None or self.text() == "" or self.font() is None:
            return
        if not self.path_mutex.tryLock():
            return
        self.path = getTextPath(self.font(), self.text(), self.alignment())
        
        if self.path is None:
            self.path_mutex.unlock()
            return
        self.path.setFillRule(Qt.FillRule.WindingFill)
        # self.path = self.path.simplified()
        # print(self.path.boundingRect())
        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())
        # if self.font() is not None:
        #     f = self.font()
        #     f.setPixelSize(self.font_size)
        #     self.setFont(f)
        # tr = self.path.boundingRect().adjusted(0, 0, int(w), int(w))
        if self.indent() == -1:
            if self.frameWidth():
                self._indent = [(metrics.boundingRect('x').width() + w * 2) / 2] * 4
            else:
                self._indent = [w] * 4
        else:
            self._indent = [self.indent()] * 4
        # if self.alignment() & Qt.AlignmentFlag.AlignLeft:
        #     x = rect.left() + indent - min(metrics.leftBearing(self.text()[0]), 0)
        # elif self.alignment() & Qt.AlignmentFlag.AlignRight:
        #     x = rect.x() + rect.width() - indent - tr.width()
        # else:
        #     x = (rect.width() - tr.width()) / 2
            
        # if self.alignment() & Qt.AlignmentFlag.AlignTop:
        #     y = rect.top() + indent + metrics.ascent()
        # elif self.alignment() & Qt.AlignmentFlag.AlignBottom:
        #     y = rect.y() + rect.height() - indent - metrics.descent()
        # else:
        #     y = (rect.height() + metrics.ascent() - metrics.descent()) / 2
        
        # print(self.text()[0], len(self.text()[0]))
        longest = max([_ for _ in self.text().split("\n")], key=len)
        

        try:
            self._indent[1] -= min(metrics.leftBearing(longest[0]), -2)
        except:
            self._indent[1] += 2
        try:
            self._indent[3] -= min(metrics.rightBearing(longest[-1]), -2)
        except:
            self._indent[3] += 2
            
        x = rect.left() 
        y = max(metrics.ascent(), -self.path.boundingRect().top())
        self.path.translate(x, y)
        
        # self._indent[0] += metrics.descent()
        self._indent[0] += 0
        self._indent[2] += max(metrics.height() * len(self.text().split("\n")) - self.path.boundingRect().bottom(), 0)
        
        if self.right_pad:
            last_word = self.text().split("\n")[-1].split(" ")[-1]
            self._indent[3] += max(self.path.boundingRect().width() - 500, 0)  #- getTextPath(self.font(), last_word, self.alignment()).boundingRect().width()
        
        # print(metrics.height(), metrics.descent(), metrics.ascent())
        # print(self._indent)
        

        
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
        
        # print(self._indent)
        
        w = self.outlineThickness()
        # print("box size", int(self.path.boundingRect().right() + self._indent[1] + self._indent[3]), int(self.path.boundingRect().bottom() + self._indent[0] + self._indent[2]))
        self.qmap = QPixmap(int(self.path.boundingRect().right() + self._indent[1] + self._indent[3]), int(self.path.boundingRect().bottom() + self._indent[0] + self._indent[2]))
        self.qmap.fill(Qt.GlobalColor.transparent)
        qp = QPainter(self.qmap)
        qp.translate(self._indent[1], self._indent[0])

        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.outlineThickness() > 0:
            self.pen.setWidthF(w * 2)
            qp.strokePath(self.path, self.pen)
        qp.fillPath(self.path, self.brush)
        qp.end()
        
        if self.qmap.width() > self.width() and self.use_scale: # or self.qmap.height() > self.height():
            scale = min(self.width() / self.qmap.width(), self.height() / self.qmap.height())
            self.qmap = self.qmap.scaled(int(self.qmap.width() * scale), int(self.qmap.height() * scale), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        
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
        qp.setRenderHints(QPainter.RenderHint.Antialiasing) # | QPainter.RenderHint.SmoothPixmapTransform)
        # qp.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        qmap = self.qmap
        
        scale = self.scale
        # qp.scale(scale, scale)
        if scale != 1:
            qmap = qmap.scaled(int(qmap.width() * scale), int(qmap.height() * scale), transformMode=Qt.SmoothTransformation)
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
            x = (self.width() - qmap.width())/ 2
        
        if self.alignment() & Qt.AlignmentFlag.AlignTop:
            y = 0
        elif self.alignment() & Qt.AlignmentFlag.AlignBottom:
            y = self.height() - qmap.height()
        else:
            y = (self.height() - qmap.height()) // 2
        
        # in_motion = self.scale != 1 or self.x_pos != 0 or self.y_pos != 0
        # if in_motion:
        #     pos = ((x + self.x_pos), (y + self.y_pos))
        #     pos_1 = (math.floor((x + self.x_pos)), math.floor((y + self.y_pos)))
        #     pos_2 = (math.ceil((x + self.x_pos)), math.ceil((y + self.y_pos)))
        #     dis_1 = math.sqrt((pos_1[0] - pos[0]) ** 2 + (pos_1[1] - pos[1]) ** 2)
        #     dis_2 = math.sqrt((pos_2[0] - pos[0]) ** 2 + (pos_2[1] - pos[1]) ** 2)
            
        #     if dis_1 != 0:
        #         new_map = QPixmap(qmap.width() + (1 if (pos_1[0] != pos_2[1]) else 0), qmap.height() + (1 if (pos_1[1] != pos_2[1]) else 0))
        #         new_map.fill(Qt.GlobalColor.transparent)
        #         painter = QPainter(new_map)
        #         # painter.setOpacity(self.opacity * min(1, dis_2 / (dis_1 + dis_2 + 0.00001)))
        #         painter.drawPixmap(0, 0, qmap)
        #         # painter.setCompositionMode(QPainter.CompositionMode_ColorDodge)
        #         painter.setOpacity(self.opacity * min(1, dis_1 / (dis_1 + dis_2 + 0.00001)))
        #         painter.drawPixmap(1 if (pos_1[0] != pos_2[1]) else 0, 1 if (pos_1[1] != pos_2[1]) else 0, qmap.copy(QRect(0, 0, qmap.width()//2, qmap.height())))
        #         painter.end()
        #         qmap = new_map
        #     qp.drawPixmap(pos_1[0], pos_1[1], qmap)
        #     # qp.drawPixmap(int((x + self.x_pos)), int((y + self.y_pos)), qmap)
        #     # print("motion", pos, pos_1, pos_2, self.opacity * dis_2 / (dis_1 + dis_2 + 0.00001), self.opacity * dis_1 / (dis_1 + dis_2 + 0.00001))
        # else:
        #     qp.drawPixmap(int((x + self.x_pos)), int((y + self.y_pos)), qmap)
        qp.drawPixmap(int((x + self.x_pos)), int((y + self.y_pos)), qmap)
        qp.end()
        self.qmap_mutex.unlock()
        
        