STYLES = {
    "vampire weekend": {
        "font-color": "#ff7d32",
        "font-family": "Futura",
        
        "line-color": "#ffffff",
        "line-width": 0,
        
        "shadow-color": "#ffffff",
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() == "vampire weekend")
    }
}