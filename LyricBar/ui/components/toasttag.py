from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, pyqtProperty, QPropertyAnimation, QTimer
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QRadialGradient

from .outlinedlabel import OutlinedLabel


class ToastBubble(QLabel):
    def __init__(self, parent=None):
        super(ToastBubble, self).__init__("", parent)
        self._opacity = 1.0
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
        
    def paintEvent(self, event):
        radius = min(self.width() // 2, self.height())
        pad = QPainterPath()
        pad.addEllipse(0, - radius, 2 * radius, 2 * radius)
        box = QPainterPath()
        box.addRect(0, 0, 2 * radius, radius)
        pad = pad.intersected(box)
        
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QRadialGradient(radius, 0, radius)
        gradient.setColorAt(0, QColor(201, 142, 162))
        gradient.setColorAt(0.8, QColor(255, 214, 228))
        gradient.setColorAt(0.9, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillPath(pad, gradient)
        painter.end()

class ToastTag(QLabel):
    def __init__(self, text_color=QColor(0, 0, 0, 150), parent=None):
        super(ToastTag, self).__init__("", parent)
        self.text_color = text_color
        
        self.bubble = ToastBubble(parent=self)
        self.bubble.setGeometry(0, 0, self.width(), self.height())
        
        self.text = OutlinedLabel("omghiiii", parent=self, brushcolor=text_color, relative_outline=False, linewidth=0)
        self.text.setGeometry(0, 0, self.width(), self.height())
        self.text.setFontFamily("Spotify Mix, Arial, Microsoft YaHei UI")
        self.text.setFontSize(15)
        self.text.setFontWeight("bold")
        self.text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(10)
        glow.setColor(text_color)
        glow.setOffset(0, 0)
        self.text.setGraphicsEffect(glow)
        
        
        self._opacity = 1.0
        self.fade_in_animation = QPropertyAnimation(self, b"opacity")
        self.fade_in_animation.setDuration(100)
        self.fade_in_animation.setStartValue(0.1)
        self.fade_in_animation.setEndValue(1.0)

        self.fade_out_animation = QPropertyAnimation(self, b"opacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.1)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out_animation.start)
        
    def setGeometry(self, x, y, w, h):
        super().setGeometry(x, y, w, h)
        self.bubble.setGeometry(0, 0, w, h)
        self.text.setGeometry(0, 0, w, h)
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.bubble.opacity = value
        self.text.opacity = value
    
    def add_newline(self, text, max_width=14):
        words = text.replace(" ", "\n").split("\n")
        i = 0
        while i + 1 < len(words):
            if len(words[i]) + len(words[i+1]) < max_width:
                words[i] += " " + words.pop(i+1)
            else:
                i += 1
        return "\n".join(words)
    
    # def setHidden(self, value):
    #     super().setHidden(value)
    #     self.bubble.setHidden(value)
    #     self.text.setHidden(value)
    
    def start(self, text=None, duration=1000):
        if text is not None:
            self.text.setText(self.add_newline(text))
            self.text.update()
        self.end()
        self.setHidden(False)

        self.show()
        self.fade_in_animation.start()
        self.timer.start(duration)
        
        self.fade_out_animation.finished.connect(lambda: self.setHidden(True))
        
    
    def end(self):
        self.setHidden(True)
        if self.fade_in_animation is not None and self.fade_in_animation.state() == QPropertyAnimation.State.Running:
            self.fade_in_animation.stop()
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()
        if self.fade_out_animation is not None and self.fade_out_animation.state() == QPropertyAnimation.State.Running:
            self.fade_out_animation.stop()
            
    
        
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
    
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.resize(400, 400)
    win.setLayout(QVBoxLayout())
    win.layout().addWidget(ToastTag("hiiiii"))
    win.show()
    
    sys.exit(app.exec_())