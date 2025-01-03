STYLES = {
    "sabrina carpenter": {
        "background-color": "#20199b",
        # "font-family": "Century-Old-Style",
        "font-family": "fonts/CenturyOldStyle-Bold.ttf",
        "font-color": "#dcca87",
        
        "rule": lambda track: (track.artist.lower() == "sabrina carpenter"),
        
        "entering": "zoomin"
    }
}