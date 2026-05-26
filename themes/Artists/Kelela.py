STYLES = {
    "raven": {
        "background": {
            "image": "images/raven.png",
        },
        "font": {
            # "family": "Engravers' Gothic",
            "family": "fonts/EngraversGothic.otf",
            "size": "30px",
            "color": "#1e1e1eaa",
        },
        "line": {
            "color": "#1e1e1eaa",
            "width": 1,
        },
        "shadow": {
            "color": "#9c9c9c",
            "offset": [-2, -2],
        },
        "match": {
            "artist": "kelela",
            "title_any": [
                "washed away",
                "happy ending",
                "let it go",
                "on the run",
                "missed call",
                "closure",
                "contact",
                "fooley",
                "holier",
                "raven",
                "bruises",
                "sorbet",
                "divorce",
                "enough for love",
                "far away",
            ],
        },
        "format": lambda x: x.upper(),
    }
}
