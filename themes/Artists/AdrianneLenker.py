STYLES = {
    "adrianne lenker": {
        "background-image": "images/adriannelenker.png",
        
        "font-image": "images/adriannelenkertext.png",
        # "font-color": "#00000000",
        "font-weight": "bold",
        
        "line-width": 0,
        "line-color": "#ffffff88",
        
        "use-shadow": False,
        "shadow-color": "#000000",
        "shadow-radius": 10,
        "shadow-offset": [0, 3],
        
        "rule": lambda track: (track.artist.lower() == "adrianne lenker")
    }
}