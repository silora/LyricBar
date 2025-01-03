def twotwo_a_million(line):
    original = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    output = "Δв¢dэfgнîJкLми◊pQя$†Ʊv₩Xyz"
    ret = ""
    line = line.upper()
    line.replace("OO", "∞")
    for char in line.upper():
        if char in original:
            ret += output[original.index(char)]
        else:
            ret += char
    return ret
STYLES = {
    "22, a million": {
        "foreground-image": "images/22amillion.png",
        
        "font-color": "#ffffff",
        "font-family": "Times New Roman, sans-serif, Gadugi",
        # "font-family": "Helvetica",
        "font-size": "30px",
        
        "line-width": 0,
        
        "shadow-color": "#ffffff",
        # "shadow-offset": [2, 2],
        "shadow-radius": 5,
        
        "rule": lambda track: (track.artist.lower() == "bon iver" and any([_.lower() in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["22", "10", "715", "33", "29", "666", "21", "8", "45", "00000"]])),
        
        # "format": twotwo_a_million
    }
}