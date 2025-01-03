import logging
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMutex
from ..globalvariables import GLOBAL_OFFSET, PLAYING_INFO_PROVIDER, SP_DC, SPICETIFY_PORT, THIRD_PARTY_LYRICS_PROVIDERS, USE_SPOTIFY_LYRICS
from .lyricmanager import FromSpotify, FromThirdParty, LyricLine, Lyrics, LyricsManager
from ..nowplaying import NowPlayingSystem, NowPlayingSpicetify
from ..utils.dataclasses import PlayingStatusTrigger
from ..themes import STYLES, get_style


# class debugQMutex(QMutex):
#     def tryLock(self, timeout=0):
#         ret = super().tryLock(timeout)
#         print("TRY LOCK: ", ret)
#         return ret
#     def unlock(self):
#         print("UNLOCK")
#         return super().unlock()


class LyricsMaintainer():
    def __init__(self, now_playing, update_callback=None):
        super().__init__()
        
        self.update_callback = update_callback

        # if PLAYING_INFO_PROVIDER == "Spotify":
        #     self.now_playing = NowPlayingSpotify(update_callback=self.update_lyrics)
        # elif PLAYING_INFO_PROVIDER == "System":
        #     self.now_playing = NowPlayingSystem(update_callback=self.update_lyrics)
        # else:
        #     NowPlayingMixed(update_callback=self.update_lyrics)
        
        self.providers = {}
        if USE_SPOTIFY_LYRICS:
            self.providers["Spotify"] = FromSpotify(SP_DC)
        if THIRD_PARTY_LYRICS_PROVIDERS and THIRD_PARTY_LYRICS_PROVIDERS != []:
            for provider in THIRD_PARTY_LYRICS_PROVIDERS:
                self.providers[provider] = FromThirdParty([provider])
        
        self.manager = LyricsManager(providers=self.providers)
        
        
        
        self.lyrics = None
        # self.style = STYLES["default"]
        # self.style["name"] = "default"
        
        self.callback_mutex = QMutex()
        self.lyrics_mutex = QMutex()
        
        self.now_playing = now_playing
        self.now_playing.register_callback(self.manager_callback)
            
        self.current_line = None
        
        self.stopped = False
        
    # def start(self):
    #     self.now_playing.start_loop()
    
    def start(self):
        self.stopped = False
        self.now_playing.activate(self.manager_callback)
    
    def pause(self):
        self.stopped = True
        self.lyrics = None
    
    @property
    def line(self):
        # # print(self.now_playing.__dict__)
        # print("has lyrics?", self.now_playing.has_lyrics)
        if not self.lyrics_mutex.tryLock(0):
            return LyricLine(-3, "🔄")
        if not self.now_playing.has_lyrics:
            self.lyrics_mutex.unlock()
            return LyricLine(-2, "♬")
        if not self.lyrics and self.now_playing.has_lyrics:
            self.lyrics_mutex.unlock()
            return LyricLine(-3, "🔄")
        if not self.lyrics:
            self.lyrics_mutex.unlock()
            return LyricLine(-2, "♬")
        if not self.now_playing.is_playing:
            self.lyrics_mutex.unlock()
            return None
        if not self.now_playing.current_begin_time:
            self.lyrics_mutex.unlock()
            return None
        l = self.lyrics.get_line_with_timestamp(self.now_playing.progress)
        if l:
            self.current_line = l
            l.end_timestamp = self.lyrics.lines[l.index + 1].timestamp if l.index < len(self.lyrics.lines) - 1 else -1
            l = self.lyrics.get_real_time(l)
            l.begin_time = self.now_playing.current_begin_time + l.timestamp
            self.lyrics_mutex.unlock()
            return l
        self.lyrics_mutex.unlock()
        return LyricLine(-2, "♬")
    
    def manager_callback(self, value):
        if self.stopped:
            return
        if not self.callback_mutex.tryLock(0):
            # print("UPDATING SKIPPED")
            return
        if value == PlayingStatusTrigger.NEW_TRACK:
            self.lyrics = None
            if self.now_playing.current_track.artist == "" or self.now_playing.current_track.title == "":
                self.callback_mutex.unlock()
                return
            # if self.update_callback is not None:
            #     self.update_callback(value)
            self.manager.get_lyrics(self.now_playing.current_track, lambda x: self.set_lyrics(*x))
            self.callback_mutex.unlock()
            return
        # if self.update_callback is not None:
        #     self.update_callback(value)
        self.callback_mutex.unlock()
        return
        
    def next_source(self):
        self.now_playing.has_lyrics = True
        if not self.now_playing.is_playing:
            return
        current_source = self.lyrics.source if self.lyrics else None
        next_source = None
        if current_source is None:
            next_source = list(self.providers.keys())
        else:
            current_idx = list(self.providers.keys()).index(current_source)
            next_source = list(self.providers.keys())
            next_source = next_source[(current_idx + 1) % len(self.providers):] + next_source[:(current_idx + 1) % len(self.providers)]
        return next_source
    
    def get_from_next_source(self):
        next_source = self.next_source()
        self.manager.get_lyrics(self.now_playing.current_track, lambda x: self.set_lyrics(*x, check_first=True), source=next_source)
        
    def set_empty_lyrics(self):
        self.lyrics = Lyrics([])
        self.lyrics.track = self.now_playing.current_track
        self.now_playing.has_lyrics = True
        self.manager.save_lyrics(self.now_playing.current_track, self.lyrics)
    
    @property
    def track_offset(self):
        if not self.now_playing.has_lyrics:
            return 0
        return self.lyrics.offset
    
    @track_offset.setter
    def track_offset(self, value):
        if not self.lyrics_mutex.tryLock(0):
            return
        if not self.now_playing.has_lyrics:
            self.lyrics_mutex.unlock()
            return
        self.lyrics.offset = value
        # print("LYRIC OFFSET UPDATED: ", self.lyrics.offset)
        self.manager.save_lyrics(self.lyrics.track, self.lyrics)
        self.lyrics_mutex.unlock()

    
    def set_lyrics(self, value, track=None, check_first=False):
        if check_first and not value:
            return
        if track is not None:
            if self.now_playing.current_track != track:
                return
        self.lyrics_mutex.lock()
        self.lyrics = value
        if not self.lyrics:
            logging.info("LYRICS NOT FOUND")
            self.now_playing.has_lyrics = False
        else:
            self.now_playing.has_lyrics = True
            if self.lyrics.source:
                self.update_callback("Lyrics from " + self.lyrics.source)
        self.lyrics_mutex.unlock()
        # print("SET LYRICS: ", self.now_playing.current_track, self.lyrics is not None)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    lm = LyricsMaintainer()
    breakpoint()
    sys.exit(app.exec_())