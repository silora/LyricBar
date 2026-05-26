STYLES = {
    "through the wall": {
        "background": {
            "image": "images/throughthewall.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/Legan.ttf",
            "color": "#e9e9f3",
            "weight": "bold",
            "size": "30px",
        },
        "line": {
            "width": 0,
            "color": "#ffffff",
        },
        "shadow": {
            "color": "#ffffff",
        },
        "animation": {
            "entering": "leftslidein",
            "leaving": "rightslideout",
            "sustaining": "hshaking",
        },
        "match": {
            "artist": "rochelle jordan",
            "title_any": [
                "grace",
                "ladida",
                "sum",
                "the boy",
                "doing it too",
                "never enough",
                "words 2 say",
                "bite the bait",
                "on 2 something",
                "ttw",
                "crave",
                "get it off",
                "sweet sensation",
                "eyes shut",
                "close 2 me",
                "i'm your muse",
                "around",
            ],
        },
        "format": lambda line: line.upper(),
    }
}
