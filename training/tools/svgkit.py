"""SVG drawing primitives for the SAP Migration Training Handbook.

Pure string generation: no third-party dependencies, no JavaScript, no external
fonts or images. Output renders identically on screen, in browser print-to-PDF
and when lifted into decks or runbooks.
"""

from __future__ import annotations

import html as _html

W = 1440

NAVY = "#0f2b4c"
BLUE = "#1b4f86"
SKY = "#e8f0fb"
SKY_B = "#9ec3ec"
GREEN = "#e6f4ea"
GREEN_B = "#3d9a5f"
AMBER = "#fdf3d8"
AMBER_B = "#d9a520"
RED = "#fdecec"
RED_B = "#c8434b"
GREY = "#f3f5f9"
GREY_B = "#c7d2e0"
PLUM = "#f1e9f7"
PLUM_B = "#8e5aa8"
MUTED = "#5b7288"
BODY = "#3d5468"


ADV = {"upper": 0.68, "lower": 0.53, "digit": 0.56, "space": 0.28, "punct": 0.34,
       "wide": 0.86, "narrow": 0.34}
WIDE = set("MWQ@%")
NARROW = set("iljtfrI.,:;!'|[](){}-/ ")


def char_w(ch, size):
    """Estimated glyph advance, used so text can be wrapped to fit containers."""
    if ch in WIDE:
        return ADV["wide"] * size
    if ch in NARROW:
        return ADV["narrow"] * size
    if ch.isspace():
        return ADV["space"] * size
    if ch.isdigit():
        return ADV["digit"] * size
    if ch.isupper():
        return ADV["upper"] * size
    if ch.isalpha():
        return ADV["lower"] * size
    return ADV["punct"] * size


def text_width(s, size, tracking=0.0, weight=500):
    return sum(char_w(c, size) for c in s) + max(0, len(s) - 1) * (tracking or 0) * size


def esc(s):
    return _html.escape(str(s), quote=True)


def svg_open(height, width=W):
    head = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" role="img" '
    head += 'preserveAspectRatio="xMidYMid meet" style="max-width:%dpx;height:auto;background:#fff;'
    head += 'font-family:Inter,-apple-system,Segoe UI,Roboto,Helvetica Neue,Arial,sans-serif;">\n'
    return head % (width, height, width)


def defs():
    out = ['<defs>']
    out.append('<pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">')
    out.append('<path d="M26 0H0V26" fill="none" stroke="#e6ebf2" stroke-width="1"/></pattern>')
    out.append('<filter id="sh" x="-14%" y="-14%" width="132%" height="155%">')
    out.append('<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0b2545" flood-opacity="0.14"/></filter>')
    out.append('<linearGradient id="hdr" x1="0" y1="0" x2="1" y2="0">')
    out.append('<stop offset="0" stop-color="#0f2b4c"/><stop offset="1" stop-color="#1b4f86"/></linearGradient>')
    out.append('<marker id="arrow" markerWidth="9" markerHeight="9" refX="7.4" refY="3.2" orient="auto" '
               'markerUnits="strokeWidth"><path d="M0 0 L8 3.2 L0 6.4 Z" fill="context-stroke"/></marker>')
    out.append('</defs>')
    return "".join(out)


def rect(x, y, w, h, fill="#ffffff", stroke="#c7d2e0", rx=10, sw=1.5, dash=None, shadow=False):
    a = ' stroke-dasharray="%s"' % dash if dash else ""
    f = ' filter="url(#sh)"' if shadow else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"%s%s/>' % (x, y, w, h, rx, fill, stroke, sw, a, f))


def text(x, y, s, size=14, fill="#12263f", weight=500, anchor="middle", spacing=None, style=None):
    ls = ' letter-spacing="%s"' % spacing if spacing else ""
    st = ' font-style="%s"' % style if style else ""
    return ('<text x="%s" y="%s" font-size="%s" fill="%s" font-weight="%s" text-anchor="%s"%s%s>%s</text>'
            % (x, y, size, fill, weight, anchor, ls, st, esc(s)))


def mtext(cx, cy, lines, size=13, fill=None, weight=500, lh=None, anchor="middle"):
    fill = fill or BODY
    lh = lh or size + 6
    y0 = cy - ((len(lines) - 1) * lh) / 2 + size * 0.36
    return "".join(text(cx, y0 + i * lh, l, size, fill, weight, anchor) for i, l in enumerate(lines))


def arrow(x1, y1, x2, y2, color="#7f96b2", sw=2, dash=None, marker="arrow"):
    a = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s marker-end="url(#%s)"/>'
            % (x1, y1, x2, y2, color, sw, a, marker))


def path(d, color="#7f96b2", sw=2, dash=None, fill="none", marker="arrow"):
    a = ' stroke-dasharray="%s"' % dash if dash else ""
    m = ' marker-end="url(#%s)"' % marker if marker else ""
    return '<path d="%s" stroke="%s" stroke-width="%s" fill="%s"%s%s/>' % (d, color, sw, fill, a, m)


def line(x1, y1, x2, y2, color="#e2e8f0", sw=1, dash=None):
    a = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, color, sw, a)


