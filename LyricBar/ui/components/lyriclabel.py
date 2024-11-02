from .pad import Pad
from .outlinedlabel import OutlinedLabel
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QBrush, QColor, QPixmap
      

class LyricLabel(OutlinedLabel):
    def __init__(self, width, height, text=None, font_family="Arial", font_size=10, font_weight="normal", use_italic=False, line_color=Qt.black, line_width=1/25, brush_color=Qt.white, background_color=QColor(0, 0, 0, 0), background_image=None, entering="fadein", sustain=None, leaving=None, parent=None):
        
        self.width = width
        self.height = height
        
        self.imagepad = QLabel("", parent=parent)
        self.imagepad.setStyleSheet("background-color: transparent")
        if background_image is not None:
            image = QPixmap(background_image)
            image = image.scaled(1, self.height, Qt.KeepAspectRatioByExpanding)
            self.imagepad.setPixmap(image)
        self.imagepad.setFixedSize(width, height)
            
        self.pad = Pad(QBrush(background_color), parent=self)
        self.pad.setFixedSize(width, height)
        
        super().__init__(text=text, relative_outline=False, linewidth=line_width, brushcolor=brush_color, linecolor=line_color, parent=parent)
        self.setFixedSize(width, height)
        
        self.setFontFamily(font_family)
        self.setFontSize(font_size)
        self.setFontWeight(font_weight)
        self.setFontItalic(use_italic)
        
        
        self.entering = None
        self.sustain = None
        self.leaving = None
        if entering is not None:
            if entering == "fadein":
                self.entering = QPropertyAnimation(self, b"opacity")
                self.entering.setStartValue(0.1)
                self.entering.setEndValue(1.0)
            elif entering == "leftslidein":
                self.entering = QPropertyAnimation(self, b"x")
                self.entering.setStartValue(-self.width())
                self.entering.setEndValue(0)
            elif entering == "rightslidein":
                self.entering = QPropertyAnimation(self, b"x")
                self.entering.setStartValue(self.width())
                self.entering.setEndValue(0)
            elif entering == "topslidein":
                self.entering = QPropertyAnimation(self, b"y")
                self.entering.setStartValue(-self.height())
                self.entering.setEndValue(0)
            elif entering == "bottomslidein":
                self.entering = QPropertyAnimation(self, b"y")
                self.entering.setStartValue(self.height())
                self.entering.setEndValue(0)
            elif entering == "zoomin":
                self.entering = QPropertyAnimation(self, b"font_size")
                self.entering.setStartValue(1)
                self.entering.setEndValue(self.font_size)
            elif entering == "zoomin_overscale":
                self.entering = QPropertyAnimation(self.label, b"font_size")
                self.entering.setStartValue(1)
                self.entering.setEndValue(self.font_size)
            self.entering.setDuration(150)
        
    def paintEvent(self, event):
        self.pad.paintEvent(event)
        self.imagepad.paintEvent(event)
        super().paintEvent(event)
        
    def setHidden(self, hidden):
        self.pad.setHidden(hidden)
        self.imagepad.setHidden(hidden)
        super().setHidden(hidden)
        
    def setBackgroundColor(self, color):
        self.pad.setColor(QBrush(color))
        
    def setBackgroundImage(self, image):
        if image is not None:   
            image = QPixmap(image)
            image = image.scaled(1, self.height, Qt.KeepAspectRatioByExpanding)
            self.imagepad.setPixmap(image)
        else:
            self.imagepad.clear()
            
    def setStyle(self, **kwargs):
        if "font_size" in kwargs:
            self.setFontSize(kwargs["font_size"])
            if self.entering is not None and self.entering.propertyName() == b"font_size":
                self.entering.setEndValue(kwargs["font_size"])
        if "font_family" in kwargs:
            self.setFontFamily(kwargs["font_family"])
        if "font_weight" in kwargs:
            self.setFontWeight(kwargs["font_weight"])
        if "use_italic" in kwargs:
            self.setFontItalic(kwargs["use_italic"])
        if "brush_color" in kwargs:
            self.setBrush(QColor(kwargs["brush_color"]))
        if "line_color" in kwargs:
            self.setPen(QColor(kwargs["line_color"]))
        if "background_color" in kwargs:
            self.setBackgroundColor(QColor(kwargs["background_color"]))
        if "background_image" in kwargs:
            self.setBackgroundImage(kwargs["background_image"])
            
    def setText(self, text, use_animation=True):
        super().setText(text)
        self.update()
        if use_animation and self.entering is not None:
            if self.entering.isRunning():
                self.entering.stop()
            self.entering.start()
    
    
        
        
    
        
    
        
    