from datetime import datetime
from PyQt5.QtCore import QMutex, QObject, QTimer
import os

from ..utils.dataclasses import PlayingStatusTrigger

from ..globalvariables import GLOBAL_OFFSET, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI



os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIPY_REDIRECT_URI

# if HTTP_PROXY and HTTP_PROXY != "":
#     os.environ["http_proxy"] = HTTP_PROXY
#     os.environ["HTTP_PROXY"] = HTTP_PROXY
# if HTTPS_PROXY and HTTPS_PROXY != "":
#     os.environ["https_proxy"] = HTTPS_PROXY
#     os.environ["HTTPS_PROXY"] = HTTPS_PROXY


class NowPlaying(QObject):
    def __init__(self, sync_interval=60000, update_callback=None):
        super().__init__()
        self.registered_callbacks = set()
        if update_callback is not None:
            self.registered_callbacks.add(update_callback)
        self.playing_info = None
        self.sync_mutex = QMutex()
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync)
        self.sync_interval = sync_interval
        self.started = False
        
        self._global_offset = GLOBAL_OFFSET

    def start_loop(self):
        self.started = True
        if self.sync_interval > 0:
            self.sync_timer.start(self.sync_interval)

    def sync(self):
        pass
    
    def register_callback(self, callback):
        self.registered_callbacks.add(callback)
        if not self.started:
            return
        if self.playing_info is not None and self.playing_info.is_playing:
            callback(PlayingStatusTrigger.NEW_TRACK)
        else:
            callback(PlayingStatusTrigger.PAUSE)
            
    def activate(self, callback=None):
        if callback is not None:
            if self.playing_info is not None and self.playing_info.is_playing:
                callback(PlayingStatusTrigger.NEW_TRACK)
            else:
                callback(PlayingStatusTrigger.PAUSE)
            return
        for callback in self.registered_callbacks:
            if self.playing_info is not None and self.playing_info.is_playing:
                callback(PlayingStatusTrigger.NEW_TRACK)
            else:
                callback(PlayingStatusTrigger.PAUSE)
    
    def unregister_callback(self, callback):
        self.registered_callbacks.remove(callback)
        
    def update_callback(self, trigger):
        for callback in self.registered_callbacks:
            callback(trigger)
            
    @property
    def global_offset(self):
        return self._global_offset
    
    @global_offset.setter
    def global_offset(self, value):
        print("GLOBAL OFFSET UPDATED: ", value)
        self._global_offset = value
            
    @property
    def progress(self):
        if not self.is_playing:
            return -1
        if not self.current_begin_time:
            return -1
        return (datetime.now().timestamp()*1000 - self.current_begin_time)
    
    @property
    def percent(self):
        if not self.is_playing:
            return -1
        if not self.current_track_length:
            return -1
        return self.progress / self.current_track_length

    @property
    def is_playing(self):
        return self.playing_info.is_playing if self.playing_info is not None else False

    @property
    def current_track(self):
        return self.playing_info.current_track if self.playing_info is not None else None
    
    @property
    def current_track_id(self):
        return (
            self.playing_info.current_track_id
            if self.playing_info is not None
            else None
        )

    @property
    def current_track_artist(self):
        return (
            self.playing_info.current_track_artist
            if self.playing_info is not None
            else None
        )

    @property
    def current_track_title(self):
        return (
            self.playing_info.current_track_title
            if self.playing_info is not None
            else None
        )

    @property
    def current_track_length(self):
        return (
            self.playing_info.current_track_length
            if self.playing_info is not None
            else None
        )

    @property
    def current_begin_time(self):
        return (
            self.playing_info.current_begin_time + self.global_offset
            if self.playing_info is not None
            else None
        )

    @property
    def last_updated_time(self):
        return self.playing_info.last_updated_time if self.playing_info is not None else None

    @property
    def has_lyrics(self):
        return self.playing_info.has_lyrics if self.playing_info is not None else False

    @has_lyrics.setter
    def has_lyrics(self, value):
        self.playing_info.has_lyrics = value











