"""Matplotlib backend for the handbook diagram primitives.

`svgkit` emits SVG strings; this module exposes the *same* function names and
signatures but draws into a Matplotlib axes instead, so `diagrams.py` can be
replayed unchanged to produce high-resolution PNGs. Those PNGs are what the Word
version of the handbook embeds (Word cannot render inline SVG).

Layout metrics (text_width / wrap_px) are imported from svgkit so the pixel
geometry — and therefore the overflow checks in svg_qa.py — stay identical
between the SVG and PNG renderings.
"""

from __future__ import annotations

import math
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402

import svgkit as _svgkit  # noqa: F401
from svgkit import char_w, esc, wrap  # noqa: F401


def _calibration(fp):
    """Ratio between this renderer's true glyph advance and svgkit's estimate.

    Layout decisions (wrapping) are made in SVG pixels; the PNG renderer uses a
    real font, so wrapping must use real widths or text escapes its container.
    """
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    probe = ("The migration team consumes the approved sizing report for target planning "
             "and validation; interfaces, NFS shares and AL11 directories are recorded.")
    w1 = TextPath((0, 0), probe, size=1.0, prop=fp).get_extents().width
    return w1 / _svgkit.text_width(probe, 1.0)


_K = {}


def _w_bucket(weight):
    try:
        w = int(weight)
    except (TypeError, ValueError):
        return 600 if str(weight) in ("semibold", "demibold", "demi") else (
            700 if str(weight) == "bold" else 500)
    return 500 if w <= 500 else (600 if w <= 650 else (700 if w <= 750 else 800))


def _k(weight=500):
    b = _w_bucket(weight)
    if b not in _K:
        _K[b] = _calibration(FontProperties(family=SANS, weight=WEIGHTS.get(b, "normal")))
    return _K[b]


def text_width(s, size, tracking=0.0, weight=500):
    """Measured advance width of `s` in SVG pixels for this backend's font."""
    key = (s, round(float(size), 2), _w_bucket(weight))
    if key not in _TEXT_W_CACHE:
        _TEXT_W_CACHE[key] = _svgkit.text_width(s, size, tracking) * _k(weight)
    return _TEXT_W_CACHE[key]


def wrap_px(s, size, avail, tracking=0.0, weight=500):
    words, lines, cur = s.split(" "), [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if text_width(trial, size, tracking, weight) <= avail or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

DPI = 200
PX_PER_IN = 100.0  # CSS px -> inches at 100 dpi, so the SVG viewBox maps 1:1

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

WEIGHTS = {400: "normal", 500: "normal", 600: "semibold", 700: "bold", 800: "black"}
PX2PT = 0.72          # 1 SVG px == 0.72 pt at the 100 dpi figure scale
_TEXT_W_CACHE = {}
# DejaVu Sans ships with Matplotlib, so the PNG build needs no system fonts.
# Extend this list if the build host has the brand face available.
SANS = ["DejaVu Sans"]

_AX = None
_H = 800
_COUNT = 0


# --------------------------------------------------------------------------- #
# surface management
# --------------------------------------------------------------------------- #
def _ax():
    global _AX
    if _AX is None:
        raise RuntimeError("no drawing surface open — call svg_open() first")
    return _AX


def svg_open(height, width=W):
    """Begin a new figure; returns '' so diagrams.py can append it harmlessly."""
    global _AX, _H, _COUNT
    _H = height
    fig = plt.figure(figsize=(width / PX_PER_IN, height / PX_PER_IN), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)          # SVG y grows downwards
    ax.axis("off")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    _AX = ax
    _COUNT += 1
    # faint graph-paper background, matching the SVG <pattern id="grid">
    for gx in range(0, width + 1, 26):
        ax.add_line(plt.Line2D([gx, gx], [0, height], color="#eef2f7", lw=0.5, zorder=0))
    for gy in range(0, int(height) + 1, 26):
        ax.add_line(plt.Line2D([0, width], [gy, gy], color="#eef2f7", lw=0.5, zorder=0))
    return ""


def save_png(path):
    ax = _ax()
    fig = ax.figure
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def close():
    global _AX
    if _AX is not None:
        plt.close(_AX.figure)
    _AX = None


def defs():
    return ""


def _z():
    global _COUNT
    _COUNT += 1
    return _COUNT


VALID_WEIGHTS = {"ultralight", "light", "normal", "regular", "book", "medium", "roman",
                 "semibold", "demibold", "demi", "bold", "heavy", "extra bold", "black"}


def _weight(w):
    """Map the SVG numeric font-weight onto Matplotlib's accepted values."""
    try:
        return WEIGHTS.get(int(w), "normal")
    except (TypeError, ValueError):
        s = str(w).strip().lower()
        return s if s in VALID_WEIGHTS else "normal"


def _norm(color, default="none"):
    if color is None or color == "none":
        return "none"
    if color == "url(#grid)":
        return "none"        # graph paper is drawn by svg_open(), not by a rect
    if isinstance(color, str) and color.startswith("url("):
        return NAVY          # gradients are flattened to the brand navy
    return color


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #
def rect(x, y, w, h, fill="#ffffff", stroke="#c7d2e0", rx=10, sw=1.5, dash=None, shadow=False,
         opacity=1.0):
    ax = _ax()
    x, y, w, h = float(x), float(y), float(w), float(h)
    fill = _norm(fill)
    stroke = _norm(stroke)
    if w <= 0 or h <= 0:
        return ""
    if shadow:
        ax.add_patch(FancyBboxPatch((x + 1.0, y + 2.6), w, h,
                                    boxstyle="round,pad=0,rounding_size=%f" % max(0.0, float(rx)),
                                    linewidth=0, facecolor="#0b2545", alpha=0.13, zorder=_z(),
                                    mutation_aspect=1))
    ls = (0, (float(dash.split()[0]), float(dash.split()[-1]))) if dash else "solid"
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%f" % max(0.0, float(rx)),
                                linewidth=float(sw) if stroke != "none" else 0,
                                edgecolor=stroke, facecolor=fill if fill != "none" else "none",
                                alpha=float(opacity), linestyle=ls, zorder=_z(),
                                mutation_aspect=1))
    return ""


