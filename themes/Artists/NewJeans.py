STYLES = {
    "newjeans": {
        "background-image": "images/newjeans.png",
        
        "font-family": "Binggrae",
        "font-size": "35px",
        "font-color": "#b6d6ed",
        
        "line-color": "#364551",
        "line-width": 3,
        
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() == "newjeans")
    }
}