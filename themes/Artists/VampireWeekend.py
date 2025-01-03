STYLES = {
    "vampire weekend": {
        "font-color": "#ff7d32",
        # "font-family": "Futura",
        "font-family": "fonts/Futura.otf",
        
        "line-color": "#ffffff",
        "line-width": 0,
        
        "shadow-color": "#ffffff",
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() == "vampire weekend")
    }
}