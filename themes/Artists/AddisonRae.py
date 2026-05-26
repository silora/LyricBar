def cap_first_n_last(line):
    """Capitalize the first and last character of a string."""
    if len(line) < 2:
        return line.upper()
    return line[0].upper() + line[1:-1] + line[-1].upper()


STYLES = {
    "addison": {
        "background": {
            "image": "images/addison.png",
        },
        "font": {
            "color": "#00b7fe",
        ## left to right 0eafe3 cec95a b6567b
            # "color": "qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #00b7fe, stop:0.5 #cece5a, stop:1 #b6567b)",
            "family": "fonts/MorticiaNF.ttf",
            "size": "35px",
        },
        "line": {
            # "color": "#858585",
            "width": 0,
        },
        "shadow": {
            "enabled": False,
            # "color": "white",
        },
        "match": {"artist": "addison rae"},
        "format": cap_first_n_last,
    }
}
