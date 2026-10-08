"""HTML building blocks used by the handbook generator."""

from __future__ import annotations

import html as _h
import re


def e(s):
    return _h.escape(str(s), quote=True)


TAGLIKE = re.compile(r"<\s*(?:/)?\s*(?:b|i|em|strong|code|span|a|br|sub|sup|u|small|kbd|div|p|ul|ol|li|table|tr|td|th|figure|details|summary|h[1-6])\b", re.I)


def raw(v):
    """True when a cell/item string should be passed through as HTML rather than escaped."""
    return isinstance(v, str) and bool(TAGLIKE.search(v))


def cellval(v):
    return v if raw(v) else e(v)


def table(headers, rows, caption=None, cls="", widths=None, align=None, note=None):
    """headers: list[str]; rows: list[list[str]] (raw HTML allowed in cells)."""
    out = ['<div class="tw">']
    out.append('<table class="%s">' % cls)
    if caption:
        out.append("<caption>%s</caption>" % e(caption))
    if widths:
        out.append("<colgroup>" + "".join('<col style="width:%s">' % w for w in widths) + "</colgroup>")
    out.append("<thead><tr>")
    for i, h in enumerate(headers):
        c = ""
        if align and align[i] == "c":
            c = ' class="c"'
        out.append("<th%s>%s</th>" % (c, cellval(h)))
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>")
        for i, cell in enumerate(r):
            c = ""
            if align and i < len(align) and align[i] == "c":
                c = ' class="c"'
            val = cellval(cell)
            out.append("<td%s>%s</td>" % (c, val))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    if note:
        out.append('<p class="tnote">%s</p>' % e(note))
    return "".join(out)


def checklist(cid, headers, items, widths=None, statuses=None, hide_status=False):
    """items: list of str (check label) or list[str] (multi-column: label + extra cols)."""
    statuses = statuses or ["Not Started", "In Progress", "Complete", "N/A", "Blocked"]
    out = ['<div class="ckbar"><div class="meter"><i></i></div><span class="pct"></span></div>']
    out.append('<div class="tw"><table class="ck" data-list="%s">' % e(cid))
    out.append("<thead><tr>")
    for i, h in enumerate(headers):
        cls = ' class="c"' if i == 0 or h in ("Done", "Status") else ""
        out.append("<th%s>%s</th>" % (cls, h if h.startswith("<") else e(h)))
    out.append("</tr></thead><tbody>")
    for idx, it in enumerate(items):
        cols = it if isinstance(it, (list, tuple)) else [it]
        plain0 = re.sub(r"<[^>]+>", "", cols[0])
        out.append('<tr><td class="c"><input type="checkbox" data-id="%s-%d" '
                   'aria-label="Mark %s complete"></td>' % (e(cid), idx, e(plain0)[:60]))
        out.append('<td class="item">%s</td>' % cellval(cols[0]))
        for extra in cols[1:]:
            out.append("<td>%s</td>" % cellval(extra))
        if not hide_status:
            opts = "".join('<option>%s</option>' % e(s) for s in statuses)
            out.append('<td><select data-id="%s-s%d">%s</select></td>' % (e(cid), idx, opts))
        out.append('<td><input type="text" data-id="%s-e%d" placeholder="Evidence reference, ticket or remark"></td>'
                   % (e(cid), idx))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def box(kind, label, body):
    return '<div class="box %s"><div class="lbl">%s</div>%s</div>' % (e(kind), e(label), body)


def para(*lines):
    return "".join("<p>%s</p>" % cellval(l) for l in lines)


def bullets(items, cls=""):
    return '<ul class="%s">' % cls + "".join("<li>%s</li>" % cellval(i) for i in items) + "</ul>"


def steps(items):
    return '<ol class="num">' + "".join("<li>%s</li>" % cellval(i) for i in items) + "</ol>"


def cards(items, cols=2, accent=False):
    """items: list of (title, body_html_or_str)."""
    cls = "grid g%d" % cols
    out = ['<div class="%s">' % cls]
    for t, b in items:
        body = b if raw(b) else "<p>%s</p>" % e(b)
        out.append('<div class="card%s"><h4>%s</h4>%s</div>'
                   % (" accent" if accent else "", e(t), body))
    out.append("</div>")
    return "".join(out)


def kpis(items):
    out = ['<div class="grid g4">']
    for k, v, d in items:
        out.append('<div class="kpi"><div class="k">%s</div><div class="v">%s</div><div class="d">%s</div></div>'
                   % (cellval(k), cellval(v), cellval(d)))
    out.append("</div>")
    return "".join(out)


def flow(parts):
    out = ['<div class="flowline">']
    for i, p in enumerate(parts):
        if i:
            out.append("<i>→</i>")
        out.append("<b>%s</b>" % e(p))
    out.append("</div>")
    return "".join(out)


def figure(slug, svg, caption):
    return ('<figure id="fig-%s"><div class="figframe">%s</div><figcaption>%s</figcaption></figure>'
            % (e(slug), svg, caption))


def pill(txt, kind=""):
    """Raw inline badge. Returns HTML, so callers must embed it in a cell/item that
    is passed through unescaped (htmlkit treats strings starting with '<' as HTML)."""
    return '<span class="pill %s">%s</span>' % (e(kind), e(txt))


def cmd(lines):
    body = "<br>".join(cellval(l) for l in lines)
    return '<div class="cmd">%s</div>' % body


def qa(items, scope_id):
    out = []
    for i, (q, a) in enumerate(items, 1):
        out.append("<details><summary><span class='qn'>%d</span><span>%s</span>"
                   "<span class='car'>▶</span></summary><div class='ans'>%s</div></details>"
                   % (i, cellval(q), a if raw(a) else para(a)))
    return "".join(out)


def section(sid, num, title, kick=None, lead=None, cls=""):
    out = ['<section id="%s" class="%s">' % (e(sid), cls)]
    if num:
        out.append('<div class="sec-h%s"><div class="num">%s</div><div>' % (" mod" if cls.startswith("mod") else "", e(num)))
        if kick:
            out.append('<div class="sec-kick">%s</div>' % e(kick))
        out.append("<h2>%s</h2></div></div>" % e(title))
    else:
        if kick:
            out.append('<div class="sec-kick">%s</div>' % e(kick))
        out.append("<h2>%s</h2>" % e(title))
    if lead:
        out.append('<p class="sec-lead">%s</p>' % cellval(lead))
    return "".join(out)


NUMPAT = re.compile(r"^(\d+(\.\d+)*|[A-E](\.\d+)*)$")


def h3(a, b=None):
    """h3("4.1", "Title") or h3("Title"). Argument order is detected automatically."""
    if b is None:
        return "<h3>%s</h3>" % e(a)
    num, title = (a, b) if NUMPAT.match(str(a)) else (b, a)
    return '<h3><span class="hn">%s</span>%s</h3>' % (e(num), e(title))


def endsec():
    return "</section>"
