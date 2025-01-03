import math
import subprocess


def hex_to_rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    if lv % 3 == 0:
        return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)) + (alpha,)
    elif lv == 8:
        return tuple(int(hex_color[i:i + 2], 16) for i in range(0, 8, 2))
    return (0,0,0,0)

def ms_to_mm_ss(ms):
    seconds = ms // 1000
    minutes = math.floor(seconds // 60)
    seconds = math.floor(seconds % 60)
    return f"{minutes:02}:{seconds:02}"


def check_if_windows_locked():
    process_name='LogonUI.exe'
    callall='TASKLIST'
    outputall=subprocess.check_output(callall)
    outputstringall=str(outputall)
    return process_name in outputstringall