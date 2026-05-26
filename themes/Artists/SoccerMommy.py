STYLES = {
    "color theory": {
        "background": {
            # "image": "images/soccermommy.png",
        },
        "font": {
            # "family": "Pixelon",
            "family": "fonts/Pixelon.ttf",
            "color": "#e8cdcdaa",
            "size": "30px",
        },
        "line": {
            # "color": "#8e0d1d88",
            "width": 0.5,
        },
        "shadow": {
            "color": "#2d7879",
            "radius": 5,
            "offset": [-2, -2],
        },
        "format": lambda line: "".join(
            [
                _
                for _ in line
                if _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ♬"
            ]
        ),
        "match": {"artist": "soccer mommy"},
    }
}
