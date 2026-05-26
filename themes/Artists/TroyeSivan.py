STYLES = {
    "something to give each other": {
        # "foreground": {
        #     "color": "qradialgradient(mode:logical, spread:reflect, cx:width/2, cy:height/2, radius:10, fx:width/2, fy:height/2, stop:0 #e0c00055, stop:0.1 #e0edaa55, stop:1 #00000000)",
        # },
        "background": {
            # "color": "qradialgradient(mode:logical, spread:reflect, cx:width/2, cy:height/2, radius:7, fx:width/2, fy:height/2, stop:0 #00000000, stop:0.5 #e0edaa55, stop:1 #e0c000)",
        },
        "font": {
            "family": "Helvetica",
            "weight": "black",
            "italic": True,
            "color": "#d94040",
            "color": "qradialgradient(mode:logical, spread:reflect, cx:width/2, cy:height/2, radius:10, fx:width/2, fy:height/2, stop:0 #d9404055, stop:0.4 #bd6c6c55, stop:1 #00000000)",
        },
        "line": {
            "width": 1,
            "color": "#dc0102",
        },
        "shadow": {
            "color": "#dc0102",
            # "offset": [0, 10],
            "radius": 40,
        },
        "animation": {
            "sustaining": "hshaking",
        },
        "match": {
            "artist": "troye sivan",
            "title_any": [
                "rush",
                "what's the time where you are?",
                "one of your girls",
                "in my room",
                "still got it",
                "can't go back, baby",
                "got me started",
                "silly",
                "honey",
                "how to stay with you",
            ],
        },
        "format": lambda line: "⚡" + line.upper() + "⚡",
    }
}
