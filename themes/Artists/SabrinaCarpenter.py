STYLES = {
    "sabrina carpenter": {
        "background-color": "qradialgradient(spread:repeat, cx:0.5, cy:-0.5, radius:1, fx:0.5, fy:0, stop:0 #20199b, stop:1 #00000000)",
        "font-family": "Century-Old-Style",
        "font-color": "#dcca87",
        
        "rule": lambda track: (track.artist.lower() == "sabrina carpenter"),
        
        "entering": "zoomin"
    }
}