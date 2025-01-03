STYLES = {
    "honeymoon": {
        # "font-family": "Joanna Solotype CG",
        "font-family": "fonts/JoannaSolotypeCG.otf",
        "font-size": "50px",
        
        "line-width": 0,
        
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() == "lana del rey" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["honeymoon", "music to watch boys to", "terrence loves you", "god knows i tried", "high by the beach", "art deco", "burnt norton", "religion", "salvatore", "the blackest day", "24", "swan song", "don't let me be misunderstood"]]) or track.title.lower().replace("‘", "'").replace("’", "'") in ["freak"])
    },
    "lfl": {
        "font-family": "fonts/LTCCaslonLongSwash.ttf",
        
        "rule": lambda track: (track.artist.lower() == "lana del rey" and (any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["lust for life", "13 beaches", "cherry", "white mustang", "summer bummer", "groupie love", "in my feelings", "coachella - woodstock in my mind", "god bless america - and all the beautiful people in it", "when the world was at war we kept dancing", "beautiful people beautiful problems", "tomorrow never came", "get free"]]) or track.title.lower().replace("‘", "'").replace("’", "'") in ["love", "change", "heroin"]))
    },
    "nfr": {
        "background-image": "images/nfr.png",
        
        # "font-family": "CCBiffBamBoom",
        "font-family": "fonts/CCBiffBamBoom.ttf",
        "font-color": "#e9dabd",
        
        "line-color": "#030101",
        "line-width": 1.5,
        
        "shadow-color": "#030101",
        "shadow-offset": [2, 2],
        "shadow-radius": 5,
        
        "entering": "zoomin_overscale",
        "sustaining": "zooming",
        "leaving": "topslideout",
        
        "rule": lambda track: (track.artist.lower() == "lana del rey" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["norman fucking rockwell", "mariners apartment complex", "venice bitch", "fuck it i love you", "doin' time", "love song", "cinnamon girl", "how to disappear", "california", "the next best american record", "the greatest", "bartender", "happiness is a butterfly", "hope is a dangerous thing for a woman like me to have - but i have it"]]))
    },
    "cotc": {
        # "font-family": "Marons",
        "font-family": "fonts/Marons.otf",
        "font-size": "40px",
        
        "shadow-color": "#000000",
        "shadow-offset": [3, 3],
        
        "rule": lambda track: (track.artist.lower() == "lana del rey" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["white dress", "chemtrails over the country club", "tulsa jesus freak", "let me love you like a woman", "wild at heart", "dark but just a game", "not all who wander are lost", "yosemite", "breaking up slowly", "dance till we die", "for free"]]))
    },
    "bb": {
        # "font-family": "Modern No. 216 Heavy",
        "font-family": "fonts/ModernNo216Heavy.ttf",
        "font-size": "20px",
        
        "rule": lambda track: (track.artist.lower() == "lana del rey" and (any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["text book", "blue banisters", "arcadia", "interlude - the trio", "black bathing suit", "if you lie down with me", "violets for roses", "dealer", "thunder", "wildflower wildfire", "nectar of the gods", "living legend", "cherry blossom", "sweet carolina"]]) or track.title.lower().replace("‘", "'").replace("’", "'") in ["beautiful"]))
    },
    "blvd": {
        # "font-family": "Futura Display",
        "font-family": "fonts/FuturaDisplay.ttf",
        "font-color": "#f2db78",
        "font-size": "40px",
        
        "shadow-radius": 3,
        
        "rule": lambda track: (track.artist.lower() == "lana del rey" and (any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["the grants", "did you know that there's a tunnel under ocean blvd", "sweet", "a&w", "judah smith interlude", "candy necklace", "jon batiste interlude", "kintsugi", "fingertips", "paris, texas", "grandfather please stand on the shoulders of my father while he's deep-sea fishing", "let the light in", "margaret", "fishtail", "peppers", "taco truck x vb"]]) or track.title.lower().replace("‘", "'").replace("’", "'") in ["sweet"]))
    },
    "lana del rey": {
        # "font-family": "Rainbow",
        "font-family": "fonts/Rainbow.ttf",
        "font-size": "50px",
        "font-color": "qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 #998a4b, stop:0.3 #9f904d, stop:1 #fdf9dc)",
        
        "line-width": 0,
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() == "lana del rey")
    }
}