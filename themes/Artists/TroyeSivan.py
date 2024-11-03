STYLES = {
    "something to give each other": {
        "background-color": "qradialgradient(mode:logical, spread:reflect, cx:width/2, cy:height/2, radius:3, fx:width/2, fy:height/2, stop:0 #e0c00088, stop:0.4 #e0edaa88, stop:1 #00000000)",
        
        "font-family": "Helvetica",
        "font-weight": "black",
        "font-italic": True,
        "font-color": "#dc0102",
        
        "line-width": 1,
        "line-color": "#dc0102",
        
        "shadow-color": "#dc0102",
        # "shadow-offset": [0, 10],
        "shadow-radius": 40,
        
        "rule": lambda track: (track.artist.lower() == "troye sivan" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["rush", "what's the time where you are?", "one of your girls", "in my room", "still got it", "can't go back, baby", "got me started", "silly", "honey", "how to stay with you"]])),
        
        "format": lambda line: "⚡" + line.upper() + "⚡"
    }
}