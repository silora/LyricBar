STYLES = {
    "the land is inhospitable": {
        "background": {
            "image": "images/thelandisinhospitable.png",
        },
        "font": {
            # "family": "Tofino Pro Personal",
            "family": "fonts/Tofino.otf",
            "color": "#000000",
        },
        "line": {
            "width": 0.75,
            "color": "#000000",
        },
        "shadow": {
            "color": "#f6e3d4",
            "radius": 10,
        },
        "match": {
            "artist": "mitski",
            "any": [
                {
                    "title_any": [
                        "bug like an angel",
                        "buffalo replaced",
                        "heaven",
                        "i don't like my mind",
                        "the deal",
                        "when memories snow",
                        "my love mine all mine",
                        "the frost",
                        "i'm your man",
                        "i love me after you",
                    ]
                },
                {"title": ["star"]},
            ],
        },
        "format": lambda x: x.upper(),
    },
    "laurel hell": {
        "background": {
            "image": "images/laurelhell.png",
        },
        "font": {
            # "family": "Laurel Hell Hand2",
            "family": "fonts/LaurelHell.otf",
            "color": "#ffffff",
            "size": "35px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#ffffff",
        },
        "match": {
            "artist": "mitski",
            "title_any": [
                "valentine, texas",
                "working for the knife",
                "the only heartbreaker",
                "stay soft",
                "everyone",
                "heat lightning",
                "the only heartbreaker",
                "love me more",
                "there's nothing left for you",
                "should've been me",
                "i guess",
                "that's our lamp",
            ],
        },
        "format": lambda x: x.replace(" ", "    "),
    },
    "be the cowboy": {
        "background": {
            "image": "images/bethecowboy.png",
        },
        "font": {
            # "family": "SantoroScriptJF",
            "family": "fonts/SantoroScriptJF.otf",
            "size": "40px",
            "color": "#00000000",
        },
        "line": {
            "width": 0.75,
            "color": "#FFFFFF",
        },
        "use-color": False,
        "shadow": {
            # "color": "#FFFFFF",
        },
        "animation": {
            "sustaining": "zooming",
        },
        "match": {
            "artist": "mitski",
            "title_any": [
                "geyser",
                "why didn't you stop me?",
                "old friend",
                "a pearl",
                "lonesome love",
                "remember my name",
                "me and my husband",
                "come into the water",
                "nobody",
                "pink in the night",
                "a horse named cold air",
                "washing machine heart",
                "blue light",
                "two slow dancers",
            ],
        },
    },
    "puberty 2": {
        "background": {
            "image": "images/puberty2.png",
        },
        "font": {
            # "family": "Edwardian Script ITC",
            "family": "fonts/EdwardianScriptITC.ttf",
            "image": "images/puberty2text.png",
            "size": "50px",
            "weight": "black",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "enabled": True,
            "color": "#ffffff",
            "radius": 10,
        },
        "match": {
            "artist": "mitski",
            "title_any": [
                "happy",
                "dan the dancer",
                "once more to see you",
                "fireworks",
                "your best american girl",
                "i bet on losing dogs",
                "my body's made of crushed little stars",
                "thursday girl",
                "a loving feeling",
                "crack baby",
                "a burning hill",
            ],
        },
    },
    "bury me at makeout creek": {
        "background": {
            "image": "images/burymeatmakeoutcreek.png",
        },
        "font": {
            "family": "Times New Roman",
            "size": "25px",
            "color": "#000000",
        },
        "shadow": {
            # "color": "#FFFFFF",
        },
        "line": {
            "color": "#000000",
            "width": 0.25,
        },
        "shadow": {
            "enabled": False,
        },
        "animation": {
            "entering": "rightslidein",
            "sustaining": "",
            "leaving": "leftslideout",
        },
        "match": {
            "artist": "mitski",
            "title_any": [
                "texas reznikoff",
                "townie",
                "first love/late spring",
                "francis forever",
                "i don't smoke",
                "jobless monday",
                "drunk walk home",
                "i will",
                "carry me out",
                "last words of a shooting star",
            ],
        },
        "format": lambda line: line.replace(" ", "  "),
    },
    "retire from sad": {
        "background": {
            "image": "images/retirefromsad.png",
        },
        "font": {
            # "family": "Nimbus Sans", #should be Nimbus Sans Round tho... i don't have that font
            # "family": "fonts/NimbusSans-Bold.otf",
            "family": "fonts/Circled.ttf",
            "weight": "black",
            "color": "#4fafc0",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#000000",
            "radius": 10,
        },
        "match": {
            "artist": "mitski",
            "title_any": [
                "goodbye, my danish sweetheart",
                "square",
                "strawberry blond",
                "humpty",
                "i want you",
                "because dreaming costs money, my dear",
                "circle",
                "class of 2013",
            ],
        },
        # "format": lambda line: " ".join(line.lower()),
        # "format": lambda line: circle_format(line),
        "format": lambda line: "".join(
            filter(lambda x: x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.?!", line.upper())
        ),
    },
    "lush": {
        "background": {
            "image": "images/lush.png",
        },
        "font": {
            # "family": "Avenir LT Std 35 Light",
            "family": "fonts/AvenirLTStd-Light.otf",
            "color": "#ffffff",
            "weight": "light",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#ffffff",
        },
        "match": {
            "artist": "mitski",
            "title_any": [
                "liquid smooth",
                "wife",
                "abbey",
                "brand new city",
                "eric",
                "bag of bones",
                "door",
                "pearl driver",
                "real men",
            ],
        },
        "format": lambda x: x.upper(),
    },
    "nothing's about to happen to me": {
        "background": {
            "image": "images/nothingsabouttohappentome.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/Forevs.ttf",
            "color": "#24242a",
            "size": "35px",
        },
        "line": {
            "width": 0,
            "color": "#ffffff",
        },
        "shadow": {
            "color": "#ffffff",
        },
        "animation": {
            "entering": "fadein",
            "leaving": "fadeout",
            "sustaining": "hshaking",
        },
        "match": {
            "artist": "mitski",
            "any": [
                {
                    "title_any": [
                        "in a lake",
                        "where's my phone?",
                        "cats",
                        "if i leave",
                        "dead women",
                        "instead of here",
                        "i'll change for you",
                        "rules",
                        "that white cat",
                        "charon's obol",
                    ]
                },
                {
                    "title": ["lightning"],
                },
            ],
        },
        "format": lambda line: (
            ('"' + (line + ". " if line[-1] not in ".!?," else line) + '"')
            if line not in "♬⏸"
            else line
        ),
    },
}
