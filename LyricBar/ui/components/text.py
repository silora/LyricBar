import re
from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetricsF, QPainterPath


def getTextPath(font, text, alignment):
    for i in range(5):
        font = QFont(font) if isinstance(font, str) else font
        font.setRawMode(True)
        metrics = QFontMetricsF(font)
        line_height = metrics.height()
        lines = text.split("\n")
        widths = [metrics.tightBoundingRect(line).width() for line in lines]
        max_width = max(widths)
        # logging.info(lines)
        path = QPainterPath()
        for idx, line in enumerate(lines):
            if alignment & Qt.AlignmentFlag.AlignLeft:
                path.addText(0, line_height * idx, font, line)
            elif alignment & Qt.AlignmentFlag.AlignRight:
                path.addText(max_width - widths[idx], line_height * idx, font, line)
            else:
                path.addText(
                    (max_width - widths[idx]) / 2, line_height * idx, font, line
                )
        if path.boundingRect().height() >= 3:
            return path
        if path.boundingRect().height() < 3 or i > 0:
            pass
    return None


@dataclass
class Run:
    text: str
    bold: bool | None = None
    italic: bool | None = None
    underline: bool | None = None
    strike: bool | None = None
    scale: float = 1.0


TAG_TOKEN_RE = re.compile(
    r"</?(?:bold|italic|underline|strike|small|big|size)(?:=[0-9]*\.?[0-9]+)?>"
)


SIZE_OPEN_RE = re.compile(r"^<size=([0-9]*\.?[0-9]+)>$")


def strip_tags(s: str) -> str:
    return TAG_TOKEN_RE.sub("", s)


def iter_markup_tokens(markup: str):
    """
    Yield ("text", chunk) or ("tag", tag_text) without the re.split capturing-group problems.
    """
    pos = 0
    for m in TAG_TOKEN_RE.finditer(markup.lower()):
        if m.start() > pos:
            yield ("text", markup[pos : m.start()])
        yield ("tag", m.group(0))
        pos = m.end()
    if pos < len(markup):
        yield ("text", markup[pos:])


def parse_runs(markup: str):
    bold = italic = underline = strike = None
    scale = 1.0
    scale_stack = []

    lines = [[]]

    for kind, tok in iter_markup_tokens(markup):
        if kind == "tag":
            if tok == "<bold>":
                bold = True
                continue
            if tok == "</bold>":
                bold = None
                continue

            if tok == "<italic>":
                italic = True
                continue
            if tok == "</italic>":
                italic = None
                continue

            if tok == "<underline>":
                underline = True
                continue
            if tok == "</underline>":
                underline = None
                continue

            if tok == "<strike>":
                strike = True
                continue
            if tok == "</strike>":
                strike = None
                continue

            if tok == "<small>":
                scale *= 0.8
                scale_stack.append(0.8)
                continue
            if tok == "</small>":
                if scale_stack:
                    scale /= scale_stack.pop()
                continue

            if tok == "<big>":
                scale *= 1.25
                scale_stack.append(1.25)
                continue
            if tok == "</big>":
                if scale_stack:
                    scale /= scale_stack.pop()
                continue

            m = SIZE_OPEN_RE.match(tok)
            if m:
                factor = float(m.group(1))
                scale *= factor
                scale_stack.append(factor)
                continue
            if tok == "</size>":
                if scale_stack:
                    scale /= scale_stack.pop()
                continue

            continue  # unknown tag: ignore safely

        # kind == "text"
        chunks = tok.split("\n")
        for i, chunk in enumerate(chunks):
            if chunk:
                lines[-1].append(
                    Run(
                        chunk,
                        bold=bold,
                        italic=italic,
                        underline=underline,
                        strike=strike,
                        scale=scale,
                    )
                )
            if i != len(chunks) - 1:
                lines.append([])

    return lines


def stronger_bold(weight: int) -> int:
    """
    Escalate font weight when <bold> is applied on already-bold text.
    """
    if weight >= QFont.Weight.Black:
        return weight
    if weight >= QFont.Weight.Bold:
        return QFont.Weight.Black
    return QFont.Weight.Bold


