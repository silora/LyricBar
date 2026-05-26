STYLES = {
    "arca": {
        "font": {
            "color": "#ffffffaa",
            # "family": "KiCk",
            "family": "fonts/KiCk.otf",
            "size": "50px",
        },
        "line": {
            "color": "#858585",
            "width": 0,
        },
        "shadow": {
            "enabled": False,
            # "color": "white",
        },
        "match": {"artist": "arca"},
        "format": lambda line: line.replace("ñ", "n")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u"),
    }
}
