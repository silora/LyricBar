STYLES = {
    "honeymoon": {
        "background": {
            "image": "images/honeymoon.png",
        },
        "font": {
            # "family": "Joanna Solotype CG",
            # "family": "fonts/JoannaSolotypeCG.otf",
            "family": "Times New Roman",
            "size": "27px",
            "color": "#033876",
            "weight": "bold",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "enabled": False,
        },
        "match": {
            "artist": "lana del rey",
            "any": [
                {
                    "title_any": [
                        "honeymoon",
                        "music to watch boys to",
                        "terrence loves you",
                        "god knows i tried",
                        "high by the beach",
                        "art deco",
                        "burnt norton",
                        "religion",
                        "salvatore",
                        "the blackest day",
                        "24",
                        "swan song",
                        "don't let me be misunderstood",
                    ]
                },
                {"title": ["freak"]},
            ],
        },
        "format": lambda line: line.upper(),
    },
    "lfl": {
        "background": {
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.95 #eae7de, stop:1 #00000000)",
        },
        "font": {
            "family": "fonts/LTCCaslonLongSwash.ttf",
            "color": "#a8060e",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#a8060e",
        },
        "match": {
            "artist": "lana del rey",
            "any": [
                {
                    "title_any": [
                        "lust for life",
                        "13 beaches",
                        "cherry",
                        "white mustang",
                        "summer bummer",
                        "groupie love",
                        "in my feelings",
                        "coachella - woodstock in my mind",
                        "god bless america - and all the beautiful people in it",
                        "when the world was at war we kept dancing",
                        "beautiful people beautiful problems",
                        "tomorrow never came",
                        "get free",
                    ]
                },
                {"title": ["love", "change", "heroin"]},
            ],
        },
    },
    "nfr": {
        "background": {
            "image": "images/nfr.png",
        },
        "font": {
            # "family": "CCBiffBamBoom",
            "family": "fonts/CCBiffBamBoom.ttf",
            "color": "#e9dabd",
        },
        "line": {
            "color": "#030101",
            "width": 1.5,
        },
        "shadow": {
            "color": "#030101",
            "offset": [2, 2],
            "radius": 5,
        },
        "animation": {
            "entering": "zoomin_overscale",
            "sustaining": "zooming",
            "leaving": "topslideout",
        },
        "match": {
            "artist": "lana del rey",
            "title_any": [
                "norman fucking rockwell",
                "mariners apartment complex",
                "venice bitch",
                "fuck it i love you",
                "doin' time",
                "love song",
                "cinnamon girl",
                "how to disappear",
                "california",
                "the next best american record",
                "the greatest",
                "bartender",
                "happiness is a butterfly",
                "hope is a dangerous thing for a woman like me to have - but i have it",
            ],
        },
    },
    "cotc": {
        "font": {
            # "family": "Marons",
            "family": "fonts/Marons.otf",
            "size": "40px",
        },
        "shadow": {
            "color": "#000000",
            "offset": [3, 3],
        },
        "match": {
            "artist": "lana del rey",
            "title_any": [
                "white dress",
                "chemtrails over the country club",
                "tulsa jesus freak",
                "let me love you like a woman",
                "wild at heart",
                "dark but just a game",
                "not all who wander are lost",
                "yosemite",
                "breaking up slowly",
                "dance till we die",
                "for free",
            ],
        },
    },
    "bb": {
        "background": {
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.95 #eae7de, stop:1 #00000000)",
        },
        "font": {
            # "family": "Modern No. 216 Heavy",
            "family": "fonts/ModernNo216Heavy.ttf",
            "size": "20px",
            "color": "#1e1e1c",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#1e1e1c",
        },
        "match": {
            "artist": "lana del rey",
            "any": [
                {
                    "title_any": [
                        "text book",
                        "blue banisters",
                        "arcadia",
                        "interlude - the trio",
                        "black bathing suit",
                        "if you lie down with me",
                        "violets for roses",
                        "dealer",
                        "thunder",
                        "wildflower wildfire",
                        "nectar of the gods",
                        "living legend",
                        "cherry blossom",
                        "sweet carolina",
                    ]
                },
                {"title": ["beautiful"]},
            ],
        },
        "format": lambda line: line.upper(),
    },
    "blvd": {
        "font": {
            # "family": "Futura Display",
            "family": "fonts/FuturaDisplay.ttf",
            "color": "#f2db78",
            "size": "40px",
        },
        "shadow": {
            "radius": 3,
        },
        "match": {
            "artist": "lana del rey",
            "any": [
                {
                    "title_any": [
                        "the grants",
                        "did you know that there's a tunnel under ocean blvd",
                        "sweet",
                        "a&w",
                        "judah smith interlude",
                        "candy necklace",
                        "jon batiste interlude",
                        "kintsugi",
                        "fingertips",
                        "paris, texas",
                        "grandfather please stand on the shoulders of my father while he's deep-sea fishing",
                        "let the light in",
                        "margaret",
                        "fishtail",
                        "peppers",
                        "taco truck x vb",
                    ]
                },
                {"title": ["sweet"]},
            ],
        },
    },
    "lana del rey": {
        "font": {
            # "family": "Rainbow",
            "family": "fonts/Rainbow.ttf",
            "size": "50px",
            "color": "qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 #998a4b, stop:0.3 #9f904d, stop:1 #fdf9dc)",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "enabled": False,
        },
        "match": {"artist": "lana del rey"},
    },
}
