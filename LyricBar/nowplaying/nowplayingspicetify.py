import json
from websocket_server import WebsocketServer
import threading
from ..utils.dataclasses import PlayingInfo, PlayingStatusTrigger, TrackInfo
from .nowplaying import NowPlaying


class NowPlayingSpicetify(NowPlaying):
    def __init__(self, socket_port=8974, update_callback=None, offset=0):
        super().__init__(sync_interval=-1, update_callback=update_callback)
        self.server = WebsocketServer(host='127.0.0.1', port=socket_port)
        self.server.set_fn_message_received(self.message_received)
        self.offset = offset
        self.update_callback(PlayingStatusTrigger.PAUSE)
        
    def start_loop(self):
        self.thread = threading.Thread(target=self.server.run_forever, daemon=True).start()
        
    def message_received(self, client, server, message):
        info = json.loads(message)
        new_playing_info = PlayingInfo(
            current_track=TrackInfo(
                artist=info["ARTIST"],
                title=info["TITLE"],
                length=info["DURATION"],
                id=info["UID"]
            ),
            current_begin_time=info["BEGINTIME"] + self.offset,
            is_playing=info["STATE"] == 1,
        )
        
        if ((self.playing_info is not None and self.playing_info.current_track.id != new_playing_info.current_track.id) or self.playing_info is None) and new_playing_info.is_playing:
            self.playing_info = new_playing_info
            self.update_callback(PlayingStatusTrigger.NEW_TRACK)
            return
        elif self.playing_info is not None and self.playing_info.is_playing != new_playing_info.is_playing:
            if new_playing_info.is_playing:
                self.update_callback(PlayingStatusTrigger.RESUME)
            else:
                self.update_callback(PlayingStatusTrigger.PAUSE)
        elif self.playing_info is None or self.playing_info.is_playing == False:
            return
        self.playing_info = new_playing_info
        return
                
                
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    def callback(trigger):
        if trigger == PlayingStatusTrigger.PAUSE:
            print("PAUSE")
        elif trigger == PlayingStatusTrigger.RESUME:
            print("RESUME")
        elif trigger == PlayingStatusTrigger.NEW_TRACK:
            print("NEW TRACK")
    
    app = QApplication(sys.argv)
    np = NowPlayingSpicetify(update_callback=callback, offset=500)
    np.start_loop()
    breakpoint()
    sys.exit(app.exec_())