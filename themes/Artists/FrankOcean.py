STYLES = {
    "channel orange":{
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.4, radius:0.5, fx:0.25, fy:0.25, stop:0 #f37521, stop:1 #00000000)",
        # "font-family": "Cooper Black",
        "font-family": "fonts/CooperBlack.ttf",
        "font-image": "images/channelorange.png",
        
        "line-width": 0,
        
        "shadow-color": "#ffffff",
        "shadow-radius": 15,
        
        
        "rule": lambda track: (track.artist.lower() == "frank ocean" and (any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["start", "thinkin bout you", "fertilizer", "sierra leone", "sweet life", "not just money", "super rich kids", "pilot jones", "crack rock", "pyramids", "lost", "monks", "bad religion", "pink matter", "forrest gump", "end"]]) or ("white" in track.title.lower() and "pink" not in track.title.lower()))),
    },
    "blonde": {
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.6, radius:0.5, fx:0.75, fy:0.25, stop:0 #e0e0e0, stop:1 #00000000)",
        
        # "font-family": "Blonde",
        "font-family": "fonts/Blonde.otf",
        "font-color": "#000000aa",
        "font-size": "50px",
        
        "line-width": 0,
        
        "shadow-color": "#000000",
        "shadow-radius": 15,
        
        
        "rule": lambda track: (track.artist.lower() == "frank ocean" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["nikes", "ivy", "pink + white", "be yourself", "solo", "skyline to", "self control", "good guy", "nights", "solo (reprise)", "pretty sweet", "facebook story", "close to you", "white ferrari", "seigfried", "godspeed", "futura free"]])),
        
        "format": lambda line: "".join([_ for _ in line if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ♬"])
    }
}