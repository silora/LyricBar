STYLES = {
    "trick": {
        "background-image": "images/trick.png",
        
        # "font-family": "Hor",
        "font-family": "fonts/Hor.ttf",
        "font-color": "#90fcfa",
        
        "line-width": 0,
        
        "shadow-color": "#000000",
        "shadow-offset": [3, 3],
        "shadow-radius": 7,
        
        "rule": lambda track: (track.artist.lower() == "alex g" and (any([_ == track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["memory", "forever", "animals", "string", "advice", "people", "whale", "trick", "kute", "so", "mary", "change", "clouds", "adam", "sarah", "16 mirrors"]]))),
                               
        "format": lambda x: x.upper()
    }
}