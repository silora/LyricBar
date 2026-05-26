STYLES = {
    "eusexua": {
        "background": {
            "image": "images/eusexua.png",
        },
        "font": {
            # "family": "OBG EUSEXUA 2024",
            "family": "fonts/Eusexua.ttf",
            "size": "30px",
            "color": "#ffffff",
        },
        "line": {
            "color": "#000000",
            "width": 0,
        },
        "shadow": {
            "enabled": False,
        },
        "match": {
            "artist": "fka twigs",
            "title_any": [
                "eusexua",
                "girl feels good",
                "perfect stranger",
                "drums of death",
                "room of fools",
                "sticky",
                "keep it, hold it",
                "childlike things",
                "striptease",
                "24hr dog",
                "wanderlust",
            ],
        },
        "format": lambda line: line.upper()
        .replace("â€˜", "'")
        .replace("â€™", "'")
        .replace("'", ""),
    },
    "afterglow": {
        "background": {
            "image": "images/afterglow.png",
        },
        "font": {
            "family": "fonts/Eusexua.ttf",
            "size": "30px",
            "color": "#000000",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "enabled": False,
        },
        "match": {
            "artist": "fka twigs",
            "title_any": [
                "love crimes",
                "slushy",
                "wild and alone",
                "hard",
                "cheap hotel",
                "touch a girl",
                "predictable girl",
                "sushi",
                "piece of mine",
                "lost all my friends",
                "stereo boy",
            ],
        },
        "format": lambda line: line.upper()
        .replace("â€˜", "'")
        .replace("â€™", "'")
        .replace("'", ""),
    },
}
