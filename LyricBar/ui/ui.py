import logging
import sys
from PyQt5.QtCore import QPropertyAnimation, Qt, QTimer, QCoreApplication, pyqtSignal, QMutex, QEvent
from PyQt5.QtGui import QColor, QCursor, QKeyEvent, QPixmap, QBrush, QPen, QGuiApplication, QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QLabel,
    QWidget,
    QMenu,
    QSystemTrayIcon
)


from qframelesswindow.windows.window_effect import WindowsWindowEffect
from qframelesswindow.utils.win32_utils import getSystemAccentColor

from ..themes import get_style, load_themes
from .components.lyriclabel import LyricLabel

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

from ..utils.tools import check_if_windows_locked


class LyricsDisplay(QWidget):
    toast_signal = pyqtSignal(str, int)
    hide_later_signal = pyqtSignal()
    cancel_hide_signal = pyqtSignal()
    callback_signal = pyqtSignal(object)
    def __init__(self, app): #, screen_width, screen_height):
        super().__init__()
        self.app = app
        
        # self.desktop = self.app.screens()
        self.screen_id = 0
        self.app.screenAdded.connect(self.screenAdded)
        self.app.screenRemoved.connect(self.screenRemoved)

        
        self.windowConfig()
        
        self.frame = QFrame(self)
        
        # self.faux_taskbar = FauxTaskbar(self.frame, geometry_reference=self)
        self.faux_taskbar = QLabel(self.frame)
        self.faux_taskbar.setStyleSheet("background-color: rgba(0, 0, 0, 0.01);")
        self.windowsEffect = WindowsWindowEffect(self)
        self.label = LyricLabel(None, parent=self.frame)
        self.toaster = ToastTag(parent=self)
        self.toaster.setHidden(True)
        self.toast_signal.connect(self.toaster.start)
        
        
        self.setPosition()
        self.show()
        self.setMouseTracking(True)
        
        self.displaying_line = None
        self.displaying_begin_time = None
        self.paused = False
        
        self.bar_hidden = False
        # self.app.installEventFilter(self)
        
        self._drag_active = False
        
        self.style_name = "default"
        self.formatter = lambda x: x
        
        self.reappear_timer = QTimer(self)
        self.reappear_timer.setSingleShot(True)
        self.reappear_timer.timeout.connect(self.reappear)
        
        self.hide_later_timer = QTimer(self)
        self.hide_later_timer.setSingleShot(True)
        self.hide_later_timer.timeout.connect(lambda: self.setHidden(True))
        
        self.hide_later_signal.connect(lambda: self.hide_later_timer.start(1000))
        self.cancel_hide_signal.connect(lambda: self.hide_later_timer.stop() if self.hide_later_timer.isActive() else None)
    

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
        
        self.now_playing.start_loop()
        self.toast("Welcome to LyricBar", 3000)
        
    @property
    def line_provider(self):
        if self.line_mode == 0:
            return self.lyric_maintainer
        return self.sst_maintainer
    
    @property
    def allowed_to_reappear(self):
        return not ((self.geometry().top() <= QCursor.pos().y() <= self.geometry().bottom()) or check_if_windows_locked() or self.app.screens() == [])
    
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
    
    def applyBackgroundEffect(self):
        self.windowsEffect.setAeroEffect(self.winId())
        # print(getSystemAccentColor().name())
        # self.windowsEffect.setAcrylicEffect(self.winId(), gradientColor="271b43ff", enableShadow=False, animationId=0)
        # self.windowsEffect.enableBlurBehindWindow(self.winId())
    
    def clearBackgroundEffect(self):
        self.windowsEffect.removeBackgroundEffect(self.winId())
        
    def switchDesktop(self, next=True):
        screen_count = len(self.app.screens())
        if screen_count == 0:
            self.setHidden(True)
        elif screen_count > 0 and self.bar_hidden:
            self.setHidden(False)
        self.screen_id = (self.screen_id + (1 if next else 0)) % screen_count
        self.toast(f"Moving to Screen {self.screen_id}")
        self.setPosition()
        
    def screenAdded(self):
        self.switchDesktop(next=False)
    
    def screenRemoved(self):
        self.switchDesktop(next=False)
    
    def toast(self, text, duration=1000):
        self.toaster.start(text, duration)
        
    def copyLyricsToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.line_provider.line.text)
    
    def setPosition(self):
        if self.screen_id >= len(self.app.screens()):
            self.switchDesktop(next=False)
        screen = self.app.screens()[self.screen_id]
        screen_height = screen.geometry().height()
        screen_width = screen.geometry().width()
        screen_top = screen.geometry().top()
        screen_left = screen.geometry().left()
        
        # self.setFixedSize(screen_width - 2 * LEFTOUT_WIDTH, TAKSBAR_HEIGHT - 1)
        width = screen_width - 2 * LEFTOUT_WIDTH
        x = (screen_width - width) // 2
        y = screen_height - TAKSBAR_HEIGHT
        
        
        self.setGeometry(screen_left + x, screen_top + y, screen_width - 2 * LEFTOUT_WIDTH, TAKSBAR_HEIGHT)
        
        self.faux_taskbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.faux_taskbar.setGeometry(0, 0, self.width(), self.height())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedSize(self.width(), self.height())
        self.toaster.setGeometry(self.width() // 3, 0, (self.height() + 10) * 2, (self.height() + 10))

    def windowConfig(self):
        # pass
        self.setAcceptDrops(False)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.X11BypassWindowManagerHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool) # | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # ApplyMica(self.winId(), MicaTheme.DARK, MicaStyle.DEFAULT)
        
    
    def updateStyle(self, style, force_reload=False):
        if not self.style_mutex.tryLock(5000):
            return
        if style["name"] == self.style_name and not force_reload:
            self.style_mutex.unlock()
            return
        self.label.setStyle(**style)
        self.style_name = style["name"]
        self.formatter = style["format"]
        self.displaying_line = None
        # self.label.setText("🔄", False)
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


    def updateLyrics(self, anim=True):
        if self.isHidden():
            return
        try:
            self.raise_()
            # pass
        except:
            pass
        line = self.line_provider.line
        begin_time = None if (line is None or line.begin_time <= 0) else line.begin_time
        if line:
            text = line.text
            anim = True
            formatted = self.formatter(text)
            if (line == self.displaying_line and formatted == self.displaying_line.text) and begin_time == self.displaying_begin_time:
                return
            if line.timestamp == -2:
                formatted = self.formatter("♬")
            elif line.timestamp == -3:
                formatted = self.formatter("🔄")
                anim = False
            elif line.timestamp == -4:
                formatted = self.formatter("👂")
            elif line.timestamp == 0:
                if self.line_mode == 0:
                    formatted = self.formatter("♬")
                else:
                    formatted = self.formatter("👂") if line.text == self.formatter("") else self.formatter(line.text)
            # print("UPDATING LYRICS", formatted)
            self.label.setText(formatted, anim and self.line_mode == 0, duration=line.end_timestamp-line.timestamp if (line.end_timestamp is not None and line.end_timestamp != -1) else None, start_time=begin_time)
            self.displaying_line = line
            self.displaying_line.text = formatted
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
        pass
    
    def update_info(self):
        self.updateLyrics()
        self.updateProgress()
        # self.checkMousePosition()
        
    def setHidden(self, hidden):
        if not hidden:
            self.cancel_hide_signal.emit()
        self.bar_hidden = hidden
        if hidden:
            self.faux_taskbar.setHidden(True)
            self.label.setHidden(True)
            self.reappear_timer.start(100)
            self.clearBackgroundEffect()
        else:
            if not self.allowed_to_reappear:
                self.reappear_timer.start(100)
                return
            self.applyBackgroundEffect()
            self.label.setHidden(False)
            self.faux_taskbar.setHidden(False)
        
    def reappear(self):
        if self.paused:
            return
        self.setHidden(False)
        
        
    def enterEvent(self, e):
        if self.bar_hidden:
            return
        if QApplication.queryKeyboardModifiers() & Qt.KeyboardModifier.ControlModifier == Qt.KeyboardModifier.ControlModifier:
            return
        self.bar_hidden = True   
        self.setHidden(True)
        
    # def checkMousePosition(self):
    #     if (self.geometry().top() <= QCursor.pos().y() <= self.geometry().bottom()):
    #         self.enterEvent(None)
    
    # def eventFilter(self, obj, event):
    #     if not self.bar_hidden and event.type() == QEvent.MouseButtonPress:
    #         self.mousePressEvent(event)
    #     return super().eventFilter(obj, event)
    
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier == Qt.KeyboardModifier.ShiftModifier:
                self.switchDesktop()
            else:
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
        
    def wheelEvent(self, e):
        QModifiers = QApplication.keyboardModifiers()
        if QModifiers & Qt.KeyboardModifier.ShiftModifier == Qt.KeyboardModifier.ShiftModifier:
            self.now_playing.global_offset += e.angleDelta().y()
            self.toast("Global Offset:\n" + str(self.now_playing.global_offset))
        else:
            self.line_provider.track_offset += e.angleDelta().y()
            self.toast("Track Offset:\n" + str(self.line_provider.track_offset))


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        swtichDesktopAction = menu.addAction("Switch Desktop")
        reloadThemeAction = menu.addAction("Reload Themes")
        self.setContextMenu(menu)
        exitAction.triggered.connect(self.exit)
        swtichDesktopAction.triggered.connect(lambda: parent.switch_desktop(True))
        reloadThemeAction.triggered.connect(lambda: [load_themes(), parent.updateStyle(get_style(parent.now_playing.current_track), force_reload=True), parent.toast("Themes Reloaded")])

    def exit(self):
        QCoreApplication.exit()

def main():
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    print("physical", app.primaryScreen().physicalDotsPerInch())
    ui = LyricsDisplay(app)
    trayIcon = SystemTrayIcon(QIcon("resources/icon.ico"), parent=ui)
    trayIcon.show()
    sys.exit(app.exec())
