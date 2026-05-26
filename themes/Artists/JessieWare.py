STYLES = {
    "what's your pleasure": {
        "background": {
            "color": "qradialgradient(spread:pad, mode:logical, cx:width/2, cy:height/2, radius:height/2+width/4, fx:width/2, fy:height/2, stop:0 #00000000, stop:0.6 #f1ece8, stop:0.7 #f1ece8, stop:0.8 #00000000)",
        },
        "font": {
            "family": "Helvetica",
            "color": "qlineargradient(spread:pad, x1:0, y1:0.4, x2:1, y2:0.43, stop:0 #f1ece8, stop:.30 #261c1a, stop:0.4 #261c1aaa, stop:0.5 #261c1a, stop:0.9 #261c1a, stop:1 #f1ece8aa)",
            "weight": "bold",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#261c1a",
        },
        "match": {
            "artist": ["jessie ware"],
            "title_any": [
                "spotlight",
                "what's your pleasure?",
                "ooh la la",
                "soul control",
                "save a kiss",
                "adore you",
                "in your eyes",
                "step into my life",
                "read my lips",
                "mirage (don't stop)",
                "the kill",
                "remember where you are",
                "please",
                "impossible",
                "eyes closed",
                "overtime",
                "hot n heavy",
                "pale blue light",
                "0208",
            ],
        },
        "format": lambda x: x.upper(),
    }
}
