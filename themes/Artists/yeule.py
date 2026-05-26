def yeule_style(line):
    original = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    output = "ѧ𝛃ℂᴰ∃ፑᏀਮ𝕀لԟᒶṂℕ❍𝕡ℚ℟ᎦT⨿ᐺሡㄨ𝕐Ꮓ𝖆ƀ𝘤Ժ𝘦𝖋ցħɨڵꝂ╽₥դØᵱᒅ𝐫ક𝕥նᏤ⍵𝕏Ỿ𝐳"
    ret = ""
    line = line.replace("Softscars", "ₛof̷̢̨̛̙̦̮͖̘͍͆♰ꙅᶜà̵̡͈̥͚́̽͛̍̕͘ ̺ ̝ ʳₛ").replace(
        "softscars", "ₛof̷̢̨̛̙̦̮͖̘͍͆♰ꙅᶜà̵̡͈̥͚́̽͛̍̕͘ ̺ ̝ ʳₛ"
    )
    for char in line:
        if char in original:
            ret += output[original.index(char)]
        elif char == " ":
            ret += "  "
        else:
            ret += char
    return ret


STYLES = {
    "yeule": {
        "font": {
            "color": "#97befc",
            "family": "Times New Roman, Gadugi",  # Times New Roman,  , sans-serif
            # "weight": "regular",
        },
        "match": {"artist": "yeule"},
        "format": yeule_style,
    }
}
