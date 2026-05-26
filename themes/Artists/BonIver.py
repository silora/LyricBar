def twotwo_a_million(line):
    original = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    output = "Δв¢dэfgнîJкLми◊pQя$†Ʊv₩Xyz"
    ret = ""
    line = line.upper()
    line.replace("OO", "âˆž")
    for char in line.upper():
        if char in original:
            ret += output[original.index(char)]
        else:
            ret += char
    return ret


STYLES = {
    "22, a million": {
        "foreground": {
            "image": "images/22amillion.png",
        },
        "font": {
            "color": "#ffffff",
            "family": "Times New Roman, sans-serif, Gadugi",
            # "family": "Helvetica",
            "size": "30px",
        },
        "line": {
            "width": 0,
        },
        "shadow": {
            "color": "#ffffff",
            # "offset": [2, 2],
            "radius": 5,
        },
        "match": {
            "artist": "bon iver",
            "title_any": [
                "22",
                "10",
                "715",
                "33",
                "29",
                "666",
                "21",
                "8",
                "45",
                "00000",
            ],
        },
        # "format": twotwo_a_million
    }
}
