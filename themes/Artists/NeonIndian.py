STYLES = {
    "neonindian": {
        "background-color": "#00000000",
        
        # "font-color": "qlineargradient(spread:pad, x1:0.3, y1:1, x2:0.7, y2:0, stop:0 #e0eef5, stop:1 #86a4cd)",
        "font-color": "#e0eef5aa",
        "font-family": "fonts/Bayshore.otf",
        "font-size": "50px",
        "font-weight": "bold",
        "font-italic": False,
        
        
        "line-color": "#e0eef5aa",
        "line-width": 0.5,

        "use-shadow": True,
        "shadow-color": "#0e98de",
        "shadow-offset": [0, 0],
        "shadow-radius": 20,
        
        "rule": lambda track: (track.artist.lower() == "neon indian")
    }
}