STYLES = {
    "post": {
        "font-color": "#d58fe8",
        "font-family": "Bjork",
        "font-size": "40px",
        
        "line-color": "#a22929",
        "line-width": 1,
        
        "shadow-color": "#a22929",
        "shadow-offset": [2, 2],
        "shadow-radius": 8,
        
        "rule": lambda track: (track.artist.lower() in ["bjork", "björk"] and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["army of me", "hyperballad", "hyper-ballad", "the modern things", "it's oh so quiet", "enjoy", "you've been flirting again", "isobel", "possibly maybe", "i miss you", "cover me", "headphones"]])),
        
        "format": lambda line: "".join([_ for _ in line if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ♬"])
    },
    "vespertine": {
        "font-color": "#ffffff",
        "font-family": "vespertine",
        "font-size": "50px",
        
        "line-width": 0,
        
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() in ["bjork", "björk"] and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["hidden place", "cocoon", "it's not up to you", "undo", "pagan poetry", "frosti", "aurora", "an echo, a stain", "sun in my mouth", "heirloom", "harm of will", "unison", "stonemilker", "lionsong", "history of touches", "black lake", "family", "notget", "atom dance", "mouth mantra", "quicksand"]]))
    }
}