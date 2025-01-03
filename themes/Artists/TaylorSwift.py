STYLES = {
    "folklore": {
        "background-color": "qradialgradient(spread:pad, cx:0.5, cy:0.9, radius:0.4, fx:0.5, fy:0.9, stop:0 #eeeeee, stop:0.5 #eeeeee88, stop:1 #00000000)",
        
        "font-family": "fonts/IMFellDWPica-Italic.ttf",
        # "font-color": "qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 #323232, stop:0.7 #eeeeee, stop:1 #eeeeee)",
        "font-color": "#eeeeee",
        
        "line-width": 0,
        "line-color": "#eeeeee",
        
        "shadow-color": "#eeeeee",
        "shadow-radius": 5,
        
        "rule": lambda track: (track.artist.lower() == "taylor swift" and any([_ in track.title.lower().lower().replace("‘", "'").replace("’", "'") for _ in ["the 1", "cardigan", "the last great american dynasty", "exile", "my tears ricochet", "mirrorball", "seven", "august", "this is me trying", "illicit affairs", "invisible string", "mad woman", "epiphany", "betty", "peace", "hoax", "the lakes", "willow", "champagne problems", "gold rush", "'tis the damn season", "tolerate it", "no body, no crime", "happiness", "dorothea", "coney island", "ivy", "cowboy like me", "long story short", "marjorie", "closure", "evermore", "right where you left me", "it's time to go"]]))
        
    }
}