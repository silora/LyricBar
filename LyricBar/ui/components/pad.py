from PyQt5.QtGui import QPainter, QBrush, QGradient, QPainterPath
from PyQt5.QtWidgets import QLabel

class Pad(QLabel):
    def __init__(self, color, parent=None):
        super().__init__("", parent)
        self.brush = QBrush(color)
        
    def setColor(self, color):
        self.brush = QBrush(color)
        self.update()   
        
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.brush.gradient() is not None and self.brush.gradient().type() == QGradient.Type.RadialGradient and self.brush.gradient().coordinateMode() == QGradient.CoordinateMode.LogicalMode:
            path = QPainterPath()
            path.addEllipse(self.brush.gradient().center(), 5, 5)
            painter.fillPath(path, self.brush.gradient().stops()[0][1])
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), self.brush)