STYLES = {
    "post": {
        "font": {
            "color": "#d58fe8",
            # "family": "Bjork",
            "family": "fonts/Bjork.ttf",
            "size": "40px",
        },
        "line": {
            "color": "#a22929",
            "width": 1,
        },
        "shadow": {
            "color": "#a22929",
            "offset": [2, 2],
            "radius": 8,
        },
        "match": {
            "artist": ["bjork", "björk"],
            "title_any": [
                "army of me",
                "hyperballad",
                "hyper-ballad",
                "the modern things",
                "it's oh so quiet",
                "enjoy",
                "you've been flirting again",
                "isobel",
                "possibly maybe",
                "i miss you",
                "cover me",
                "headphones",
            ],
        },
        "format": lambda line: "".join(
            [
                _
                for _ in line
                if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ â™¬"
            ]
        ),
    },
    "vespertine": {
        "font": {
            "color": "#ffffff",
            # "family": "vespertine",
            "family": "fonts/Vespertine.ttf",
            "size": "50px",
        },
        "line": {
            "width": 0.75,
            "color": "#ffffff",
        },
        "shadow": {
            "enabled": False,
        },
        "match": {
            "artist": ["bjork", "björk"],
            "title_any": [
                "hidden place",
                "cocoon",
                "it's not up to you",
                "undo",
                "pagan poetry",
                "frosti",
                "aurora",
                "an echo, a stain",
                "sun in my mouth",
                "heirloom",
                "harm of will",
                "unison",
                "stonemilker",
                "lionsong",
                "history of touches",
                "black lake",
                "family",
                "notget",
                "atom dance",
                "mouth mantra",
                "quicksand",
            ],
        },
    },
}
