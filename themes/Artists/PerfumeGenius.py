STYLES = {
    "glory": {
        "foreground": {
            "image": "images/glory_fore.png",
        },
        "background": {
            "image": "images/glory.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/Univers.ttf",
            # "color": "#285eff",
            "color": "qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0.2 #285eff, stop:0.7 #bdcdff)",
            "size": "30px",
            "italic": True,
        },
        "line": {
            "width": 0,
            "color": "#0a0e46",
        },
        "shadow": {
            "color": "#363743",
            "offset": [1, 1],
            "radius": 5,
        },
        "animation": {
            "entering": "topslidein",
            "leaving": "bottomslideout",
            "sustaining": "vshaking",
        },
        "match": {
            "artist": "perfume genius",
            "title_any": [
                "it's a mirror",
                "no front teeth",
                "clean heart",
                "me & angel",
                "left for tomorrow",
                "full on",
                "capezio",
                "dion",
                "in a row",
                "hanging out",
                "glory",
                "it's fine",
                "undercurrent",
            ],
        },
        "format": lambda line: line.upper(),
    },
    "ugly season": {
        "background": {
            "image": "images/uglyseason.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/Mariken.ttf",
            "color": "#d11e0c",
            "size": "40px",
            # "weight": "bold",
        },
        "line": {
            "width": 0,
            "color": "#0a0e46",
        },
        "shadow": {
            "color": "#363743",
            "offset": [1, 1],
            "radius": 5,
        },
        "animation": {
            "entering": "topslidein",
            "leaving": "bottomslideout",
            "sustaining": "hshaking",
        },
        "match": {
            "artist": "perfume genius",
            "title_any": [
                "just a room",
                "herem",
                "teeth",
                "pop song",
                "scherzo",
                "ugly season",
                "eye in the wall",
                "photograph",
                "hellbent",
                "cenote",
            ],
        },
        "format": lambda line: line.upper(),
    },
    "set my heart on fire immediately": {
        "font": {
            "family": "fonts/VirginRomanNormal.ttf",
            "weight": "bold",
            "size": "50px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {"enabled": False},
        "match": {
            "artist": "perfume genius",
            "title_any": [
                "whole life",
                "describe",
                "without you",
                "jason",
                "leave",
                "on the floor",
                "your body changes everything",
                "moonbend",
                "just a touch",
                "nothing at all",
                "one more try",
                "some dream",
                "borrowed light",
            ],
        },
        "format": lambda line: line.upper(),
    },
    "too bright": {
        "foreground": {
            # "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #a58460, stop:1 #99795b)",
            "image": "images/toobright_fore.png"
        },
        "background": {
            # "color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #a58460, stop:1 #99795b)",
            "image": "images/toobright.png"
        },
        "font": {
            "family": "fonts/AceSans-Bold.ttf",
            "color": "#e7dfc8",
            "size": "30px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {"enabled": False},
        "match": {
            "artist": "perfume genius",
            "title_any": [
                "i decline",
                "queen",
                "fool",
                "no good",
                "my body",
                "don't let them in",
                "grid",
                "longpig",
                "i'm a mother",
                "too bright",
                "all along",
            ],
        },
        "format": lambda line: line.upper(),
    },
}
