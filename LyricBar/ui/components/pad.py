from PyQt5.QtGui import QPainter, QBrush, QGradient, QPainterPath
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QLabel

class Pad(QLabel):
    def __init__(self, color, parent=None):
        super().__init__("", parent)
        self.brush = QBrush(color)
        self.rounded_radius = 0
        
    def setColor(self, color):
        self.brush = QBrush(color)
        self.update()   
        
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.brush.gradient() is not None and self.brush.gradient().type() == QGradient.Type.RadialGradient and self.brush.gradient().CoordinateMode == QGradient.CoordinateMode.LogicalMode:
            print(self.brush.gradient().focalPoint())
            center = QPointF(self.brush.gradient().focalPoint())
            center.setX(center.x() * self.width())
            center.setY(center.y() * self.height())
            path = QPainterPath()
            path.addEllipse(center, 1, 1)
            painter.fillPath(path, self.brush.gradient().stops()[0][1])
        painter.setRenderHints(QPainter.RenderHint.Antialiasing) # | QPainter.RenderHint.HighQualityAntialiasing)
        if self.rounded_radius > 0:
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), self.rounded_radius, self.rounded_radius)
            painter.fillPath(path, self.brush)
        else:
            painter.fillRect(self.rect(), self.brush)