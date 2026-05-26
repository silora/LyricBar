STYLES = {
    "sexistential": {
        "background": {
            "image": "images/sexistential.png",
        },
        "font": {
            # "family": "Superstar M54",
            "family": "fonts/ControlUpright.ttf",
            "color": "#ffffff",
            "size": "30px",
        },
        "line": {
            "width": 0,
            "color": "#ffffff",
        },
        "shadow": {
            "color": "#ffffff",
            "radius": 5,
        },
        "animation": {
            "entering": "",
            "leaving": "",
            "sustaining": "",
        },
        "match": {
            "artist": "robyn",
            "title_any": [
                "really real",
                "dopamine",
                "blow my mind",
                "sucker for love",
                "it don't mean a thing",
                "talk to me",
                "sexistential",
                "light up",
                "into the sun",
            ],
        },
        ### add a space every 3-5 characters (randomly)
        "format": lambda line: " ".join(
            [
                line.replace(" ", "  ")[i : i + (3 + hash(line.replace(" ", "  ")) % 3)]
                for i in range(
                    0,
                    len(line.replace(" ", "  ")),
                    3 + hash(line.replace(" ", "  ")) % 3,
                )
            ]
        ),
    }
}
