#!/usr/bin/env python3
"""Build the SAP Migration Training Handbook.

Outputs:
  training/handbook/index.html          single-file handbook (screen + print-to-PDF)
  training/handbook/assets/*.svg|.html  standalone diagrams

Run from anywhere:  python3 training/tools/build_handbook.py
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "handbook", "assets"))
OUT = os.path.normpath(os.path.join(HERE, "..", "handbook", "index.html"))

sys.path.insert(0, HERE)
sys.path.insert(0, ASSETS)

import diagrams  # noqa: E402
import content_a as A  # noqa: E402
import content_b as B  # noqa: E402
import content_c as C  # noqa: E402
from style import CSS, JS  # noqa: E402

SECTIONS = [
    ("—", "top", "Cover"),
    ("—", "howto", "How to use this handbook"),
    ("—", "fm", "Document control & approval"),
    ("—", "toc", "Table of contents"),
    ("1", "overview", "Executive training overview"),
    ("2", "objectives", "Objectives & learning outcomes"),
    ("3", "lifecycle", "End-to-end migration lifecycle"),
    ("4", "m1", "Module 1 · Preparation & baseline"),
    ("5", "m2", "Module 2 · Architecture, AWS & build"),
    ("6", "m3", "Module 3 · HANA MDC, backup & recovery"),
    ("7", "m4", "Module 4 · Post-migration validation"),
    ("8", "m5", "Module 5 · Performance & troubleshooting"),
    ("9", "m6", "Module 6 · Oracle migration & switchover"),
    ("10", "m7", "Module 7 · Cutover, Go/No-Go & hypercare"),
    ("11", "tcode", "Transaction & technology reference"),
    ("12", "checklists", "Consolidated validation checklists"),
    ("13", "evidence", "Evidence & documentation strategy"),
    ("14", "ownership", "Ownership & operating model"),
    ("15", "playbook", "Troubleshooting playbook"),
    ("16", "lessons", "Key lessons & practical guidance"),
    ("17", "quiz", "Final knowledge check"),
    ("A", "app-a", "Appendix A · Source coverage"),
    ("B", "app-b", "Appendix B · Completion record"),
    ("C", "app-c", "Appendix C · Glossary"),
    ("D", "app-d", "Appendix D · Review & vetting notes"),
    ("E", "app-e", "Appendix E · Version control"),
]


def scope(svg, prefix):
    """Namespace the internal <defs> ids so eight inline SVGs can share one document."""
    token = "@@P@@"
    out = re.sub(r'\bid="([^"]+)"', lambda m: 'id="%s%s"' % (token, m.group(1)), svg)
    out = re.sub(r'url\(#([^)]+)\)', lambda m: 'url(#%s%s)' % (token, m.group(1)), out)
    return out.replace(token, prefix)


def render_body():
    """Render every section except Appendix D and return the HTML fragments."""
    return [A.s_howto(), A.s_fm(), A.s_toc(), A.s1_overview(), A.s2_objectives(),
            A.s3_lifecycle(), A.s4_m1(), A.s5_m2(), A.s6_m3(), B.s7_m4(), B.s8_m5(),
            B.s9_m6(), B.s10_m7(), C.s11_tcode(), C.s12_checklists(), C.s13_evidence(),
            C.s14_ownership(), C.s15_playbook(), C.s16_lessons(), C.s17_quiz(),
            C.s_app_a(), C.s_app_b(), C.s_app_c(), C.s_app_e()]


def update_stats(figs):
    """Keep the QC figures quoted in Appendix D true for the build being produced."""
    probe = "".join(render_body())
    C.STATS.update({
        "figures": len(figs),
        "tables": probe.count("<table"),
        "checklists": probe.count('class="ck"'),
        "items": probe.count('<input type="checkbox"'),
        "callouts": probe.count('class="box'),
        "quiz": len(C.QUIZ),
        "glossary": len(C.GLOSSARY),
        "words": len(re.sub(r"<[^>]+>", " ", probe).split()),
        "sections": probe.count("<section"),
    })


def write_standalone(outdir, figs):
    """Emit each figure as a standalone .svg plus a minimal .html viewer."""
    os.makedirs(outdir, exist_ok=True)
    for slug, (_label, _fn) in diagrams.ALL.items():
        svg = figs[slug]
        label = diagrams.ALL[slug][0]
        doc = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
               "<title>%s</title><style>body{margin:0;padding:24px;background:#fff}"
               "</style></head><body>%s</body></html>" % (label, svg))
        with open(os.path.join(outdir, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg + "\n")
        with open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8") as fh:
            fh.write(doc)


def build(verbose=True):
    figs = {}
    for slug, (_label, fn) in diagrams.ALL.items():
        figs[slug] = scope(fn(), slug + "-")
    for mod in (A, B, C):
        mod.FIG.clear()
        mod.FIG.update(figs)
    # Render everything except Appendix D first, so the QC numbers it quotes
    # (tables, checklists, figures, glossary terms) are computed from the real build.
    update_stats(figs)
    parts = render_body()
    order = ["howto", "fm", "toc", "overview", "objectives", "lifecycle", "m1", "m2", "m3",
             "m4", "m5", "m6", "m7", "tcode", "checklists", "evidence", "ownership",
             "playbook", "lessons", "quiz", "app-a", "app-b", "app-c", "app-e"]
    body = [A.cover(), '<div class="shell">', A.rail(SECTIONS[1:]),
            '<main class="paper" id="body"><div class="wrap">']
    rendered = dict(zip(order, parts))
    for sid in order:
        body.append(rendered[sid])
        if sid == "app-c":
            body.append(C.s_app_d())
    body.append("</div></main></div>")
    body.append('<button class="backtop no-print" aria-label="Back to top">↑</button>')

    html = "\n".join([
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>SAP Migration Training Handbook · v1.0</title>",
        '<meta name="description" content="Consolidated SAP-to-AWS migration training handbook: '
        'discovery and source baseline, AWS build validation, HANA MDC backup and recovery, Basis '
        'post-migration validation, performance troubleshooting, Oracle Data Guard switchover, cutover, '
        'Go/No-Go and hypercare.">',
        '<meta name="author" content="Amit Prajapati">',
        "<style>%s</style>" % CSS,
        "</head>",
        "<body>",
        "".join(body),
        "<script>%s</script>" % JS,
        "</body>",
        "</html>",
    ])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    write_standalone(ASSETS, figs)

    issues = qc(html, figs)
    if verbose:
        print("built %s (%.1f KB)" % (OUT, len(html.encode()) / 1024))
        for slug in sorted(figs):
            print("  figure %-24s %6.1f KB" % (slug, len(figs[slug].encode()) / 1024))
        print("QC: %s" % ("clean" if not issues else "%d issue(s)" % len(issues)))
        for i in issues:
            print("  ! %s" % i)
    return 1 if issues else 0


def qc(html, figs):
    """Cheap structural checks: unresolved anchors, duplicate ids, unclosed sections."""
    problems = []
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    seen = set()
    for i in re.findall(r'\sid="([^"]+)"', html):
        if i in seen:
            problems.append("duplicate id: %s" % i)
        seen.add(i)
    for href in set(re.findall(r'href="#([^"]+)"', html)):
        if href and href not in ids:
            problems.append("broken anchor: #%s" % href)
    opens, closes = html.count("<section"), html.count("</section>")
    if opens != closes:
        problems.append("section open/close mismatch: %d vs %d" % (opens, closes))
    for tag in ("table", "figure", "details", "svg", "main", "aside"):
        o, c = len(re.findall(r"<%s[\s>]" % tag, html)), html.count("</%s>" % tag)
        if o != c:
            problems.append("<%s> open/close mismatch: %d vs %d" % (tag, o, c))
    for slug, svg in figs.items():
        if not svg.startswith("<svg") or not svg.rstrip().endswith("</svg>"):
            problems.append("figure %s is not a well-formed SVG root" % slug)
    if "undefined" in html or "None</td>" in html or "{FIG" in html:
        problems.append("template placeholder leaked into output")
    return problems


if __name__ == "__main__":
    sys.exit(build())
