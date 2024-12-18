import logging
import sys
from PyQt5.QtCore import QPropertyAnimation, Qt, QTimer, QCoreApplication, pyqtSignal, QMutex
from PyQt5.QtGui import QColor, QCursor, QKeyEvent, QPixmap, QBrush, QPen, QGuiApplication, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QLabel,
    QWidget,
    QMenu,
    QSystemTrayIcon
)

from ..themes import STYLES, get_style


from .components.toasttag import ToastTag

from .components.progressbar import ProgressBar

from .components.pad import Pad
from .components.utils import convert_to_color

from ..globalvariables import PLAYING_INFO_PROVIDER, TAKSBAR_HEIGHT, LEFTOUT_WIDTH, SPICETIFY_PORT
from .components.outlinedlabel import OutlinedLabel
from ..backend.lyricsmaintainer import LyricsMaintainer
from ..backend.sttmaintainer import STTMaintainer
from ..nowplaying import NowPlayingSpicetify, NowPlayingSystem


from .components.fauxtaskbar import FauxTaskbar
from ..utils.dataclasses import PlayingStatusTrigger
# from windows_toasts import Toast, ToastDuration, WindowsToaster

# def _start(self, time): 
#     print(self.objectName(), f"start {time}") 
#     print(self.objectName(), f"started {time}")
# QTimer.start = _start

class FakeQMutex(QMutex):
    def tryLock(self, timeout=0):
        return True
    def unlock(self):
        pass

