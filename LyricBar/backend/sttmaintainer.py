import logging
from vosk import Model, KaldiRecognizer
import pyaudio
from PyQt5.QtCore import pyqtSignal, QMutex, QObject, QThread

from ..utils.dataclasses import PlayingStatusTrigger
from ..globalvariables import STT_MODEL_PATH, STT_TRACKING_INPUT
from ..backend.lyricmanager import LyricLine
from datetime import datetime


class STTThread(QThread):
    def __init__(self, model, recognizer, stream):
        super().__init__()
        self.model = model
        self.recognizer = recognizer
        self.stream = stream
        
        self.cancelled = False
        self.text = ""
        self.timestamp = -4
        
        self.update_time = True
        
    def cancel(self):
        self.cancelled = True
    
    def gracefully_out(self):
        self.deleteLater()
        
    def format_text(self, text, length=10):
        words = text.split()
        # if len(words) % 15 > 5:
        # text = " ".join(words[len(words)//15*15:])
        # text = " ".join(words[-15:])
        # if len(words) % length > 0:
        #     text = " ".join(words[len(words)//length*length:])
        # else:
        #     text = " ".join(words[(len(words)//length - 1)*length:])
        if text == "":
            return "👂"
        return " ".join(words[-length:]) + " ___"
        # return " ".join(words[(len(words)//15-1)*15:])
        
        
    def run(self):
        self.stream.start_stream()
        while not self.cancelled:
            if self.update_time:
                # self.timestamp = datetime.now().timestamp()
                self.timestamp = 0
                self.update_time = False
            try:
                data = self.stream.read(10000, exception_on_overflow=False)
                text = self.recognizer.PartialResult()[17:-3]
                if text.strip() != "":
                    # print(text, end="\t")
                    self.text = self.format_text(text)
                    # print(self.text)
                self.recognizer.AcceptWaveform(data)
                # if self.recognizer.AcceptWaveform(data):
                #     # pass
                #     text = self.recognizer.Result()
                #     self.update_time = True
            except:
                pass
        self.stream.stop_stream()
        if self.recognizer.PartialResult()[17:-3].strip() != "":
            self.recognizer.AcceptWaveform(b"")
            self.recognizer.Reset()
        # except Exception as e:
        #     print(e)
        self.gracefully_out()
    
        
class STTMaintainer(QObject):
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    def __init__(self, now_playing, update_callback=None):
        super().__init__()
        
        self.update_callback = update_callback
        
        self.now_playing = now_playing
        
        self.callback_mutex = QMutex()
        self.caption_mutex = QMutex()
        
        self.now_playing = now_playing
        self.now_playing.register_callback(self.manager_callback)
            
        self.current_line = None
        
        self.model = None
        self.recognizer = None
        try:
            self.model = Model(STT_MODEL_PATH)
            self.recognizer = KaldiRecognizer(self.model, 16000)
        except:
            print("Failed to load STT model")
        
        mic = pyaudio.PyAudio()

        self.stream = None
        device_index = None
        
        for i in range(0, mic.get_device_count()):
            if STT_TRACKING_INPUT in mic.get_device_info_by_index(i)['name']:
                device_index = i
                break
        if device_index is None or STT_TRACKING_INPUT == "":
            print("Failed to find System Loopback device")
        else:
            print(f"Found System Loopback device {STT_TRACKING_INPUT} at index {device_index}")
            self.stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192, input_device_index=device_index)
            
        self.start_signal.connect(self.start_listen)
        self.stop_signal.connect(self.stop_listen)
        
        self.running = False
        self.running_mutex = QMutex()
        
        # self.line = LyricLine(-2, "♬")
        
        self.stt_thread = None
        
        self.stopped = False
        
    def start(self):
        if self.model is None or self.recognizer is None or self.stream is None:
            return
        self.stopped = False
        self.now_playing.activate(self.manager_callback)
        
    def pause(self):
        if self.stopped:
            return
        self.stopped = True
        self.stop_signal.emit()
        
    @property
    def line(self):
        if not self.running_mutex.tryLock(0):
            return LyricLine(-4, "👂")
        if not self.running:
            self.running_mutex.unlock()
            return LyricLine(-4, "👂")
        if not self.stt_thread:
            self.running_mutex.unlock()
            return LyricLine(-4, "👂")
        l = LyricLine(self.stt_thread.timestamp, self.stt_thread.text)
        self.running_mutex.unlock()
        return l
        
    def start_listen(self):
        if not self.running_mutex.tryLock(1000):
            return
        if self.running or self.stopped:
            self.running_mutex.unlock()
            return
        print("Starting STT")
        self.running = True
        if self.stt_thread is not None:
            try:
                self.stt_thread.cancel()
            except:
                pass
        
        self.stt_thread = STTThread(self.model, self.recognizer, self.stream)
        self.stt_thread.start()
        self.running_mutex.unlock()
        
    def stop_listen(self):
        if not self.running_mutex.tryLock(1000):
            return
        if not self.running:
            self.running_mutex.unlock()
            return
        print("Stopping STT")
        self.running = False
        self.stt_thread.cancel()
        # self.line = LyricLine(-2, "♬")
        self.running = False
        self.running_mutex.unlock()
        
        
    def next_source(self):
        pass
    
    def manager_callback(self, value):
        if self.stopped:
            return
        if not self.callback_mutex.tryLock(0):
            return
        if value == PlayingStatusTrigger.NEW_TRACK:
            self.start_signal.emit()
        elif value == PlayingStatusTrigger.PAUSE:
            self.stop_signal.emit()
        elif value == PlayingStatusTrigger.RESUME:
            self.start_signal.emit()
        self.callback_mutex.unlock()
        return
    
    def get_from_next_source(self):
        pass
    
    def set_empty(self):
        pass
    
    
    @property
    def track_offset(self):
        return 0
    
    @track_offset.setter
    def track_offset(self, value):
        pass

        
    