STYLES = {
    "dtmf": {
        "background": {
            "image": "images/dtmf.png",
        },
        "font": {
            "color": "#d22b01",
            # "image": "images/dtmftext.png",
            "family": "fonts/DtMF.ttf",
            "size": "30px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "enabled": False,
        },
        "match": {
            "artist": ["bad bunny"],
            "title_any": [
                "nuevayol",
                "voy a llevarte pa pr",
                "baile inolvidable",
                "perfumito nuevo",
                "weltita",
                "veldá",
                "el clúb",
                "ketu tecré",
                "bokete",
                "kloufrens",
                "turista",
                "café con ron",
                "pitorro de coco",
                "lo que le pasa a hawaii",
                "eoo",
                "dtmf",
                "la mudanza",
            ],
        },
        # replace non-alphanumeric characters (except all the music symbols, pause symbol) with space, then make sure only one space exists between words, then strip leading/trailing spaces
        "format": lambda line: " ".join(
            c
            for c in "".join(
                c if c.isalnum() or c in "áéíóúü" else " " for c in line
            ).split(" ")
            if c.strip() != ""
        ).replace("ü", "u"),
    }
}
