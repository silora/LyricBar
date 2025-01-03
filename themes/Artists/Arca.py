STYLES = {
    "arca": {
        "font-color": "black",
        # "font-family": "KiCk",
        "font-family": "fonts/KiCk.otf",
        "font-size": "60px",
        
        "line-color": "#858585",
        "line-width": 2,
        
        "shadow-color": "white",
        
        "rule": lambda track: (track.artist.lower() == "arca"),
        
        "format": lambda line: line.replace("ñ", "n").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    }
}