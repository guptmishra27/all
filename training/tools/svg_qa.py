"""Geometric QA for the handbook SVG diagrams.

No browser is available in this sandbox, so diagrams are verified analytically:
every <text> node is measured with a per-character advance table, then checked
against (a) the viewBox and (b) the innermost container it is anchored in.
Overflow is reported so the drawing code can be corrected before publishing.
"""

from __future__ import annotations

import glob
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"

# rough Helvetica/Inter advance widths as a fraction of font-size
ADV = {
    "upper": 0.68, "lower": 0.53, "digit": 0.56, "space": 0.28, "punct": 0.34,
    "wide": 0.86, "narrow": 0.34,
}
WIDE = set("MWQ@%")
NARROW = set("iljtfrI.,:;!'|[](){}-/ ")


def char_w(ch, size):
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


def text_width(s, size, tracking=0.0):
    return sum(char_w(c, size) for c in s) + max(0, len(s) - 1) * (tracking or 0) * size


def span(x, w, anchor):
    if anchor == "start":
        return x, x + w
    if anchor == "end":
        return x - w, x
    return x - w / 2, x + w / 2


def rects(tree):
    out = []
    for r in tree.iter(NS + "rect"):
        try:
            x, y = float(r.get("x", 0)), float(r.get("y", 0))
            w, h = float(r.get("width", 0)), float(r.get("height", 0))
        except ValueError:
            continue
        out.append((x, y, w, h, r.get("fill", ""), r.get("stroke", "")))
    return out


def panels(tree):
    """Containers worth checking: rects big enough to hold a label."""
    return [r for r in rects(tree) if r[2] > 90 and r[3] > 34 and r[4] not in ("none", "url(#grid)")]


def check(path, pad=3.0, verbose=False):
    tree = ET.parse(path)
    root = tree.getroot()
    vb = [float(v) for v in root.get("viewBox").split()]
    VW, VH = vb[2], vb[3]
    boxes = panels(tree)
    problems = []
    for x, y, w, h, _f, _s in rects(tree):
        if x < -1 or y < -1 or x + w > VW + 1 or y + h > VH + 1:
            problems.append(("RECT-CLIP", "rect x=%.0f y=%.0f w=%.0f h=%.0f" % (x, y, w, h),
                             "right=%.0f bottom=%.0f" % (x + w, y + h),
                             "viewBox %.0fx%.0f" % (VW, VH), "", ""))
    for t in root.iter(NS + "text"):
        s = "".join(t.itertext()).strip()
        if not s:
            continue
        x, y = float(t.get("x", 0)), float(t.get("y", 0))
        size = float(t.get("font-size", 14))
        anchor = t.get("text-anchor", "start")
        tracking = float(t.get("letter-spacing", 0) or 0)
        w = text_width(s, size, tracking)
        x0, x1 = span(x, w, anchor)
        y0, y1 = y - size * 0.82, y + size * 0.24
        if x0 < -1 or x1 > VW + 1 or y0 < -1 or y1 > VH + 1:
            problems.append(("VIEWBOX", s[:70], round(x0, 1), round(x1, 1), round(y, 1),
                             "viewBox width=%s" % VW))
            continue
        # innermost container whose centre contains the anchor point
        cands = [b for b in boxes if b[0] <= x <= b[0] + b[2] and b[1] <= y <= b[1] + b[3]]
        if not cands:
            continue
        cands.sort(key=lambda b: b[2] * b[3])
        bx, by, bw, bh = cands[0][:4]
        # only enforce when the label looks like it belongs to that container
        if bw > 240 and bh > 200:
            continue
        if x0 < bx + pad or x1 > bx + bw - pad:
            problems.append(("H-OVERFLOW", s[:70], round(x0, 1), round(x1, 1),
                             "box x=%.0f w=%.0f (%.0f..%.0f)" % (bx, bw, bx + pad, bx + bw - pad), ""))
    return problems


def main(pattern, verbose=False):
    total = 0
    for path in sorted(glob.glob(pattern)):
        probs = check(path, verbose=verbose)
        name = path.split("/")[-1]
        if probs:
            print("\n== %s : %d issue(s)" % (name, len(probs)))
            for p in probs:
                print("   %-11s %-72s x0=%-8s x1=%-8s %s %s" % p)
            total += len(probs)
        else:
            print("== %s : clean" % name)
    print("\nTOTAL ISSUES: %d" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/svgout/*.svg"))
