STYLES = {
    "eusexua": {
        "background-image": "images/eusexua.png",
        
        "font-family": "OBG EUSEXUA 2024",
        "font-size": "30px",
        "font-color": "#ffffff",
        
        "line-color": "#000000",
        "line-width": 0,
        
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() == "fka twigs" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["eusexua", "perfect stranger"]])),
        
        "format": lambda line: line.upper().replace("‘", "").replace("’", "").replace("'", "")
    }
}