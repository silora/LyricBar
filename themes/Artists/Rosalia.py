STYLES = {
    "motomami": {
        "background-color": "qradialgradient(spread:pad, mode:logical, cx:width/2, cy:height/2, radius:height/2+width/4, fx:width/2, fy:height/2, stop:0 #ffffff, stop:0.45 #ffffff, stop:0.5 #00000000, stop:0.51 #ffffff, stop:0.6 #00000000, stop:0.61 #ffffff, stop:1 #00000000)",
        
        "font-color": "#FF0000",
        # "font-family": "Motomami",
        "font-family": "fonts/Motomami.ttf",
        "font-size": "65px",
        
        "line-color": "#ffffff",
        "line-width": 3,

        "shadow-color": "#FF0000",
        "shadow-offset": [0, 0],
        "shadow-radius": 30,
        
        "format": lambda line: line.replace("motomami", "MoToMaMi").replace("Motomami", "MoToMaMi").replace("MOTOMAMI", "MoToMaMi"),
        
        "rule": lambda track: (track.artist.lower() in ["rosalia", "rosalía"] and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["saoko", "candy", "la fama", "bulería", "buleria", "chicken teriyaki", "hentai", "bizcochito", "g3 n15", "motomami", "diablo", "delirio de grandeza", "cuuuuuuuuuute", "como un g", "abcdefg", "la combi versace", "sakura", "thank yu :)", "despechá", "despecha", "aislamiento", "la kilié", "la kilie", "lax", "chiri"]]))
    }
}