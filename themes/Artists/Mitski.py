STYLES = {
    "the land is inhospitable": {
        "background-image": "images/thelandisinhospitable.png",
        
        "font-family": "Tofino Pro Personal",
        "font-color": "#000000",
        
        "line-width": 0.75,
        "line-color": "#000000",
        
        "shadow-color": "#f6e3d4",
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() == "mitski" and (any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["bug like an angel", "buffalo replaced", "heaven", "i don't like my mind", "the deal", "when memories snow", "my love mine all mine", "the frost", "i'm your man", "i love me after you"]]) or any([_ == track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["star"]]))),
        
        "format": lambda x: x.upper()
    },
    "laurel hell": {
        "background-image": "images/laurelhell.png",
        
        "font-family": "Laurel Hell Hand2",
        "font-color": "#ffffff",
        "font-size": "35px",
        
        "line-width": 0,
        
        "shadow-color": "#ffffff",
        
        "rule": lambda track: (track.artist.lower() == "mitski" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["valentine, texas", "working for the knife", "the only heartbreaker", "stay soft", "everyone", "heat lightning", "the only heartbreaker", "love me more", "there's nothing left for you", "should've been me", "i guess", "that's our lamp"]])),
        
        "format": lambda x: x.replace(" ", "    ")
    },
    "be the cowboy": {
        "background-image": "images/bethecowboy.png",
        
        "font-family": "SantoroScriptJF",
        "font-size": "40px",
        "font-color": "#00000000",
        
        "line-width": 0.75,
        "line-color": "#FFFFFF",
        
        "use-color": False,
        # "shadow-color": "#FFFFFF",
        "sustaining": "zooming",
        
        "rule": lambda track: (track.artist.lower() == "mitski" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["geyser", "why didn't you stop me?", "old friend", "a pearl", "lonesome love", "remember my name", "me and my husband", "come into the water", "nobody", "pink in the night", "a horse named cold air", "washing machine heart", "blue light", "two slow dancers"]])),
    },
    "puberty 2": {
        "background-image": "images/puberty2.png",
        
        "font-family": "Edwardian Script ITC",
        "font-image": "images/puberty2text.png",
        "font-size": "50px",
        "font-weight": "black",
        
        "line-width": 0,
        
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() == "mitski" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["happy", "dan the dancer", "once more to see you", "fireworks", "your best american girl", "i bet on losing dogs", "my body's made of crushed little stars", "thursday girl", "a loving feeling", "crack baby", "a burning hill"]]))
    },
    "bury me at makeout creek": {
        "background-image": "images/burymeatmakeoutcreek.png",
        
        "font-family": "Times New Roman",
        "font-size": "25px",
        "font-color": "#000000",
        # "shadow-color": "#FFFFFF",
        
        "line-color": "#000000",
        "line-width": 0.25,
        
        "use-shadow": False,
        
        "entering": "rightslidein",
        "sustaining": "",
        "leaving": "leftslideout",
        
        "rule": lambda track: (track.artist.lower() == "mitski" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["texas reznikoff", "townie", "first love/late spring", "francis forever", "i don't smoke", "jobless monday", "drunk walk home", "i will", "carry me out", "last words of a shooting star"]])),
        
        "format": lambda line: line.replace(" ", "  ")
    },
    "retire from sad": {
        "background-image": "images/retirefromsad.png",
        
        "font-family": "Nimbus Sans", #should be Nimbus Sans Round tho... i don't have that font
        "font-weight": "black",
        "font-color": "#ffffff",
        
        "line-width": 0,
        
        "shadow-color": "#ffffff",
        
        "rule": lambda track: (track.artist.lower() == "mitski" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["goodbye, my danish sweetheart", "square", "strawberry blond", "humpty", "i want you", "because dreaming costs money, my dear", "circle", "class of 2013"]]))
    },
    "lush": {
        "background-image": "images/lush.png",
        
        "font-family": "Avenir LT Std 35 Light",
        "font-color": "#ffffff",
        "font-weight": "light",
        "line-width": 0,
        "shadow-color": "#ffffff",
        
        "rule": lambda track: (track.artist.lower() == "mitski" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["liquid smooth", "wife", "abbey", "brand new city", "eric", "bag of bones", "door", "pearl driver", "real men"]])),
        
        "format": lambda x: x.upper()
        
    }
}