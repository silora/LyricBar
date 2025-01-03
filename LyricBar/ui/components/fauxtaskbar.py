from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PIL import ImageGrab
from PIL import Image
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QMutex
from mss.windows import MSS as mss

from .outlinedlabel import get_path_lock
# import timeit


# class ColorGrabberThread(QThread):
#     colors_grabbed = pyqtSignal(object, object)

#     def __init__(self, geom_ref, parent=None):
#         super().__init__(parent)
#         self.geom_ref = geom_ref

#     def run(self):
#         left_colors, right_colors = self.grab_colors()
#         self.colors_grabbed.emit(left_colors, right_colors)

#     def grab_colors(self):
#         # start_time = timeit.default_timer()
#         geom = self.geom_ref.geometry()
#         sample_geom = geom.adjusted(-1, 0, 1, 0)
#         img = None
#         try:
#             img = ImageGrab.grab((sample_geom.left(), sample_geom.top(), sample_geom.right()+1, sample_geom.bottom()+1), all_screens=True)
#         except Exception as e:
#             return None, None
#         left_colors = np.zeros((geom.height(), 3), dtype=np.float32)
#         for i in range(geom.height()):
#             left_colors[i] = img.getpixel((0, i))
#         right_colors = np.zeros((geom.height(), 3), dtype=np.float32)
#         for i in range(geom.height()):
#             right_colors[i] = img.getpixel((-1, i))
        
#         # elapsed = timeit.default_timer() - start_time
#         # print(f"Time taken to grab colors: {elapsed} seconds")
        
#         return left_colors, right_colors

class ColorGrabberThread(QThread):

    def __init__(self, geom_ref, parent=None):
        super().__init__(parent)
        self.geom_ref = geom_ref

    def run(self):
        left_colors, right_colors = self.grab_colors()
        self.parent().colors_grabbed.emit(left_colors, right_colors)
        self.parent().updateMutex.unlock()
        get_path_lock.unlock()

    def grab_colors(self):
        # start_time = timeit.default_timer()
        geom = self.geom_ref.geometry()
        sample_geom = geom.adjusted(-1, 0, 1, 0)
        img = None
        try:
            img = mss().grab((sample_geom.left(), sample_geom.top(), sample_geom.right()+1, sample_geom.bottom()+1))
        except Exception as e:
            return None, None
        left_colors = np.zeros((geom.height(), 3), dtype=np.float32)
        for i in range(geom.height()):
            left_colors[i] = img.pixel(0, i)
        right_colors = np.zeros((geom.height(), 3), dtype=np.float32)
        for i in range(geom.height()):
            right_colors[i] = img.pixel(-1, i)
        
        return left_colors, right_colors
    

def gen_qmap(left_colors, right_colors, geom):
    # start_time = timeit.default_timer()
    
    if left_colors is None or right_colors is None:
        return None
        
    pixels = np.linspace(left_colors, right_colors, geom.width(), axis=0).astype(dtype=np.uint8).transpose(1, 0, 2)
    image = Image.fromarray(pixels)
    qmap = QImage(image.tobytes(), image.width, image.height, QImage.Format.Format_RGB888)
    
    return qmap


class FauxTaskbar(QLabel):
    colors_grabbed = pyqtSignal(object, object)
    
    def start_color_grabber(self):
        if not get_path_lock.tryLock():
            return
        if self.updateMutex.tryLock():
            self.color_grabber.start()
        else:
            self.updateMutex.unlock()
        
    def __init__(self, parent=None, geometry_reference=None):
        super().__init__("", parent)
        self._blending = None
        self.geometry_reference = geometry_reference
        self.blending = None
        self.color_grabber = ColorGrabberThread(self.geometry_reference, parent=self)
        self.colors_grabbed.connect(self.update_faux_taskbar)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_color_grabber)
        
        self.timer.start(100)
        self.updateMutex = QMutex()
        # self.update_signal.connect(self.update_faux_taskbar)
        
    
    def update_faux_taskbar(self, left_colors, right_colors):
        new_gen = gen_qmap(left_colors, right_colors, self.geometry_reference.geometry())
        if new_gen is not None:
            self.blending = new_gen
            self.update()
            
    def setHidden(self, hidden):
        if hidden:
            self.timer.stop()
        else:
            self.timer.start()
        super().setHidden(hidden)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.blending is not None:
            painter.drawImage(0, 0, self.blending)