def font_for_run(base_font: QFont, run: Run) -> QFont:
    f = QFont(base_font)

    if run.bold is not None:
        if run.bold:
            base_w = f.weight()
            f.setWeight(stronger_bold(base_w))
        else:
            f.setBold(False)
    if run.italic is not None:
        f.setItalic(run.italic)
    if run.underline is not None:
        f.setUnderline(run.underline)
    if run.strike is not None:
        f.setStrikeOut(run.strike)

    if run.scale != 1.0:
        ps = f.pointSizeF()
        if ps and ps > 0:
            f.setPointSizeF(max(0.1, ps * run.scale))
        else:
            px = f.pixelSize()
            if px and px > 0:
                f.setPixelSize(max(1, int(round(px * run.scale))))
            else:
                f.setPointSizeF(max(0.1, 12.0 * run.scale))

    f.setRawMode(True)
    return f


def measure_rich(font: QFont, rich_text: str):
    base = QFont(font)
    base.setRawMode(True)

    lines = parse_runs(rich_text)

    line_spacing = QFontMetricsF(base).lineSpacing()
    max_w = 0.0

    for runs in lines:
        w = 0.0
        for run in runs:
            rf = font_for_run(base, run)
            w += QFontMetricsF(rf).horizontalAdvance(run.text)
        max_w = max(max_w, w)

    h = line_spacing * max(1, len(lines))
    return max_w, h


def getTextPathRich(font, text, alignment):
    base = QFont(font) if isinstance(font, str) else QFont(font)
    base.setRawMode(True)

    lines = parse_runs(text)
    bm = QFontMetricsF(base)

    base_line_spacing = bm.lineSpacing()
    DESCENT_WEIGHT = 1
    MIN_GAP_FACTOR = 1

    line_widths = []
    line_ad = []  # (max_ascent, max_descent)

    # measure per-line
    for runs in lines:
        w = 0.0
        max_ascent = 0.0
        max_descent = 0.0

        if not runs:
            max_ascent = bm.ascent()
            max_descent = bm.descent()
        else:
            for run in runs:
                rf = font_for_run(base, run)
                m = QFontMetricsF(rf)
                w += m.horizontalAdvance(run.text)
                max_ascent = max(max_ascent, m.ascent())
                max_descent = max(max_descent, m.descent())

        line_widths.append(w)
        line_ad.append((max_ascent, max_descent))

    max_width = max(line_widths) if line_widths else 0.0

    # build path: first line baseline at y=0 (like getTextPath)
    path = QPainterPath()
    baseline_y = 0.0

    for i, runs in enumerate(lines):
        ascent, descent = line_ad[i]

        if alignment & Qt.AlignRight:
            x = max_width - line_widths[i]
        elif alignment & Qt.AlignHCenter:
            x = (max_width - line_widths[i]) / 2.0
        else:
            x = 0.0

        for run in runs:
            rf = font_for_run(base, run)
            m = QFontMetricsF(rf)
            path.addText(x, baseline_y, rf, run.text)
            x += m.horizontalAdvance(run.text)

        # advance baseline between lines only (NO last-line extra advance)
        if i + 1 < len(lines):
            next_ascent = line_ad[i + 1][0]
            baseline_y += max(
                next_ascent,
                descent * DESCENT_WEIGHT,
                base_line_spacing * MIN_GAP_FACTOR,
            )

    # compute "layout height" in a way updatePath can use:
    # top pad: first line ascent above baseline 0
    first_ascent = line_ad[0][0] if line_ad else bm.ascent()
    # bottom pad: last line descent below its baseline
    last_descent = line_ad[-1][1] if line_ad else bm.descent()
    layout_h = first_ascent + baseline_y + last_descent
    layout_w = max_width

    layout = {
        "width": float(layout_w),
        "height": float(layout_h),
        "first_ascent": float(first_ascent),
        "last_descent": float(last_descent),
        "baseline_advance": float(baseline_y),
    }
    return path, layout
