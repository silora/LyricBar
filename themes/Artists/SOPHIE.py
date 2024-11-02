STYLES = {
    "sophie": {
        "background-image": "images/sophie.png",
        
        "font-color": "#ffffffbb",
        "font-family": "Jean",
        "font-size": "40px",
        "font-weight": "bold",
        
        "line-width": 1,
        "line-color": "#ffffffaa",
        
        "shadow-color": "#ffffff66",
        "shadow-radius": 5,
        "shadow-offset": [-3, -3],
        
        "rule": lambda track: (track.artist.lower() == "sophie")
    }
}