class LyricsDisplay(QWidget):
    toast_signal = pyqtSignal(str, int)
    hide_later_signal = pyqtSignal()
    cancel_hide_signal = pyqtSignal()
    callback_signal = pyqtSignal(object)
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.windowConfig()
        
        self.frame = QFrame(self)
        
        self.faux_taskbar = FauxTaskbar(self.frame, geometry_reference=self)
        
        self.pad = Pad(convert_to_color("rgba(0, 0, 0, 0)"), parent=self.frame)
        
        self.imagepad = QLabel("", parent=self.frame)
        self.imagepad.setStyleSheet("background-color: transparent")
        
        self.label = OutlinedLabel("- LyricBar -", parent=self.frame, linewidth=0, relative_outline=False, brushcolor=QColor(138, 206, 0, 255), linecolor=QColor(255, 255, 255, 100))
        
        self.progress = ProgressBar(parent=self.frame)
        
        # self.left_timer = QLabel("00:00", parent=self.frame)
        # self.right_timer = QLabel("00:00", parent=self.frame)
        # self.progress.setGeometry((self.width() - 400) // 2, -10, 400, 16)
        glow = QGraphicsDropShadowEffect()
        glow.setColor(QColor(0, 0, 0, 200))
        glow.setBlurRadius(15)
        glow.setOffset(0, 0)
        self.progress.setGraphicsEffect(glow)
        
        self.setGeometry()
        
        # self.windowHandle().screenChanged.connect(self.setGeometry)

        self.show()
        
        self.setMouseTracking(True)
        
        self.displaying_line = None
        self.bar_hidden = False
        self.paused = False
        
        self._drag_active = False
        
        self.style_name = "default"
        self.formatter = lambda x: x
        
        self.reappear_timer = QTimer(self)
        self.reappear_timer.setSingleShot(True)
        self.reappear_timer.timeout.connect(self.reappear)
        
        self.entering = None  
        self.sustain = None
        self.toaster = ToastTag(parent=self.frame)
        self.toaster.setGeometry(self.width() // 3, 0, (self.height() + 5) * 2, (self.height() + 5))
        self.toast_signal.connect(self.toaster.start)
        
        self.callback_signal.connect(self.maintainer_callback)
        
        if PLAYING_INFO_PROVIDER == "Spicetify":
            self.now_playing = NowPlayingSpicetify(socket_port=SPICETIFY_PORT, update_callback=self.callback_signal.emit, offset=120)
        else:
            self.now_playing = NowPlayingSystem(update_callback=self.callback_signal.emit, sync_interval=25, offset=0)
        
        self.line_mode = 0
        self.lyric_maintainer = LyricsMaintainer(self.now_playing, self.callback_signal.emit)
        
        self.sst_maintainer = STTMaintainer(self.now_playing, self.callback_signal.emit)
        self.sst_maintainer.pause()
        
        
        self.timer = QTimer(self)
        self.update_mutex = QMutex()
        self.style_mutex = QMutex()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(50)
        
        self.taskbar_repaint_timer = QTimer(self)
        self.taskbar_repaint_timer.timeout.connect(self.updateTaskbar)
        self.taskbar_repaint_timer.start(20000)
              
        self.hide_later_timer = QTimer(self)
        self.hide_later_timer.setSingleShot(True)
        self.hide_later_timer.timeout.connect(lambda: self.setHidden(True))
        
        self.now_playing.start_loop()

        self.hide_later_signal.connect(lambda: self.hide_later_timer.start(1000))
        self.cancel_hide_signal.connect(lambda: self.hide_later_timer.stop() if self.hide_later_timer.isActive() else None)
                
        self.setHidden(True)
        self.toast("Welcome To LyricBar", duration=4000)
        
    @property
    def line_provider(self):
        if self.line_mode == 0:
            return self.lyric_maintainer
        return self.sst_maintainer
    
    def switch_mode(self):
        print("SWITCHING MODE")
        if self.line_mode == 0:
            self.line_mode = 1
            self.toast("Switching to STT Mode")
            self.label.right_pad = True
            self.lyric_maintainer.pause()
            self.sst_maintainer.start()
        else:
            self.line_mode = 0
            self.toast("Switching to Lyrics Mode")
            self.label.right_pad = False
            self.lyric_maintainer.start()
            self.sst_maintainer.pause()
    
    def set_stt_mode(self):
        if self.line_mode == 0:
            self.switch_mode()
            
    def set_lyrics_mode(self):
        if self.line_mode == 1:
            self.switch_mode()
    
    def setGeometry(self):
        self.faux_taskbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.faux_taskbar.setGeometry(0, 0, self.width(), self.height())
        
        self.pad.setGeometry(0, 0, self.width(), self.height())
        self.pad.setStyleSheet("background-color: transparent")
        
        self.imagepad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imagepad.setGeometry(0, 0, self.width(), self.height())
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.label.setGeometry(0, 0, self.width(), self.height())
        
        self.progress.setGeometry((self.width() - 400) // 2, self.height() - 10, 400, 8)
        
        # self.left_timer.setGeometry((self.width() - 400) // 2 - 60, 0, 60, 16)
        # self.right_timer.setGeometry((self.width() + 400) // 2, 0, 60, 16)
        
    def copyLyricsToClipboard(self):
        clipboard = QApplication.clipboard()
        print("COPYING TO CLIPBOARD")
        clipboard.setText(self.line_provider.line.text)
        
    def windowConfig(self):
        
        self.setAcceptDrops(False)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool) # | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(self.screen_width - 2 * LEFTOUT_WIDTH, TAKSBAR_HEIGHT - 1)
        widget = self.geometry()
        x = (self.screen_width - widget.width()) // 2
        y = self.screen_height - TAKSBAR_HEIGHT + 1
        self.move(x, y)

    def updateStyle(self, style):
        if not self.style_mutex.tryLock(5000):
            return
        print("UPDATING STYLE")
        if style["name"] == self.style_name:
            self.style_mutex.unlock()
            return
        if "font-image" in style:
            self.label.setBrush(QPixmap(style["font-image"]))
        else:
            self.label.setBrush(QBrush(convert_to_color(style["font-color"])))
        self.label.setPen(QPen(convert_to_color(style["line-color"])))
        self.label.setOutlineThickness(style["line-width"])
        self.label.font_size = int(style['font-size'].replace("px", ""))
        self.label.font_family = style['font-family']
        if style['font-weight'] == "light":
            self.label.font_weight = 25
        elif style['font-weight'] == "normal":
            self.label.font_weight = 50
        elif style['font-weight'] == "demibold":
            self.label.font_weight = 63
        elif style['font-weight'] == "bold":
            self.label.font_weight = 75
        elif style['font-weight'] == "black":
            self.label.font_weight = 87
        self.label.font_italic = style['font-italic']
        self.label.flip = style["flip-text"]
        self.label.opacity = 1
        self.label.scale = 1
        self.label.setGraphicsEffect(None)
        if style["use-shadow"]:
            glow = QGraphicsDropShadowEffect()
            glow.setColor(QColor(*style["shadow-color"]) if isinstance(style["shadow-color"], tuple) else QColor(style["shadow-color"]))
            glow.setOffset(style["shadow-offset"][0], style["shadow-offset"][1])
            glow.setBlurRadius(style["shadow-radius"])
            self.label.setGraphicsEffect(glow)
        if "progress-color" not in style:
            if "font-image" in style:
                self.progress.progress_color = QPixmap(style["font-image"])
            else:
                self.progress.progress_color = convert_to_color(style["font-color"])
            # if isinstance(self.progress.progress_color, QColor):
            #     self.progress.progress_color.setAlpha(255)
        else:
            self.progress.progress_color = convert_to_color(style["progress-color"])
        if "progress-line-color" not in style and style["line-width"] != 0:
            self.progress.line_color = convert_to_color(style["line-color"])
        else:
            self.progress.line_color = QColor(0, 0, 0, 0)
        
        self.pad.setColor(convert_to_color(style["background-color"], width=self.width(), height=self.height()))
        
        if "background-image"  in style:
            image = QPixmap(style["background-image"])
            image = image.scaled(1, self.pad.height(), Qt.KeepAspectRatioByExpanding)
            self.imagepad.setPixmap(image)
        else:
            self.imagepad.setPixmap(QPixmap())
        if style["entering"] == "fadein":
            self.entering = QPropertyAnimation(self.label, b"opacity")
            self.entering.setDuration(200)
            self.entering.setStartValue(0.01)
            self.entering.setEndValue(1.0)
        elif style["entering"] == "zoomin":
            self.entering = QPropertyAnimation(self.label, b"scale")
            self.entering.setDuration(200)
            self.entering.setStartValue(0.1)
            self.entering.setEndValue(1)
        elif style["entering"] == "zoomin_overscale":
            self.entering = QPropertyAnimation(self.label, b"scale")
            self.entering.setDuration(200)
            self.entering.setStartValue(0.1)
            self.entering.setKeyValueAt(0.6, 1.5)
            self.entering.setEndValue(1)
        else:
            self.entering = None
        # if self.entering is not None:
        #     self.entering.finished.connect(self.sustaining_animation)
        # self.sustain = QPropertyAnimation(self.label, b"geometry")
        # self.sustain.setDuration(1000)
        # self.sustain.setLoopCount(1)
        # base = QRect(self.geometry())
        # self.sustain.setStartValue(base)
        # self.sustain.setKeyValues([(0.1, base.adjust(-1, 2, 0, 0)), (0.4, base.adjust(2, 4, 0, 0)), (0.9, base.adjust(3, 6, 0, 0)), (1, base.adjust(-2, -3, 0, 0))])
        # self.sustain.setEndValue(base)
        self.style_name = style["name"]
        self.formatter = style["format"]
        self.style_mutex.unlock()
        return 
    
    def maintainer_callback(self, value):
        if value == PlayingStatusTrigger.PAUSE:
            self.paused = True
            print("!!PAUSING", self.now_playing.current_track)
            self.hide_later_signal.emit()
        elif value == PlayingStatusTrigger.RESUME:
            self.paused = False
            print("!!RESUMING", self.now_playing.current_track)
            self.setHidden(False)
        elif value == PlayingStatusTrigger.NEW_TRACK:
            self.paused = False
            print("!!NEW TRACK", self.now_playing.current_track)
            if self.now_playing.current_track.is_music:
                self.set_lyrics_mode()
            else:
                self.set_stt_mode()
            self.updateStyle(get_style(self.now_playing.current_track))
            self.setHidden(False)
        elif isinstance(value, str):
            self.toast_signal.emit(value, 2000)
    
    def sustaining_animation(self):
        if self.sustain.state() == QPropertyAnimation.State.Running:
            return
        print("SUSTAINING")
        self.sustain.start()
    
    def entering_animation(self):
        if self.entering is None:
            return
        if self.sustain is not None and self.sustain.state() == QPropertyAnimation.State.Running:
            print("STOP SUSTAINING")
            self.sustain.stop()
        if self.entering.state() == QPropertyAnimation.State.Running:
            self.entering.stop()
        self.entering.start()
        
    def updateLyrics(self, anim=True):
        try:
            self.raise_()
        except:
            pass
        line = self.line_provider.line
        # if self.lyric_maintainer.style and self.lyric_maintainer.style != self.style_name:
        #     self.updateStyle()
        # print("UPDATING LYRICS", line)
        if line:
            text = line.text
            formatted = self.formatter(text)
            if line.timestamp == -2:
                formatted = "♬"
                anim = False
            elif line.timestamp == -3:
                formatted = "🔄"
                anim = False
            elif line.timestamp == -4:
                formatted = "👂"
                anim = False
            if formatted != self.label.text():
                self.label.setText(formatted)
            if line != self.displaying_line and text != "" and anim:
                self.entering_animation()
            self.displaying_line = line
            return
        self.displaying_line = None
        self.label.setText("⏸")
        return
        
    def updateProgress(self):
        if self.bar_hidden:
            return
        self.progress.progress = self.now_playing.percent
        # self.left_timer.setText(ms_to_mm_ss(self.lyric_maintainer.progress))
        # self.right_timer.setText(ms_to_mm_ss(self.lyric_maintainer.now_playing.current_track_length))
        self.progress.update()
        
    def updateTaskbar(self):
        if self.bar_hidden:
            return
        self.faux_taskbar.update_taskbar()
    
    def update_info(self):
        self.updateLyrics()
        self.updateProgress()
        
    def setHidden(self, hidden):
        if not hidden:
            self.cancel_hide_signal.emit()
        self.bar_hidden = hidden
        if hidden:
            print("HIDING")
            self.faux_taskbar.setHidden(True)
            self.pad.setHidden(True)
            self.imagepad.setHidden(True)
            self.progress.setHidden(True)
            self.label.setHidden(True)
        else:
            print("UNHIDING")
            self.label.setHidden(False)
            self.progress.setHidden(False)
            self.pad.setHidden(False)
            self.imagepad.setHidden(False)
            self.faux_taskbar.setHidden(False)
        

    def reappear(self):
        if self.paused:
            return
        if self.geometry().contains(QCursor.pos()):
            self.reappear_timer.start(200)
            return
        self.setHidden(False)
        
    def enterEvent(self, e):
        if self.bar_hidden:
            return
        if QApplication.queryKeyboardModifiers() & Qt.KeyboardModifier.ControlModifier == Qt.KeyboardModifier.ControlModifier:
            return
        self.bar_hidden = True   
        self.setHidden(True)
        self.reappear_timer.start(200)
        
    def toast(self, text, duration=1000):
        self.toaster.start(text, duration)
        
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.copyLyricsToClipboard()
            self.toast("Lyrics Copied to Clipboard")
        elif e.button() == Qt.MouseButton.RightButton:
            self.line_provider.get_from_next_source()
            self.toast("Searching from Next Source")
        elif e.button() == Qt.MouseButton.MiddleButton:
            if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier == Qt.KeyboardModifier.ShiftModifier:
                self.line_provider.set_empty_lyrics()        
                self.toast("Lyrics Cleared")
            else:
                self.line_provider.track_offset = 0
                self.toast("Track Offset Reset")
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Space:
            self.switch_mode()
    
    def setCenter(self, widget):
        widget.move((self.width() - widget.width()) // 2, (self.height() - widget.height()) // 2)
            
    def wheelEvent(self, e):
        QModifiers = QApplication.keyboardModifiers()
        if QModifiers & Qt.KeyboardModifier.ShiftModifier == Qt.KeyboardModifier.ShiftModifier:
            self.line_provider.global_offset += e.angleDelta().y()
            self.toast("Global Offset:\n" + str(self.line_provider.global_offset))
        else:
            self.line_provider.track_offset += e.angleDelta().y()
            self.toast("Track Offset:\n" + str(self.line_provider.track_offset))
            
    def dragEnterEvent(self, e):
        print("DRAG ENTER")
        self.enterEvent(e)

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)

    def exit(self):
        QCoreApplication.exit()

def main():

    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    ui = LyricsDisplay(app.primaryScreen().size().width(), app.primaryScreen().size().height())
    trayIcon = SystemTrayIcon(QIcon("resources/icon.ico"))
    trayIcon.show()
    sys.exit(app.exec())
