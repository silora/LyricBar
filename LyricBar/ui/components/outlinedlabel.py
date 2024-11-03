import math
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize, pyqtProperty, pyqtSignal, QMutex
from PyQt5.QtGui import QBrush, QFontMetrics, QPainter, QPainterPath, QPen, QColor, QPixmap, QTransform



# QPainterPath Form::pathText(int x, int y, QFont font, const QString &text)
# {
#     QPainterPath path;
 
#     qreal lineHeight = QFontMetricsF(font).height();
#     int lineCount = 1;
#     QByteArray content = text.toUtf8();
#     QBuffer buff(&content);
#     buff.open(QBuffer::ReadOnly);
#     while(!buff.atEnd()) {
#         QByteArray line = buff.readLine();
#         path.addText(x, y + lineCount * lineHeight, font, line);
#         lineCount++;
#     }
#     return path;

def getTextPath(font, text, alignment):
    metrics = QFontMetrics(font)
    line_height = metrics.height()
    lines = text.split("\n")
    widths = [metrics.boundingRect(line).width() for line in lines]
    max_width = max(widths)
    # print(lines)
    path = QPainterPath()
    for idx, line in enumerate(lines):
        if alignment & Qt.AlignmentFlag.AlignLeft:
            path.addText(0, line_height * idx, font, line)
            pass
        elif alignment & Qt.AlignmentFlag.AlignRight:
            path.addText(max_width - widths[idx], line_height * idx, font, line)
        elif alignment & Qt.AlignmentFlag.AlignHCenter:
            path.addText((max_width - widths[idx]) / 2, line_height * idx, font, line)
    return path
    

class OutlinedLabel(QLabel):
    update_signal = pyqtSignal()
    def __init__(self, text=None, relative_outline=True, linewidth=1/25, brushcolor=QColor(255, 255, 255), linecolor=QColor(0, 0, 0), parent=None, **kwargs):
        super().__init__(text=text, parent=parent, **kwargs)
        self.w = linewidth
        self.mode = relative_outline
        self.flip = False
        self._opacity = 1
        self._scale = 1
        
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
        

        self.setBrush(brushcolor)
        self.setPen(linecolor)
        
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
        self._opacity = value
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
        
    @pyqtProperty(str)
    def font_family(self):
        return self.font().family()
    
    @font_family.setter
    def font_family(self, value):
        f = self.font()
        f.setFamily(value)
        self.setFont(f)
        self.updatePath()
        
    @pyqtProperty(int)
    def font_weight(self):
        return self.font().weight()
    
    @font_weight.setter
    def font_weight(self, value):
        f = self.font()
        f.setWeight(value)
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
        self.path.setFillRule(Qt.FillRule.WindingFill)
        self.path = self.path.simplified()
        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())
        if self.font() is not None:
            f = self.font()
            f.setPixelSize(self.font_size)
            self.setFont(f)
        tr = self.path.boundingRect().adjusted(0, 0, int(w), int(w))
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
        self._indent[0] += metrics.descent()
        self._indent[2] += metrics.height() * len(self.text().split("\n")) - self.path.boundingRect().height()
        x = rect.left() 
        y = rect.top() + metrics.ascent()
        
        self.path.translate(x, y)
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
        self.qmap = QPixmap(int(self.path.boundingRect().right() + self._indent[1] + self._indent[3]), int(self.path.boundingRect().bottom() + self._indent[0] + self._indent[2]))
        self.qmap.fill(Qt.GlobalColor.transparent)
        qp = QPainter(self.qmap)
        qp.translate(self._indent[1], self._indent[0])

        qp.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        if self.flip:
            qp.scale(-1, 1)
            qp.translate(-self.qmap.width(), 0)
        if self.outlineThickness() > 0:
            self.pen.setWidthF(w * 2)
            qp.strokePath(self.path, self.pen)
        qp.fillPath(self.path, self.brush)
        qp.end()
        
        if self.qmap.width() > self.width(): # or self.qmap.height() > self.height():
            scale = min(self.width() / self.qmap.width(), self.height() / self.qmap.height())
            self.qmap = self.qmap.scaled(int(self.qmap.width() * scale), int(self.qmap.height() * scale))
        
        self.path_mutex.unlock()
        self.qmap_mutex.unlock()
    
    def paintEvent(self, event):
        if not self.qmap_mutex.tryLock():
            return
        if self.qmap is None:
            self.qmap_mutex.unlock()
            return
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        
        qmap = QPixmap(self.qmap)        
        
        scale = self.scale
        if scale != 1:
            qmap = qmap.scaled(int(qmap.width() * scale), int(qmap.height() * scale))
        qp.setOpacity(self.opacity)
        
        x, y = 0, 0
        if self.alignment() & Qt.AlignmentFlag.AlignLeft:
            x = 0
        elif self.alignment() & Qt.AlignmentFlag.AlignRight:
            x = self.width() - qmap.width()
        else:
            x = (self.width() - qmap.width()) // 2
        
        if self.alignment() & Qt.AlignmentFlag.AlignTop:
            y = 0
        elif self.alignment() & Qt.AlignmentFlag.AlignBottom:
            y = self.height() - qmap.height()
        else:
            y = (self.height() - qmap.height()) // 2
        
        qp.drawPixmap(x, y, qmap)
        qp.end()
        self.qmap_mutex.unlock()
        
        