from LyricBar.nowplaying import NowPlayingSystem

np = NowPlayingSystem()
sessions = np.manager.get_sessions()
sessions = [session.source_app_user_model_id for session in sessions]
print("Current Running Players:", sessions)
input("Press Enter to exit...")

