#### Default Theme
STYLES = {
    "white": {
        "background": {
            "color": "#00000000",
        },
        "font": {
            "color": "qradialgradient(spread:reflect, mode:logical, cx:50, cy:0, radius:40, stop:0 #ffffffaa, stop:1 #ffffff)",
            "family": "SF Pro Display, Spotify Mix, Arial, Microsoft YaHei UI",
            "size": "30px",
            "weight": "bold",
            "italic": False,
        },
        "line": {
            "color": "#ffffffaa",
            "width": 0,
        },
        "shadow": {
            "enabled": True,
            "color": "#ffffff",
            "offset": [0, 0],
            "radius": 10,
        },
        "text": {
            "flip": False,
        },
        "animation": {
            "entering": "fadein",
            "sustaining": "flickering",
            "leaving": "fadeout",
        },
    },
    "black": {
        "background": {
            "color": "#00000000",
        },
        "font": {
            "color": "qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #00000000, stop:0.1 #000000, stop:0.6 #000000, stop:1 #00000000)",
            "family": "SF Pro Display, Spotify Mix, Arial, Microsoft YaHei UI",
            "size": "30px",
            "weight": "bold",
            "italic": False,
        },
        "line": {
            "color": "#7c7c7c",
            "width": 2,
        },
        "shadow": {
            "enabled": True,
            "color": "#000000",
            "offset": [0, 0],
            "radius": 5,
        },
        "text": {
            "flip": False,
        },
        "animation": {
            "entering": "fadein",
            "sustaining": "flickering",
            "leaving": "fadeout",
        },
    },
    "pink": {
        "background": {
            "color": "#00000000",
        },
        "font": {
            "color": "qlineargradient(spread:pad, x1:0, y1:0.55, x2:1, y2:0.45, stop:0 #e3a0b7, stop:1 #bbbbbb)",
            "family": "SF Pro Display, Spotify Mix, Arial, Microsoft YaHei UI",
            "size": "30px",
            "weight": "bold",
            "italic": False,
        },
        "progress": {
            "line_color": "#00000000",
        },
        "line": {
            "color": "#ce6f72",
            "width": 0.3,
        },
        "shadow": {
            "enabled": True,
            "color": "#e3a0b7",
            "offset": [0, 0],
            "radius": 9,
        },
        "text": {
            "flip": False,
        },
        "animation": {
            "entering": "fadein",
            "sustaining": "flickering",
            "leaving": "fadeout",
        },
    },
    "LyricBar theme": {
        "background": {
            "color": "#00000000",
        },
        "font": {
            "color": "qlineargradient(spread:pad, x1:0, y1:0.55, x2:1, y2:0.45, stop:0 #e3a0b7, stop:1 #bbbbbb)",
            "family": "Spotify Mix, SF Pro Display, Spotify Mix, Arial, Microsoft YaHei UI",
            "size": "32px",
            "weight": "black",
            "italic": False,
        },
        "progress": {
            "line_color": "#00000000",
        },
        "line": {
            "color": "#ce6f72",
            "width": 0.3,
        },
        "shadow": {
            "enabled": True,
            "color": "#e3a0b7",
            "offset": [0, 0],
            "radius": 9,
        },
        "text": {
            "flip": False,
        },
        "animation": {
            "entering": "fadein",
            "sustaining": "flickering",
            "leaving": "fadeout",
        },
    },
    # "LyricBar theme": {
    #     # "background-color": "#00000000",
    #     "background-color": "qradialgradient(spread:pad, mode:logical, cx:width/2, cy:height/2, radius:height/2+width/4, fx:width/2, fy:(height/2+width/4)/5*3, stop:0 #ffffff88, stop:0.15 #ffffff88, stop:0.3 #2e749555, stop:0.6 #2e7495aa, stop:1 #00000000)",
    #     "font-image": "images/wave.png",
    #     "font-family": "fonts/AsturoGrandSerif-Regular.otf",
    #     # "font-family": "SF Pro Display, Spotify Mix, Arial, Microsoft YaHei UI",
    #     "font-size": "37px",
    #     "font-weight": "bold",
    #     "font-italic": True,
    #     "line-color": "#000000",
    #     "line-width": 0,
    #     "use-shadow": True,
    #     "shadow-color": "#000000",
    #     "shadow-offset": [3, 3],
    #     "shadow-radius": 5,
    #     # "progress-line-color": "#00000000",
    #     # "progress-line-color": "#00000000",
    #     # "progress-color": "#00000000",
    #     "flip-text": False,
    #     "entering": "fadein",
    #     # "entering": "bottomslidein",
    #     "sustaining": "flickering",
    #     "leaving": "fadeout"
    #     # "leaving": "topslideout"
    # }
    # "LyricBar theme": {
    #     "background-color": "#00000000",
    #     "font-image": "images/flame.png",
    #     # "font-color": "qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 #e3a0b7ff, stop:1 #bbbbffaa)",
    #     # "font-color": "qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 #000000, stop:0.4 #000000, stop:0.5 #f5e943, stop:0.6 #f5e943, stop:0.7 #e01818)",
    #     "font-family": "fonts/Poultrygeist.ttf",
    #     # "font-family": "SF Pro Display, Spotify Mix, Arial, Microsoft YaHei UI",
    #     "font-size": "37px",
    #     "font-weight": "bold",
    #     "font-italic": False,
    #     "line-color": "#e4c946aa",
    #     "line-width": 2,
    #     "use-shadow": True,
    #     "shadow-color": "#e4c946",
    #     "shadow-offset": [0, 0],
    #     "shadow-radius": 0,
    #     # "progress-line-color": "#e4c946aa",
    #     # "progress-color": "#991e0f",
    #     "progress-line-color": "#00000000",
    #     "progress-color": "#00000000",
    #     "flip-text": False,
    #     # "entering": "fadein",
    #     "entering": "zoomin",
    #     "sustaining": None,
    #     "leaving": "fadeout"
    #     # "leaving": "zoomout"
    # }
}
