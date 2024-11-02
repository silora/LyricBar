STYLES = {
    "hikaru utada": {
        "font-image": "images/hikaruutada.png",
        
        "font-weight": "bold",
        
        "line-color": "#d4dfef",
        "line-width": 0,
        
        "use-shadow": False,
        "shadow-color": "#d4dfef",
        "shadow-radius": 5,
        "shadow-offset": [2, 2],
        
        "rule": lambda track: (track.artist.lower() in ["宇多田ヒカル", "hikaru utada", "宇多田光", "utada"])
    }
}