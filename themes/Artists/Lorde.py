STYLES = {
    "virgin": {
        "foreground": {
            "color": "qradialgradient(mode:logical, spread:reflect, cx:width/2, cy:height/2, radius:50, fx:width/2, fy:height/2, stop:0 #94c1e133, stop:0.3 #0b88be33, stop:1 #00000000)"
        },
        "background": {"image": "images/virgin.png"},
        "font": {
            "family": "fonts/EurostileExtended.ttf",
            "weight": "bold",
            "color": "#f21905",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#939a1b",
            "radius": 20,
        },
        "animation": {
            "sustaining": "",
        },
        "match": {
            "artist": "lorde",
            "title_any": [
                "hammer",
                "what was that",
                "shapeshifter",
                "man of the year",
                "favourite daughter",
                "current affairs",
                "clearblue",
                "grwm",
                "broken glass",
                "if she could see me now",
                "david",
            ],
        },
    },
    "solar power": {
        "background": {
            # "color": "qradialgradient(spread:pad, mode:logical, cx:width/2, cy:height/2, radius:height/2+width/4, fx:width/2, fy:height/2, stop:0 #e2f2f3, stop:0.3 #a9cde6, stop:0.76 #77addb, stop:0.8 #4686cb, stop:1 #00000000)",
            "color": "qradialgradient(spread:pad, mode:logical, cx:width/2, cy:height/2, radius:height/2+width/4, fx:width/2, fy:(height/2+width/4)/5*3, stop:0 #e2f2f3, stop:0.3 #a9cde6, stop:0.76 #77addb, stop:0.8 #4686cb, stop:1 #00000000)",
        },
        "font": {
            "family": "Helvetica",
            "color": "#dfe817",
            "weight": "black",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#939a1b",
            "radius": 20,
        },
        "match": {
            "artist": "lorde",
            "title_any": [
                "the path",
                "solar power",
                "california",
                "stoned at the nail salon",
                "fallen fruit",
                "secrets from a girl",
                "the man with the axe",
                "dominoes",
                "big star",
                "leader of a new regime",
                "mood ring",
                "oceanic feeling",
                "helen of troy",
                "hold no grudge",
            ],
        },
    },
    "melodrama": {
        "background": {
            "image": "images/melodrama.png",
        },
        "font": {
            # "family": "Canela Light Trial",
            "family": "fonts/Canela-Light.otf",
            "color": "#f7c059",
            "size": "33px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {"color": "#e34345", "offset": [2, 2], "radius": 5},
        "match": {
            "artist": "lorde",
            "title_any": [
                "green light",
                "sober",
                "homemade dynamite",
                "the louvre",
                "liability",
                "hard feelings/loveless",
                "sober ii (melodrama)",
                "writer in the dark",
                "supercut",
                "liability (reprise)",
                "perfect places",
            ],
        },
    },
    "pure heroine": {
        "font": {
            # "family": "Futura",
            "family": "fonts/Futura.ttf",
            "size": "25px",
            "color": "qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #ffffff, stop:0.9 #ffffff, stop:1 #b7b5b6)",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#ffffff",
        },
        "match": {
            "artist": "lorde",
            "title_any": [
                "tennis court",
                "400 lux",
                "royals",
                "ribs",
                "buzzcut season",
                "team",
                "glory and gore",
                "still sane",
                "white teeth teens",
                "a world alone",
            ],
        },
        "format": lambda x: " ".join(x.upper()).replace("   ", "  "),
    },
}