def text(x, y, s, size=14, fill="#12263f", weight=500, anchor="middle", spacing=None,
         opacity=1.0, style=None):
    ax = _ax()
    s = str(s)
    if not s.strip():
        return ""
    ha = {"start": "left", "middle": "center", "end": "right"}.get(anchor, "left")
    t = ax.text(float(x), float(y), s, fontsize=float(size) * PX2PT, color=_norm(fill, "#12263f"),
                fontweight=_weight(weight), ha=ha, va="baseline", alpha=float(opacity),
                fontstyle="italic" if style == "italic" else "normal",
                fontfamily=SANS, zorder=_z())
    if spacing:
        try:
            # letter-spacing is not supported directly; approximate wide tracking
            # with a thin space so kickers still read as spaced small-caps.
            spaced = "\u2009".join(list(s)) if float(spacing) >= 0.8 else s
            if spaced != s:
                t.set_text(spaced)
        except (TypeError, ValueError):
            pass
    return ""


def mtext(cx, cy, lines, size=13, fill=None, weight=500, lh=None, anchor="middle"):
    fill = fill or BODY
    lh = lh or size + 6
    y0 = cy - ((len(lines) - 1) * lh) / 2 + size * 0.36
    for i, l in enumerate(lines):
        text(cx, y0 + i * lh, l, size, fill, weight, anchor)
    return ""


def _arrowhead(ax, x1, y1, x2, y2, color, sw):
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    if dist < 0.5:
        return
    ux, uy = dx / dist, dy / dist
    length = max(6.0, sw * 3.6)
    halfw = length * 0.42
    bx, by = x2 - ux * length, y2 - uy * length
    px, py = -uy, ux
    ax.add_patch(Polygon([(x2, y2), (bx + px * halfw, by + py * halfw),
                          (bx - px * halfw, by - py * halfw)],
                         closed=True, facecolor=color, edgecolor="none", zorder=_z()))


def _marker_color(marker):
    return {"arrowg": GREEN_B, "arrowr": RED_B, "arrowa": AMBER_B}.get(marker, "#7f96b2")


def arrow(x1, y1, x2, y2, color="#7f96b2", sw=2, dash=None, marker="arrow"):
    ax = _ax()
    col = _norm(color, "#7f96b2")
    ls = (0, (float(dash.split()[0]), float(dash.split()[-1]))) if dash else "solid"
    ax.add_line(plt.Line2D([float(x1), float(x2)], [float(y1), float(y2)], color=col,
                           lw=float(sw), linestyle=ls, solid_capstyle="round", zorder=_z()))
    _arrowhead(ax, float(x1), float(y1), float(x2), float(y2), col, float(sw))
    return ""


