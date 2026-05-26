STYLES = {
    "iconoclasts": {
        "background": {
            "image": "images/iconoclasts.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/GoudyOldStyleRoman.ttf",
            "color": "#d2d2d2",
            "weight": "bold",
            "size": "26px",
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
        "match": {
            "artist": "anna von hausswolff",
            "title_any": [
                "the beast",
                "facing atlas",
                "the iconoclast",
                "the whole woman",
                "the mouth",
                "stardust",
                "aging young women",
                "consensual neglect",
                "struggle with the beast",
                "an ocean of time",
                "unconditional love",
                "rising legends",
            ],
        },
        "format": lambda line: line.upper(),
    }
}
