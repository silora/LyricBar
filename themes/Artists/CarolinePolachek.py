STYLES = {
    "caroline polachek": {
        "background-image": "images/carolinepolachek.png",
        "font-family": "Sinistre",
        "font-size": "35px",
        "font-color": "#704212",
        
        "line-color": "#adadad",
        "line-width": 0,
        
        "shadow-color": "#704212",
        "shadow-offset": [0, 0],
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() in ["caroline polachek", "chairlift"])
    }
}