def chip(cx, cy, label, fill="#0f2b4c", color="#ffffff", w=None, h=26, size=12, rx=13):
    w = w or max(58, len(label) * size * 0.60 + 26)
    return (rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=fill, rx=rx)
            + text(cx, cy + size * 0.36, label, size=size, fill=color, weight=700, spacing="0.3"))


def badge(cx, cy, n, r=17, fill="#1b4f86", color="#ffffff", size=15):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (cx, cy, r, fill)
            + text(cx, cy + size * 0.36, str(n), size=size, fill=color, weight=700))


def diamond(cx, cy, w, h, fill=AMBER, stroke=AMBER_B, sw=2):
    pts = "%s,%s %s,%s %s,%s %s,%s" % (cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2, cx - w / 2, cy)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (pts, fill, stroke, sw)


def title(x, y, s, size=21, fill=NAVY):
    return (text(x, y, s, size=size, fill=fill, weight=800, anchor="start", spacing="-0.2")
            + rect(x, y + 10, 74, 4, fill=BLUE, stroke="none", rx=2))


def sub(x, y, s, size=13.5, fill=MUTED, width_chars=168):
    """Render a subtitle, wrapping long text into lines of roughly width_chars."""
    return "".join(text(x, y + i * 20, l, size=size, fill=fill, weight=500, anchor="start")
                   for i, l in enumerate(wrap_px(s, size, width_chars * size * 0.52)))


def sub_h(s, size=13.5, width_chars=168):
    return (len(wrap_px(s, size, width_chars * size * 0.52)) - 1) * 20


def panel(x, y, w, h, heading, fill="#ffffff", stroke="#c7d2e0", hfill="url(#hdr)", hsize=14, rx=12, hh=40):
    out = [rect(x, y, w, h, fill=fill, stroke=stroke, rx=rx, shadow=True)]
    out.append('<path d="M%s %s V%s A%s %s 0 0 1 %s %s H%s A%s %s 0 0 1 %s %s V%s Z" fill="%s"/>'
               % (x, y + hh, y + rx, rx, rx, x + rx, y, x + w - rx, rx, rx, x + w, y + rx, y + hh, hfill))
    out.append(text(x + w / 2, y + hh / 2 + hsize * 0.36, heading, size=hsize, fill="#ffffff",
                    weight=700, spacing="0.2"))
    return "".join(out)


def legend(items, x, y, sw=26, gap=14, size=12.5):
    out, cx = [], x
    for kind, color, label in items:
        if kind == "line":
            out.append(line(cx, y - 4, cx + sw, y - 4, color=color, sw=3))
        elif kind == "dash":
            out.append(line(cx, y - 4, cx + sw, y - 4, color=color, sw=3, dash="6 5"))
        else:
            out.append(rect(cx, y - 14, sw, 20, fill=color, stroke=color, rx=5))
        out.append(text(cx + sw + 8, y, label, size=size, fill=BODY, weight=600, anchor="start"))
        cx += sw + 8 + len(label) * size * 0.56 + gap
    return "".join(out)


def footnote(x, y, s, size=12, fill="#7b8794"):
    return text(x, y, s, size=size, fill=fill, weight=500, anchor="start", style="italic")


def callout(x, y, w, h, kicker, lines, fill=AMBER, stroke=AMBER_B, kfill="#8a6410",
            bfill="#5c4a12", size=12.5, lh=21, bullet=False):
    """Callout box with automatic wrapping so text never escapes its container."""
    out = [rect(x, y, w, h, fill=fill, stroke=stroke, rx=12, shadow=True)]
    usable = w - 56
    out.append(text(x + 24, y + 30, kicker, size=11.5, fill=kfill, weight=800,
                    anchor="start", spacing="1.1"))
    yy = y + 58
    for raw in lines:
        prefix = "•  " if bullet else ""
        avail = usable - (text_width(prefix, size) if bullet else 0)
        for seg in wrap_px(raw, size, avail):
            out.append(text(x + 24, yy, prefix + seg, size=size, fill=bfill,
                            weight=600, anchor="start"))
            prefix = "    " if bullet else ""
            yy += lh
    return "".join(out)


def wrap_px(s, size, avail, tracking=0.0, weight=500):
    """Greedy word wrap measured in estimated rendered pixels."""
    words, lines, cur = s.split(" "), [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if text_width(trial, size, tracking) <= avail or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def stage_card(x, y, w, h, n, name, items, accent=BLUE, fill="#ffffff"):
    out = [rect(x, y, w, h, fill=fill, stroke=GREY_B, rx=10, shadow=True)]
    out.append(rect(x, y, 6, h, fill=accent, stroke="none", rx=0))
    out.append('<circle cx="%s" cy="%s" r="15" fill="%s"/>' % (x + 30, y + 28, accent))
    out.append(text(x + 30, y + 33, str(n), size=14, fill="#ffffff", weight=700))
    out.append(text(x + 54, y + 33, name, size=15, fill=NAVY, weight=800, anchor="start"))
    yy = y + 62
    for it in items:
        out.append('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (x + 26, yy - 4, accent))
        out.append(text(x + 36, yy, it, size=12.5, fill=BODY, weight=500, anchor="start"))
        yy += 21
    return "".join(out)


def wrap(s, n):
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