def line(x1, y1, x2, y2, color="#e2e8f0", sw=1, dash=None):
    ax = _ax()
    ls = (0, (float(dash.split()[0]), float(dash.split()[-1]))) if dash else "solid"
    ax.add_line(plt.Line2D([float(x1), float(x2)], [float(y1), float(y2)],
                           color=_norm(color, "#e2e8f0"), lw=float(sw), linestyle=ls, zorder=_z()))
    return ""


_PATH_RE = re.compile(r"([MLHVZCSQ])\s*([^MLHVZCSQ]*)", re.I)


def _parse_path(d):
    pts, cur, start = [], (0.0, 0.0), (0.0, 0.0)
    for cmd, args in _PATH_RE.findall(d or ""):
        nums = [float(v) for v in re.findall(r"-?\d*\.?\d+(?:e[-+]?\d+)?", args)]
        c = cmd.upper()
        if c == "M":
            cur = (nums[0], nums[1])
            start = cur
            pts.append(cur)
            for i in range(2, len(nums) - 1, 2):
                cur = (nums[i], nums[i + 1])
                pts.append(cur)
        elif c == "L":
            for i in range(0, len(nums) - 1, 2):
                cur = (nums[i], nums[i + 1])
                pts.append(cur)
        elif c == "H":
            for v in nums:
                cur = (v, cur[1])
                pts.append(cur)
        elif c == "V":
            for v in nums:
                cur = (cur[0], v)
                pts.append(cur)
        elif c in ("C", "S", "Q"):
            # control points are approximated by their on-curve endpoint
            step = 6 if c in ("C", "S") else 4
            for i in range(0, len(nums) - step + 1, step):
                cur = (nums[i + step - 2], nums[i + step - 1])
                pts.append(cur)
        elif c == "Z":
            pts.append(start)
            cur = start
    return pts


def path(d, color="#7f96b2", sw=2, dash=None, fill="none", marker="arrow"):
    ax = _ax()
    pts = _parse_path(d)
    if len(pts) < 2:
        return ""
    col = _norm(color, "#7f96b2")
    ls = (0, (float(dash.split()[0]), float(dash.split()[-1]))) if dash else "solid"
    ax.add_line(plt.Line2D([p[0] for p in pts], [p[1] for p in pts], color=col, lw=float(sw),
                           linestyle=ls, solid_capstyle="round", solid_joinstyle="round", zorder=_z()))
    if fill and fill != "none":
        ax.add_patch(Polygon(pts, closed=True, facecolor=_norm(fill), edgecolor="none", zorder=_z()))
    if marker:
        _arrowhead(ax, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1],
                   _norm(_marker_color(marker), "#7f96b2"), float(sw))
    return ""


def poly(points, color="#7f96b2", sw=2, dash=None, marker="arrow"):
    pts = [(float(a), float(b)) for a, b in
           (p.strip().split(",") for p in str(points).split() if "," in p)]
    if len(pts) < 2:
        return ""
    ax = _ax()
    ls = (0, (float(dash.split()[0]), float(dash.split()[-1]))) if dash else "solid"
    ax.add_line(plt.Line2D([p[0] for p in pts], [p[1] for p in pts], color=_norm(color, "#7f96b2"),
                           lw=float(sw), linestyle=ls, zorder=_z()))
    if marker:
        _arrowhead(ax, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], _norm(color, "#7f96b2"), float(sw))
    return ""


def diamond(cx, cy, w, h, fill=AMBER, stroke=AMBER_B, sw=2):
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    _ax().add_patch(Polygon(pts, closed=True, facecolor=_norm(fill), edgecolor=_norm(stroke),
                            lw=float(sw), zorder=_z()))
    return ""


def _circle(cx, cy, r, fill):
    _ax().add_patch(Circle((float(cx), float(cy)), float(r), facecolor=_norm(fill),
                           edgecolor="none", zorder=_z()))


def chip(cx, cy, label, fill="#0f2b4c", color="#ffffff", w=None, h=26, size=12, rx=13):
    w = w or max(58, len(label) * size * 0.60 + 26)
    rect(cx - w / 2, cy - h / 2, w, h, fill=fill, stroke=fill, rx=rx)
    text(cx, cy + size * 0.36, label, size=size, fill=color, weight=700, spacing="0.3")
    return ""


