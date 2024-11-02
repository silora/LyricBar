from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PIL import ImageGrab
from PIL import Image
import numpy as np


def gen_qmap(geom):
    sample_geom = geom.adjusted(-1, 0, 1, 0)
    img = ImageGrab.grab((sample_geom.left(), sample_geom.top(), sample_geom.right()+1, sample_geom.bottom()+1))
    # screenshot = pyautogui.screenshot(region=(sample_geom.left(), sample_geom.top(), sample_geom.width(), sample_geom.height()))
    # img = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
    left_colors = np.zeros((geom.height(), 3), dtype=np.float32)
    for i in range(geom.height()):
        left_colors[i] = img.getpixel((0, i))
        # left_colors[i] = img[0, i]
    right_colors = np.zeros((geom.height(), 3), dtype=np.float32)
    for i in range(geom.height()):
        right_colors[i] = img.getpixel((-1, i))
        # right_colors[i] = img[geom.width()-1, i]
    
    pixels = np.linspace(left_colors, right_colors, geom.width(), axis=0).astype(dtype=np.uint8).transpose(1, 0, 2)
    image = Image.fromarray(pixels)
    qmap = QImage(image.tobytes(), image.width, image.height, QImage.Format.Format_RGB888)
    
    return qmap


class FauxTaskbar(QLabel):
    update_signal = pyqtSignal()
    def __init__(self, parent=None, geometry_reference=None):
        super().__init__("", parent)
        self._blending = None
        self.geometry_reference = geometry_reference
        self.blending = gen_qmap(self.geometry_reference.geometry())
        
        self.update_signal.connect(self.update_faux_taskbar)
        
    
    def update_faux_taskbar(self):
        self.blending = gen_qmap(self.geometry_reference.geometry())
        self.update()
        
    def update_taskbar(self):
        self.update_signal.emit()
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.blending)

