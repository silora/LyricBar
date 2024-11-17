STYLES = {
    "immunity": {
        "background-image": "images/immunity.png",
        
        "font-family": "Astloch",
        "font-color": "#f3f2ef",
        "font-weight": "bold",
        "font-size": "40px",
        
        "line-width": 0,
        
        "shadow-color": "#bbb4a4",
        "shadow-radius": 10,
        
        "rule": lambda track: (track.artist.lower() == "clairo" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["alewife", "impossible", "closer to you", "north", "bags", "softly", "sofia", "white flag", "feel something", "sinking", "i wouldn't ask you"]]))
    },
    "charm": {
        "background-color": "qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #43340d, stop:1 #2a1502)",
        
        "font-family": "Xaltid",
        "font-color": "#8b893f",
        "font-weight": "bold",
        "font-size": "40px",
        
        "line-width": 0,
        
        "shadow-color": "#8b893f",
        
        "rule": lambda track: (track.artist.lower() == "clairo" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["nomad", "sexy to someone", "second nature", "slow dance", "thank you", "terrapin", "juna", "add up my love", "echo", "glory of the snow", "pier 4"]]))
    }
}