STYLES = {
    "i see you": {
        "font-image": "images/iseeyou.png",
        "font-weight": "bold",
        
        "line-color": "#adadad",
        "line-width": 0,
        
        "rule": lambda track: (track.artist.lower() in ["the xx"])
    }
}