STYLES = {
    "sos": {
        "background-image": "images/sos.png",
        
        # "font-family": "Superstar M54",
        "font-family": "fonts/SuperstarM54.ttf",
        "font-color": "#ffffff44",
        
        "line-width": 0.5,
        "line-color": "#ffffff",
        
        "shadow-color": "#ffffff",
        
        "entering": "topslidein",
        "leaving": "bottomslideout",
        "sustaining": "vshaking",    
        
        "rule": lambda track: (track.artist.lower() == "sza" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["sos", "kill bill", "seek & destroy", "low", "love language", "blind", "used", "snooze", "notice me", "gone girl", "smoking on my ex pack", "ghost in the machine", "f2f", "nobody gets me", "conceited", "special", "too late", "far", "shirt", "open arms", "i hate u", "good days", "forgiveless"]]))
    },
    "ctrl": {
        "background-image": "images/ctrl.png",
        
        # "font-family": "Mx437 IBM VGA 8x14",
        "font-family": "fonts/Mx437IBMVGA8x14.ttf",
        "font-color": "#51f57522",
        "font-size": "35px",
        
        "line-width": 0.5,
        "line-color": "#1f7820",
        
        "shadow-color": "#41cc44",
        "shadow-radius": 5,
        
        "entering": "topslidein",
        "leaving": "bottomslideout",
        "sustaining": "hshaking",  
        
        "rule": lambda track: (track.artist.lower() == "sza" and any([_ in track.title.lower().replace("‘", "'").replace("’", "'") for _ in ["supermodel", "love galore", "doves in the wind", "drew barrymore", "prom", "the weekend", "go gina", "garden (say it like dat)", "broken clocks", "anything", "wavy (interlude)", "normal girl", "pretty little birds", "20 something"]]))
    }
}