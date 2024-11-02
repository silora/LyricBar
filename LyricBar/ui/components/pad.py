from PyQt5.QtGui import QPainter, QBrush
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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), self.brush)