STYLES = {
    "brat remix": {
        # "background-color": "#8bcc00",
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #8bcc00, stop:1 #00000000)",
        
        "font-color": "#000000",
        # "font-family": "Arial Narrow",
        "font-family": "fonts/ArialNarrow.ttf",
        "font-size": "30px",
        "font-weight": "light",
        
        "line-color": "#000000",
        "line-width": 0,

        "shadow-color": "#000000",
        "shadow-offset": [0, 0],
        "shadow-radius": 7,
        
        "flip-text": True,
        
        "rule": lambda track: (track.artist.lower() == "charli xcx" and any([all([s in track.title.lower().replace("‘", "'").replace("’", "'") for s in _ ]) for _ in [("360", "robyn"), ("club classics", "bb trickz"), ("sympathy is a knife", "ariana grande"), ("i might say something stupid", "the 1975"), ("talk talk", "troye sivan"), ("von dutch", "a. g. cook"), ("everything is romantic", "caroline polachek"), ("rewind", "bladee"), ("so i", "a. g. cook"), ("girl, so confusing", "lorde"), ("apple", "the japanese house"), ("b2b", "tinashe"), ("mean girls", "julian casablancas"), ("i think about it all the time", "bon iver"), ("365", "shygirl"), ("guess", "billie eilish"), ("spring breakers", "kesha")]]))
    },
    "brat": {
        # "background-color": "#8ace00",
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0, stop:0 #8ace00, stop:1 #00000000)",
        
        "font-color": "#000000",
        # "font-family": "Arial Narrow",
        "font-family": "fonts/ArialNarrow.ttf",
        "font-size": "30px",
        "font-weight": "light",
        
        "line-color": "#000000",
        "line-width": 0,

        "shadow-color": "#000000",
        "shadow-offset": [0, 0],
        "shadow-radius": 7,
        
        "rule": lambda track: (track.artist.lower() == "charli xcx" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["360", "club classics", "sympathy is a knife", "i might say something stupid", "talk talk", "von dutch", "everything is romantic", "rewind", "so i", "girl, so confusing", "apple", "b2b", "mean girls", "i think about it all the time", "365", "guess", "spring breakers", "hello goodbye", "in the city"]]))
    },
    "crash": {
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.3, fx:0.5, fy:0.2, stop:0 #e30e13, stop:1 #00000000)",
        
        # "font-color": "#1640be",
        "font-color": "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #1640be, stop:1 #7d92d3)",
        # "font-family": "Onyx BT",
        "font-family": "fonts/OnyxBT.ttf",
        "font-size": "40px",
        
        "line-color": "#e8ebf5",
        "line-width": 0,
        
        # "use-shadow": False,
        "shadow-color": "#000000",

        "rule": lambda track: (track.artist.lower() == "charli xcx" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["crash", "new shapes", "good ones", "constant repeat", "beg for you", "move me", "baby", "lightning", "every rule", "yuck", "used to know me", "twice", "selfish girl", "how can i not know what i need right now", "sorry if i hurt you", "what you think about me"]]))
    }, 
    "pop2": {
        "background-color": "qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #00000000 stop:0.2 #00000000, stop:0.35 #6c4343, stop:0.4 #815d39, stop:0.45 #706c3d, stop:0.5 #4b6d3b, stop:0.55 #3d6c6c, stop:0.6 #394b6d, stop:0.65 #4b3b6d, stop:0.8 #00000000, stop:1 #00000000)",
        "font-color": "#d8d2ed",
        
        "progress-color": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e48d8d, stop:0.16 #eca864, stop:0.33 #efe87c, stop:0.5 #a5e8a5, stop:0.66 #7ce8ef, stop:0.83 #7c9fef, stop:1 #a57cef)",
        "progress-line-color": "#00000000",
        # "font-family": "Neoneon",
        "font-family": "fonts/ChangelingNeoInline.otf",
        "font-size": "33px",
        
        "line-width": 0.25,
        "line-color": "#9f93cc",
        
        "shadow-color": "#d8d2ed",
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() == "charli xcx" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["backseat", "out of my head", "lucky", "tears", "i got it", "femmebot", "delicious", "unlock it", "porsche", "track 10"]]))
        
    },
    "vroom vroom": {
        "font-color": "#0000000099",
        # "font-family": "Rawhide Raw 2012",
        "font-family": "fonts/RawhideRaw2012.ttf",
        "font-size": "27px",
        
        "line-color": "#e3e3e3",
        "line-width": 1.1,
        
        "shadow-color": "#757575",
        "shadow-offset": [1.5, 1.5],
        "shadow-radius": 3,
        
        "rule": lambda track: (track.artist.lower() == "charli xcx" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["vroom vroom", "paradise", "trophy", "secret"]])),
        
        "format": lambda line: "".join([_ for _ in line if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-"]).upper().replace("R ", "r ")
    }
}