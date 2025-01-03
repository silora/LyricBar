from PyQt5.QtGui import QColor, QGradient, QLinearGradient, QRadialGradient, QConicalGradient
import regex as re

from ...utils.tools import hex_to_rgba


def calculate(s, **kwargs):
    for key in kwargs:
        s = s.replace(key, str(kwargs[key]))
    try:
        result = eval(s)
    except Exception as e:
        result = 0
    return result


def convert_to_color(color, **kwargs):
    if isinstance(color, QColor):
        return color
    if isinstance(color, QGradient):
        return color
    if isinstance(color, tuple):
        return QColor(*color)
    if isinstance(color, str) and color.startswith("rgb("):
        color = color.replace("rgb(", "").replace(")", "").split(", ")
        return QColor(int(color[0]), int(color[1]), int(color[2]))
    if isinstance(color, str) and color.startswith("rgba("):
        color = color.replace("rgba(", "").replace(")", "").split(", ")
        return QColor(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
    if isinstance(color, str) and color.startswith("#"):
        return QColor(*hex_to_rgba(color))
    if isinstance(color, str) and any([color.startswith(_) for _ in ["qlineargradient", "qradialgradient", "qconicalgradient"]]):
        g = None
        if color.startswith("qlineargradient"):
            g = QLinearGradient()
            x1 = calculate(re.search(r"x1:([^,]+)", color).group(1), **kwargs)
            y1 = calculate(re.search(r"y1:([^,]+)", color).group(1), **kwargs)
            x2 = calculate(re.search(r"x2:([^,]+)", color).group(1), **kwargs)
            y2 = calculate(re.search(r"y2:([^,]+)", color).group(1), **kwargs)
            g.setStart(x1, y1)
            g.setFinalStop(x2, y2)
            
            
        elif color.startswith("qradialgradient"):
            g = QRadialGradient()
            cx = calculate(re.search(r"cx:([^,]+)", color).group(1), **kwargs)
            cy = calculate(re.search(r"cy:([^,]+)", color).group(1), **kwargs)
            if "fx:" in color:
                fx = calculate(re.search(r"fx:([^,]+)", color).group(1), **kwargs)
            else:
                fx = cx
            if "fy:" in color:
                fy = calculate(re.search(r"fy:([^,]+)", color).group(1), **kwargs)
            else:
                fy = cy
            radius = calculate(re.search(r"radius:([^,]+)", color).group(1), **kwargs)
            g.setCenter(cx, cy)
            g.setFocalPoint(fx, fy)
            g.setRadius(radius)
            # g.setCenterRadius(radius)
            
            focalradius = re.search(r"focalradius:([^,]+)", color)
            if focalradius is not None:
                g.setFocalRadius(calculate(focalradius.group(1), **kwargs))
            else:
                g.setFocalRadius(-0.15)
            
        elif color.startswith("qconicalgradient"):
            g = QConicalGradient()
            cx = calculate(re.search(r"cx:([^,]+)", color).group(1), **kwargs)
            cy = calculate(re.search(r"cy:([^,]+)", color).group(1), **kwargs)
            angle = calculate(re.search(r"angle:([^,]+)", color).group(1), **kwargs)
            g.setCenter(cx, cy)
            g.setAngle(angle)
        
        spread = re.search(r"spread:(\w+)", color)
        if spread is None:
            spread = "pad"
        else:
            spread = spread.group(1)
        if spread == "reflect":
            g.setSpread(QGradient.Spread.ReflectSpread)
        elif spread == "repeat":
            g.setSpread(QGradient.Spread.RepeatSpread)
        else:
            g.setSpread(QGradient.Spread.PadSpread)
            
        mode = re.search(r"mode:(\w+)", color)
        if mode is None:
            mode = "object"
        else:
            mode = mode.group(1)
        if mode == "logical":
            g.setCoordinateMode(QGradient.CoordinateMode.LogicalMode)
        elif mode == "stretch":
            g.setCoordinateMode(QGradient.CoordinateMode.StretchToDeviceMode)
        elif mode == "bounding":
            g.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        else:
            g.setCoordinateMode(QGradient.CoordinateMode.ObjectMode)
            
        
        stops = re.findall(r"stop:([\d\.]+) ([\w#]+|rgb\(\d+, \d+, \d+\)|rgba\(\d+, \d+, \d+, \d+\))(?=[,)])", color)
        for stop in stops:
            pos = float(stop[0])
            if pos < 0.0001:
                pos = 0
            g.setColorAt(min(pos, 1), convert_to_color(stop[1]))
        return g
    if isinstance(color, str):
        return QColor(color)        
        
        