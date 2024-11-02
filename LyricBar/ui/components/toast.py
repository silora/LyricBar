# from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
# from PyQt5.QtGui import QColor

# from .outlinedlabel import OutlinedLabel

# class Toast(OutlinedLabel):
#     def __init__(self, parent, text, font_color=QColor(80, 80, 80), font=None, duration=2000):
#         super().__init__("", parent=parent, brushcolor=font_color)

#         self.setStyleSheet(f"background: rgba(200, 200, 200, 1); font-size: 20px; font-family: Spotify Mix, Arial, Microsoft YaHei UI; font-weight: bold; padding: 8px; border-radius: 5px;")
#         if font is not None:
#             self.setFont(font)
#         self.setText(text)
#         self.setAlignment(Qt.AlignCenter)

#         self.fade_in_animation = QPropertyAnimation(self, b"opacity")
#         self.fade_in_animation.setDuration(100)
#         self.fade_in_animation.setStartValue(0.1)
#         self.fade_in_animation.setEndValue(1.0)

#         self.fade_out_animation = QPropertyAnimation(self, b"opacity")
#         self.fade_out_animation.setDuration(300)
#         self.fade_out_animation.setStartValue(1.0)
#         self.fade_out_animation.setEndValue(0.1)

#         # Timer for sustaining
#         self.timer = QTimer()
#         self.timer.setSingleShot(True)
#         self.timer.timeout.connect(self.start_fade_out)

#         # Show the toast
#         self.show()
#         self.fade_in_animation.start()
#         self.timer.start(1000)  # Sustain for 1 second

#         # Connect the finished signal of fade-out animation to the delete method
#         self.fade_out_animation.finished.connect(self.deleteLater)

#     def start_fade_out(self):
#         self.fade_out_animation.start()