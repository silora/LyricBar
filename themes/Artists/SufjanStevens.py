STYLES = {
    "sufjan stevens": {
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.4, fx:0.5, fy:1, stop:0 #374a50, stop:1 #00000000)",
        
        "font-family": "NimbuSanTBolCon",
        "font-color": "#ffffff",
        "font-size": "45px",
        
        "line-width": 0,
        
        "shadow-color": "#c8e21f",
        "shadow-offset": [2, 2],
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() in ["sufjan stevens", "sisyphus"]),
        
        "entering": "zoomin_overscale"
    }
}