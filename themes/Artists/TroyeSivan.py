STYLES = {
    "something to give each other": {
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:1, radius:0.8, fx:0.5, fy:0.5, stop:0 #e0c000, stop:0.7 #e0edaa, stop:1 #00000000)",
        
        "font-family": "Helvetica",
        "font-weight": "black",
        "font-italic": True,
        "font-color": "#dc010288",
        
        "line-width": 1,
        "line-color": "#dc0102",
        
        "shadow-color": "#dc0102",
        # "shadow-offset": [0, 10],
        "shadow-radius": 40,
        
        "rule": lambda track: (track.artist.lower() == "troye sivan" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["rush", "what's the time where you are?", "one of your girls", "in my room", "still got it", "can't go back, baby", "got me started", "silly", "honey", "how to stay with you"]])),
        
        "format": lambda line: "⚡" + line.upper() + "⚡"
    }
}