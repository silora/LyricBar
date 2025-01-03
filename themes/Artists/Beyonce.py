STYLES = {
    "renaissance": {
        "background-image": "images/renaissance.png",
        "font-color": "#ffffff",
        # "font-family": "Roboto Mono",
        "font-family": "fonts/RobotoMono-Light.ttf",
        "font-size": "25px",
        "font-weight": "light",
        
        "shadow-color": "#ffffff",
        
        "line-width": 0.3,
        
        "rule": lambda track: (track.artist.lower() in ["beyonce", "beyoncé"] and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["i'm that girl", "cozy", "alien superstar", "cuff it", "energy", "break my soul", "church girl", "plastic off the sofa", "virgo's groove", "move", "heated", "thique", "all up in your mind", "america has a problem", "pure/honey", "summer renaissance"]])),
        
        "format": lambda line: line.upper()
    },
    "cowboy carter": {
        "background-image": "images/cowboycarter.png",
        "foreground-image": "images/cowboycarter_fore.png",
        "font-color": "#e0e0e0",
        # "font-family": "Roboto Mono",
        "font-family": "fonts/RobotoMono-Light.ttf",
        "font-size": "25px",
        "font-weight": "light",
        
        "line-width": 0.3,
        
        "rule": lambda track: (track.artist.lower() in ["beyonce", "beyoncé"] and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["ameriican requiem", "blackbiird", "16 carriages", "protector", "my rose", "smoke hour", "texas hold 'em", "bodyguard", "dolly p", "jolene", "daughter", "spaghettii", "alliigator tears", "smoke hour ii", "just for fun", "ii most wanted", "levii's jeans", "flamenco", "the linda martell show", "ya ya", "oh louisiana", "desert eagle", "riiverdance", "ii hands ii heaven", "tyrant", "sweet ★ honey ★ buckiin'", "amen"]])),
        
        "format": lambda line: line.upper()
    },
    "beyonce": {
        "background-color": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #00000000, stop:0.4 #090b0a, stop:0.6 #090b0a, stop:1 #00000000)",
        
        "font-color": "#d0a8bc",
        "font-family": "fonts/KnockoutHTF66FullFlyweight.otf",
        "font-size": "50px",
        
        "line-width": 0,
        "use-shadow": False,
        
        "rule": lambda track: (track.artist.lower() in ["beyonce", "beyoncé"]) and (any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["pretty hurts", "haunted", "drunk in love", "blow", "no angel", "partition", "jealous", "rocket", "mine", "xo", "flawless", "superpower", "blue", "7/11", "ring off", "standing on the sun"]]) or any([_ == track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["heaven"]])),
        
        "format": lambda line: line.upper()
    }
}