#!/usr/bin/env python3
"""Render the eight handbook figures to high-resolution PNGs.

The figures are defined once, in terms of the drawing primitives in `svgkit`.
Here those primitives are swapped for the Matplotlib backend in `mplkit`, so the
exact same layout code produces PNGs that the Word build can embed.

Usage:  <venv>/bin/python training/tools/render_png.py [outdir]
        (needs matplotlib; run build_handbook.py first so the SVGs exist)
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(
    os.path.join(HERE, "..", "handbook", "assets"))

sys.path.insert(0, HERE)

import svgkit  # noqa: E402,F401  (loaded for real first: mplkit imports its metrics)
import mplkit  # noqa: E402

# Replay diagrams.py against the Matplotlib backend instead of the SVG one.
sys.modules["svgkit"] = mplkit
import diagrams  # noqa: E402  (its `from svgkit import ...` now resolves to mplkit)


def render(outdir=OUT, quiet=False):
    os.makedirs(outdir, exist_ok=True)
    written = []
    for slug, (_label, fn) in diagrams.ALL.items():
        fn()
        target = os.path.join(outdir, slug + ".png")
        mplkit.save_png(target)
        mplkit.close()
        written.append(target)
        if not quiet:
            print("  %-24s %7.1f KB" % (slug + ".png", os.path.getsize(target) / 1024))
    return written


if __name__ == "__main__":
    print("rendered %d figures to %s" % (len(render()), OUT))