def badge(cx, cy, n, r=17, fill="#1b4f86", color="#ffffff", size=15):
    _circle(cx, cy, r, fill)
    text(cx, cy + size * 0.36, str(n), size=size, fill=color, weight=700)
    return ""


def title(x, y, s, size=21, fill=NAVY):
    text(x, y, s, size=size, fill=fill, weight=800, anchor="start", spacing="-0.2")
    rect(x, y + 10, 74, 4, fill=BLUE, stroke="none", rx=2)
    return ""


def sub(x, y, s, size=13.5, fill=MUTED, width_chars=168):
    lines = wrap_px(s, size, width_chars * size * 0.52)
    for i, l in enumerate(lines):
        text(x, y + i * 20, l, size=size, fill=fill, weight=500, anchor="start")
    return ""


def sub_h(s, size=13.5, width_chars=168):
    return (len(wrap_px(s, size, width_chars * size * 0.52)) - 1) * 20


def panel(x, y, w, h, heading, fill="#ffffff", stroke="#c7d2e0", hfill="url(#hdr)",
          hsize=14, rx=12, hh=40):
    rect(x, y, w, h, fill=fill, stroke=stroke, rx=rx, shadow=True)
    rect(x, y, w, hh, fill=hfill, stroke="none", rx=rx)
    rect(x, y + hh - rx, w, rx, fill=hfill, stroke="none", rx=0)
    text(x + w / 2, y + hh / 2 + hsize * 0.36, heading, size=hsize, fill="#ffffff",
         weight=700, spacing="0.2")
    return ""


def legend(items, x, y, sw=26, gap=14, size=12.5):
    cx = x
    for kind, color, label in items:
        if kind in ("line", "dash"):
            line(cx, y - 4, cx + sw, y - 4, color=color, sw=3, dash="6 5" if kind == "dash" else None)
        else:
            rect(cx, y - 14, sw, 20, fill=color, stroke=color if color != "#ffffff" else GREY_B, rx=5)
        text(cx + sw + 8, y, label, size=size, fill=BODY, weight=600, anchor="start")
        cx += sw + 8 + len(label) * size * 0.56 + gap
    return ""


def footnote(x, y, s, size=12, fill="#7b8794"):
    return text(x, y, s, size=size, fill=fill, weight=500, anchor="start", style="italic")


def callout(x, y, w, h, kicker, lines, fill=AMBER, stroke=AMBER_B, kfill="#8a6410",
            bfill="#5c4a12", size=12.5, lh=21, bullet=False):
    rect(x, y, w, h, fill=fill, stroke=stroke, rx=12, shadow=True)
    usable = w - 56
    text(x + 24, y + 30, kicker, size=11.5, fill=kfill, weight=800, anchor="start", spacing="1.1")
    yy = y + 58
    for rawline in lines:
        prefix = "•  " if bullet else ""
        avail = usable - (text_width(prefix, size, weight=600) if bullet else 0)
        for seg in wrap_px(rawline, size, avail, weight=600):
            text(x + 24, yy, prefix + seg, size=size, fill=bfill, weight=600, anchor="start")
            prefix = "    " if bullet else ""
            yy += lh
    return ""


def stage_card(x, y, w, h, n, name, items, accent=BLUE, fill="#ffffff"):
    rect(x, y, w, h, fill=fill, stroke=GREY_B, rx=10, shadow=True)
    rect(x, y, 6, h, fill=accent, stroke="none", rx=0)
    _circle(x + 30, y + 28, 15, accent)
    text(x + 30, y + 33, str(n), size=14, fill="#ffffff", weight=700)
    text(x + 54, y + 33, name, size=15, fill=NAVY, weight=800, anchor="start")
    yy = y + 62
    for it in items:
        _circle(x + 26, yy - 4, 2.6, accent)
        text(x + 36, yy, it, size=12.5, fill=BODY, weight=500, anchor="start")
        yy += 21
    return ""


def tspan_line(cx, cy, parts, size=13, anchor="middle", lh=20):
    widths = [len(p[0]) * size * 0.53 for p in parts]
    x = cx - sum(widths) / 2
    for (t, f, wt), w in zip(parts, widths):
        text(x, cy, t, size=size, fill=f, weight=wt, anchor="start")
        x += w
    return ""
