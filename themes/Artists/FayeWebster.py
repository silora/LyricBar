STYLES = {
    "faye webster": {
        # "font-family": "TWS Modern French 25",
        "font-family": "fonts/TWSModernFrench25.ttf",
        "font-color": "#1d5fa3",
        "font-size": "25px",
        
        "line-color": "#a4abe0",
        "line-width": 0,
        
        "shadow-color": "#cecece66",
        "shadow-offset": [3, 3],
        "shadow-radius": 5,
        
        "rule": lambda track: (track.artist.lower() == "faye webster")
    }
}