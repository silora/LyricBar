STYLES = {
    "wor$t girl in america": {
        "foreground": {
            "image": "images/worstgirlinamerica_fore.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/Futura-Italic.ttf",
            "color": "#83aec7",
            "weight": "bold",
            "italic": True,
            "size": "30px",
        },
        "line": {
            "width": 0,
            "color": "#83aec7",
        },
        "shadow": {
            "color": "#0d3248",
            "offset": [2, 2],
            "radius": 5,
        },
        "animation": {
            "entering": "zoomin",
        },
        "match": {
            "artist": "slayyyter",
            "title_any": [
                "dance...",
                "beat up chanels",
                "cannibalism!",
                "old technology",
                "crank",
                "gas station",
                "yes goddd",
                "unknown loverz",
                "old flings",
                "i'm actually kinda famous",
                "st. loser",
                "what is it like, to be liked?",
                "*prayer*",
                "brittany murphy.",
            ],
        },
        "format": lambda line: line.upper(),
    }
}
