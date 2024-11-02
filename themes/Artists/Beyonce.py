STYLES = {
    "renaissance": {
        "font-color": "#e0e0e0",
        "font-family": "Roboto Mono",
        "font-size": "25px",
        "font-weight": "light",
        
        "line-width": 0.3,
        
        "rule": lambda track: (track.artist.lower() in ["beyonce", "beyoncé"] and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["i'm that girl", "cozy", "alien superstar", "cuff it", "energy", "break my soul", "church girl", "plastic off the sofa", "virgo's groove", "move", "heated", "thique", "all up in your mind", "america has a problem", "pure/honey", "summer renaissance", "ameriican requiem", "blackbiird", "16 carriages", "protector", "my rose", "smoke hour", "texas hold 'em", "bodyguard", "dolly p", "jolene", "daughter", "spaghettii", "alliigator tears", "smoke hour ii", "just for fun", "ii most wanted", "levii's jeans", "flamenco", "the linda martell show", "ya ya", "oh louisiana", "desert eagle", "riiverdance", "ii hands ii heaven", "tyrant", "sweet ★ honey ★ buckiin'", "amen"]])),
        
        "format": lambda line: line.upper()
    }
}