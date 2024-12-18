import logging
import sys
from PyQt5.QtCore import QPropertyAnimation, Qt, QTimer, QCoreApplication, pyqtSignal, QMutex, QEvent
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

from .components.lyriclabel import LyricLabel

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
        
        self.label = LyricLabel(self.width(), self.height(), None, parent=self.frame)
        
        self.setGeometry()        
        # self.windowHandle().screenChanged.connect(self.setGeometry)

        self.show()
        
        self.setMouseTracking(True)
        
        self.displaying_line = None
        self.displaying_begin_time = None
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
        self.toaster.setGeometry(self.width() // 3, 0, (self.height() + 10) * 2, (self.height() + 10))
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
            self.label.use_scale = False
            self.lyric_maintainer.pause()
            self.sst_maintainer.start()
        else:
            self.line_mode = 0
            self.toast("Switching to Lyrics Mode")
            self.label.right_pad = False
            self.label.use_scale = True
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
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def copyLyricsToClipboard(self):
        clipboard = QApplication.clipboard()
        print("COPYING TO CLIPBOARD")
        clipboard.setText(self.line_provider.line.text)
        
    def windowConfig(self):
        
        self.setAcceptDrops(False)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.X11BypassWindowManagerHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool) # | Qt.WindowTransparentForInput)
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
        self.label.setStyle(**style)
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
            # pass
        except:
            pass
        line = self.line_provider.line
        begin_time = None if (line is None or line.begin_time <= 0) else line.begin_time
        if line:
            if (line == self.displaying_line and line.text == self.displaying_line.text) and begin_time == self.displaying_begin_time:
                return
            text = line.text
            anim = True
            formatted = self.formatter(text)
            if line.timestamp == -2:
                formatted = "♬"
            elif line.timestamp == -3:
                formatted = "🔄"
                anim = False
            elif line.timestamp == -4:
                formatted = "👂"
            elif line.timestamp == 0:
                if self.line_mode == 0:
                    formatted = "♬"
                else:
                    formatted = "👂" if line.text == "" else line.text
            self.label.setText(formatted, anim and self.line_mode == 0, duration=line.end_timestamp-line.timestamp if (line.end_timestamp is not None and line.end_timestamp != -1) else None, start_time=begin_time)
            self.displaying_line = line
            self.displaying_begin_time = begin_time
            return
        self.displaying_line = None
        if self.label.text() != "⏸":
            self.label.setText("⏸", False)
        return
        
    def updateProgress(self):
        if self.bar_hidden:
            return
        self.label.setProgress(self.now_playing.percent)

        
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
            self.label.setHidden(True)
        else:
            print("UNHIDING")
            self.label.setHidden(False)
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
            if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier == Qt.KeyboardModifier.ShiftModifier:
                self.switch_mode()
            else:
                self.line_provider.get_from_next_source()
                self.toast("Searching from Next Source")
        elif e.button() == Qt.MouseButton.MiddleButton:
            if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier == Qt.KeyboardModifier.ShiftModifier:
                self.line_provider.set_empty_lyrics()        
                self.toast("Lyrics Cleared")
            else:
                self.line_provider.track_offset = 0
                self.toast("Track Offset Reset")
    
    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key.Key_Space:
    #         self.switch_mode()
    
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
            
    def eventFilter(self, object, e):
        if e.type() == QEvent.Type.MouseMove:
            if self.geometry().contains(QCursor.pos()):
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
