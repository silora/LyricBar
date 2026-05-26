STYLES = {
    "channel orange": {
        "background": {
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.4, radius:0.5, fx:0.25, fy:0.25, stop:0 #f37521, stop:1 #00000000)",
        },
        "font": {
            # "family": "Cooper Black",
            "family": "fonts/CooperBlack.ttf",
            "image": "images/channelorange.png",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#ffffff",
            "radius": 15,
        },
        "match": {
            "artist": "frank ocean",
            "any": [
                {
                    "title_any": [
                        "start",
                        "thinkin bout you",
                        "fertilizer",
                        "sierra leone",
                        "sweet life",
                        "not just money",
                        "super rich kids",
                        "pilot jones",
                        "crack rock",
                        "pyramids",
                        "lost",
                        "monks",
                        "bad religion",
                        "pink matter",
                        "forrest gump",
                        "end",
                    ]
                },
                {
                    "all": [
                        {"title_any": "white"},
                        {"not": {"title_any": "pink"}},
                    ]
                },
            ],
        },
    },
    "blonde": {
        "background": {
            "color": "qradialgradient(spread:pad, cx:0.5, cy:0.6, radius:0.5, fx:0.75, fy:0.25, stop:0 #e0e0e0, stop:1 #00000000)",
        },
        "font": {
            # "family": "Blonde",
            "family": "fonts/Blonde.otf",
            "color": "#000000aa",
            "size": "50px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#000000",
            "radius": 15,
        },
        "match": {
            "artist": "frank ocean",
            "title_any": [
                "nikes",
                "ivy",
                "pink + white",
                "be yourself",
                "solo",
                "skyline to",
                "self control",
                "good guy",
                "nights",
                "solo (reprise)",
                "pretty sweet",
                "facebook story",
                "close to you",
                "white ferrari",
                "seigfried",
                "godspeed",
                "futura free",
            ],
        },
        "format": lambda line: "".join(
            [
                _
                for _ in line
                if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZZ â™¬"
            ]
        ),
    },
}
