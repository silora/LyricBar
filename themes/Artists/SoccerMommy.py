STYLES = {
    "color theory": {
        # "background-image": "images/soccermommy.png",
        
        # "font-family": "Pixelon",
        "font-family": "fonts/Pixelon.ttf",
        "font-color": "#e8cdcdaa",
        "font-size": "30px",
        
        # "line-color": "#8e0d1d88",
        "line-width": 0.5,
        
        "shadow-color": "#2d7879",
        "shadow-radius": 5,
        "shadow-offset": [-2, -2],
        
        "format": lambda line: "".join([_ for _ in line if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ♬"]),
        "rule": lambda track: (track.artist.lower() == "soccer mommy")
    }
}