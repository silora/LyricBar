STYLES = {
    "rock music": {
        "background": {
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #ffffff, stop:1 #00000000)",
        },
        "font": {
            "color": "#000000",
            # "family": "Arial Narrow",
            "family": "Times New Roman",
            "size": "30px",
            "weight": "bold",
        },
        "line": {
            "color": "#000000",
            "width": 0,
        },
        "shadow": {
            "enabled": False,
        },
        "match": {
            "artist": "charli xcx",
            "title_any": [
                "rock music",
                "ss26",
                "i keep thinking about you every single day and night",
                "playboy bunny",
            ],
        },
        "format": lambda line: line.upper(),
    },
    "brat remix": {
        "background": {
            # "color": "#8bcc00",
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #8bcc00, stop:1 #00000000)",
        },
        "font": {
            "color": "#000000",
            # "family": "Arial Narrow",
            "family": "fonts/ArialNarrow.ttf",
            "size": "30px",
            "weight": "light",
        },
        "line": {
            "color": "#000000",
            "width": 0,
        },
        "shadow": {
            "color": "#000000",
            "offset": [0, 0],
            "radius": 7,
        },
        "text": {
            "flip": True,
        },
        "match": {
            "artist": "charli xcx",
            "any": [
                {"title_all": ["360", "robyn"]},
                {"title_all": ["club classics", "bb trickz"]},
                {"title_all": ["sympathy is a knife", "ariana grande"]},
                {"title_all": ["i might say something stupid", "the 1975"]},
                {"title_all": ["talk talk", "troye sivan"]},
                {"title_all": ["von dutch", "a. g. cook"]},
                {"title_all": ["everything is romantic", "caroline polachek"]},
                {"title_all": ["rewind", "bladee"]},
                {"title_all": ["so i", "a. g. cook"]},
                {"title_all": ["girl, so confusing", "lorde"]},
                {"title_all": ["apple", "the japanese house"]},
                {"title_all": ["b2b", "tinashe"]},
                {"title_all": ["mean girls", "julian casablancas"]},
                {"title_all": ["i think about it all the time", "bon iver"]},
                {"title_all": ["365", "shygirl"]},
                {"title_all": ["guess", "billie eilish"]},
                {"title_all": ["spring breakers", "kesha"]},
            ],
        },
    },
    "brat": {
        "background": {
            # "color": "#8ace00",
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #8ace00, stop:1 #00000000)",
        },
        "font": {
            "color": "#000000",
            # "family": "Arial Narrow",
            "family": "fonts/ArialNarrow.ttf",
            "size": "30px",
            "weight": "light",
        },
        "line": {
            "color": "#000000",
            "width": 0,
        },
        "shadow": {
            "color": "#000000",
            "offset": [0, 0],
            "radius": 7,
        },
        "match": {
            "artist": "charli xcx",
            "title_any": [
                "360",
                "club classics",
                "sympathy is a knife",
                "i might say something stupid",
                "talk talk",
                "von dutch",
                "everything is romantic",
                "rewind",
                "so i",
                "girl, so confusing",
                "apple",
                "b2b",
                "mean girls",
                "i think about it all the time",
                "365",
                "guess",
                "spring breakers",
                "hello goodbye",
                "in the city",
            ],
        },
    },
    "crash": {
        "background": {
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.3, fx:0.5, fy:0.2, stop:0 #e30e13, stop:1 #00000000)",
        },
        "font": {
            # "color": "#1640be",
            "color": "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #1640be, stop:1 #7d92d3)",
            # "family": "Onyx BT",
            "family": "fonts/OnyxBT.ttf",
            "size": "40px",
        },
        "line": {
            "color": "#e8ebf5",
            "width": 0,
        },
        "shadow": {
            # "enabled": False,
            "color": "#000000",
        },
        "match": {
            "artist": "charli xcx",
            "title_any": [
                "crash",
                "new shapes",
                "good ones",
                "constant repeat",
                "beg for you",
                "move me",
                "baby",
                "lightning",
                "every rule",
                "yuck",
                "used to know me",
                "twice",
                "selfish girl",
                "how can i not know what i need right now",
                "sorry if i hurt you",
                "what you think about me",
            ],
        },
    },
    "pop2": {
        "background": {
            "color": "qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #00000000 stop:0.2 #00000000, stop:0.35 #6c4343, stop:0.4 #815d39, stop:0.45 #706c3d, stop:0.5 #4b6d3b, stop:0.55 #3d6c6c, stop:0.6 #394b6d, stop:0.65 #4b3b6d, stop:0.8 #00000000, stop:1 #00000000)",
        },
        "font": {
            "color": "#d8d2ed",
        },
        "progress": {
            "color": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e48d8d, stop:0.16 #eca864, stop:0.33 #efe87c, stop:0.5 #a5e8a5, stop:0.66 #7ce8ef, stop:0.83 #7c9fef, stop:1 #a57cef)",
            "line_color": "#00000000",
        },
        "font": {
            # "family": "Neoneon",
            "family": "fonts/ChangelingNeoInline.otf",
            "size": "33px",
        },
        "line": {
            "width": 0.25,
            "color": "#9f93cc",
        },
        "shadow": {
            "color": "#d8d2ed",
            "radius": 10,
        },
        "match": {
            "artist": "charli xcx",
            "title_any": [
                "backseat",
                "out of my head",
                "lucky",
                "tears",
                "i got it",
                "femmebot",
                "delicious",
                "unlock it",
                "porsche",
                "track 10",
            ],
        },
    },
    "vroom vroom": {
        "font": {
            "color": "#0000000099",
            # "family": "Rawhide Raw 2012",
            "family": "fonts/RawhideRaw2012.ttf",
            "size": "27px",
        },
        "line": {
            "color": "#e3e3e3",
            "width": 1.1,
        },
        "shadow": {
            "color": "#757575",
            "offset": [1.5, 1.5],
            "radius": 3,
        },
        "match": {
            "artist": "charli xcx",
            "title_any": ["vroom vroom", "paradise", "trophy", "secret"],
        },
        "format": lambda line: "".join(
            [
                _
                for _ in line
                if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-"
            ]
        )
        .upper()
        .replace("R ", "r "),
    },
}
