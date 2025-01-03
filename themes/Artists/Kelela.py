STYLES = {
    "raven": {
        "background-image": "images/raven.png",
        
        # "font-family": "Engravers' Gothic",
        "font-family": "fonts/EngraversGothic.otf",
        "font-size": "30px",
        "font-color": "#1e1e1eaa",
        
        "line-color": "#1e1e1eaa",
        "line-width": 1,
        
        "shadow-color": "#9c9c9c",
        "shadow-offset": [-2, -2],
        
        "rule": lambda track: (track.artist.lower() == "kelela" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["washed away", "happy ending", "let it go", "on the run", "missed call", "closure", "contact", "fooley", "holier", "raven", "bruises","sorbet", "divorce", "enough for love", "far away" ]])),
        "format": lambda x: x.upper()
    }
}