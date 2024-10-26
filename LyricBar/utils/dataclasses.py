from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Optional


class PlayingStatusTrigger(Enum):
    PAUSE = 1
    RESUME = 2
    NEW_TRACK = 3
    

@dataclass
class TrackInfo:
    artist: str = None
    id: str = None
    title: str = None
    length: int = None
    _hash: str = None

    def __str__(self):
        return f"{self.artist} - {self.title} [{self.id}] ({self.length})"

    def __eq__(self, value: "TrackInfo") -> bool:
        if self.id is not None and value.id is not None:
            return self.id == value.id
        if (
            self.artist is not None
            and value.artist is not None
            and self.title is not None
            and value.title is not None
        ):
            return self.artist == value.artist and self.title == value.title
        return False

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def get_hash(self):
        h = hashlib.new('sha256')
        h.update(f'{self.artist} - {self.title}'.encode())
        return h.hexdigest()

    @property
    def hash_id(self):
        if self._hash is None:
            self._hash = self.get_hash()
        return self._hash

@dataclass
class PlayingInfo:
    current_track: TrackInfo
    current_begin_time: int
    is_playing: bool
    last_updated_time: Optional[int] = None
    has_lyrics: bool = True

    @property
    def current_track_artist(self):
        return self.current_track.artist

    @current_track_artist.setter
    def current_track_artist(self, value):
        self.current_track.artist = value

    @property
    def current_track_id(self):
        return self.current_track.id

    @current_track_id.setter
    def current_track_id(self, value):
        self.current_track.id = value

    @property
    def current_track_title(self):
        return self.current_track.title

    @current_track_title.setter
    def current_track_title(self, value):
        self.current_track.title = value

    @property
    def current_track_length(self):
        return self.current_track.length

    @current_track_length.setter
    def current_track_length(self, value):
        self.current_track.length = value

