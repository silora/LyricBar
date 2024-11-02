import logging
import spotipy
import os

from .nowplaying import NowPlaying
from ..utils.dataclasses import PlayingInfo, TrackInfo
from ..globalvariables import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
)


os.environ["SPOTIPY_CLIENT_ID"] = SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = SPOTIPY_REDIRECT_URI


class NowPlayingSpotify(NowPlaying):
    def __init__(self, sync_interval=100000000, update_callback=None):
        super().__init__(sync_interval, update_callback)
        self.scope = "user-read-currently-playing"
        self.spotify_connector = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(scope=self.scope)
        )

    def update_check(self, old_playing_info, new_playing_info):
        if old_playing_info is None:
            return True
        if new_playing_info.is_playing != old_playing_info.is_playing:
            return True
        if new_playing_info.current_track != old_playing_info.current_track:
            return True
        if new_playing_info.progress != old_playing_info.progress:
            return True
        return False

    def sync(self):
        if self.playing_info is not None and self.playing_info.is_playing:
            logging.debug(
                f"NOW PLAYING: {self.playing_info.current_track_artist} - {self.playing_info.current_track_title} ({int(time.time()*1000) - self.playing_info.current_begin_time}/{self.playing_info.current_track_length})"
            )
        logging.debug("TRY SYNC WITH SPOTIFY")
        if not self.sync_mutex.tryLock(0):
            logging.debug("SYNCING SKIPPED")
            return
        info = None
        try:
            info = asyncio.run(self.get_now_playing_info())
        except:
            self.sync_mutex.unlock()
            return
        if self.update_check(self.playing_info, info):
            logging.debug("SYNCING")
            self.playing_info = info
            if self.update_callback is not None:
                self.update_callback(self.playing_info)
        self.sync_mutex.unlock()

    async def get_now_playing_info(self):
        info, current_time = None, int(time.time() * 1000)
        try:
            info = self.spotify_connector.current_user_playing_track()
        except Exception as e:
            logging.info(e)
            logging.info("SPOTIFY CONNECTION FAILED")
            return None
        if info is None:
            return None
        return PlayingInfo(
            current_track=TrackInfo(
                artist=(
                info["item"]["artists"][0]["name"]
                if "artists" in info["item"]
                and len(info["item"]["artists"]) > 0
                and "name" in info["item"]["artists"][0]
                else None
                ),
                id=(
                    info["item"]["id"] if "item" in info and "id" in info["item"] else None
                ),
                title=(
                    info["item"]["name"]
                    if "item" in info and "name" in info["item"]
                    else None
                ),
                length=(
                    info["item"]["duration_ms"]
                    if "item" in info and "duration_ms" in info["item"]
                    else None
                )
            ),
            current_begin_time=(
                (current_time - info["progress_ms"]) if "progress_ms" in info else None
            ),
            is_playing=info["is_playing"] if "is_playing" in info else None,
            progress=info["progress_ms"] if "progress_ms" in info else None,
        )
