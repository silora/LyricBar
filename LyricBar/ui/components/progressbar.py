from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QLabel


class ProgressBar(QLabel):
    def __init__(self, parent=None, progress_color=QColor(255, 255, 255, 200), background_color=QColor(0, 0, 0, 48), line_color=QColor(0, 0, 0, 0)):
        super().__init__("", parent)
        self.progress = 0
        self.progress_color = progress_color
        self.background_color = background_color
        self.line_color = line_color
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()
        path.addRoundedRect(QRectF(2, 2, self.width()-4, self.height()-4), 4, 4)
        painter.fillPath(path, self.background_color)
        progress = max(0, self.progress)
        path = QPainterPath()
        path.addRoundedRect(QRectF(2, 2, int((self.width()-4) * progress), (self.height()-4)), 4, 4)
        painter.fillPath(path, QBrush(self.progress_color))
        
        pen = QPen(self.line_color)
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.strokePath(path, pen)
        
        # self.left_time.paintEvent(event)
        # self.right_time.paintEvent(event)
        