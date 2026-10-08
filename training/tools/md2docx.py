#!/usr/bin/env python3
"""Render the generated handbook HTML into a professionally formatted .docx.

The HTML build is the source of truth; this walks its DOM and emits an editable
Word document with the same content, the same structure and native Word versions
of the eight figures (see docx_diagrams.py).

Usage:  <venv>/bin/python training/tools/md2docx.py
"""

from __future__ import annotations

import os
import re
import sys

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from lxml import html as LH

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docx_diagrams as DG  # noqa: E402

IN = os.path.normpath(os.path.join(HERE, "..", "handbook", "index.html"))
OUT = os.path.normpath(os.path.join(HERE, "..", "handbook",
                                    "SAP-Migration-Training-Handbook-v1.0.docx"))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "handbook", "assets"))

NAVY = RGBColor(0x0F, 0x2B, 0x4C)
BLUE = RGBColor(0x1B, 0x4F, 0x86)
BODYC = RGBColor(0x33, 0x4E, 0x68)
MUTED = RGBColor(0x5B, 0x72, 0x88)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CODEC = RGBColor(0x12, 0x3A, 0x63)

BODY_FONT = "Calibri"
HEAD_FONT = "Calibri Light"
MONO_FONT = "Consolas"

BOX_STYLE = {
    "key": ("0F2B4C", "F4F7FB", "KEY POINT"),
    "warn": ("D9A520", "FFFDF5", "CAUTION"),
    "risk": ("C8434B", "FFFBFB", "CRITICAL"),
    "ok": ("3D9A5F", "F8FCF9", "GOOD PRACTICE"),
    "": ("1B4F86", "FBFCFE", "NOTE"),
}


# --------------------------------------------------------------------------- #
# low level OOXML helpers
# --------------------------------------------------------------------------- #
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k.replace("_", ":")), v)
    return e


def shade(el, fill):
    """Apply a solid fill. Accepts 'RRGGBB' or an RGBColor."""
    if not isinstance(fill, str):
        fill = str(fill)
    fill = fill.lstrip("#")
    if len(fill) != 6:
        return
    pr = el.get_or_add_tcPr() if el.tag.endswith("}tc") else el.get_or_add_pPr()
    pr.append(_el("w:shd", w_val="clear", w_color="auto", w_fill=fill))


def cell_shade(cell, fill):
    shade(cell._tc, fill)


def para_shade(p, fill):
    shade(p._p, fill)


def para_border(p, edges=("left",), color="1B4F86", size=18, space=6):
    pPr = p._p.get_or_add_pPr()
    bd = OxmlElement("w:pBdr")
    for e in edges:
        bd.append(_el("w:" + e, w_val="single", w_sz=str(size), w_space=str(space), w_color=color))
    pPr.append(bd)


def run_shade(run, fill):
    run._r.get_or_add_rPr().append(_el("w:shd", w_val="clear", w_color="auto", w_fill=fill))


def keep_with_next(p, on=True):
    pPr = p._p.get_or_add_pPr()
    k = OxmlElement("w:keepNext")
    if not on:
        k.set(qn("w:val"), "0")
    pPr.append(k)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def set_col_widths(table, widths_pct, avail=17.0):
    table.autofit = False
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    total = sum(widths_pct)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths_pct):
                cell.width = Cm(round(avail * widths_pct[i] / total, 2))
    for i, col in enumerate(table.columns):
        if i < len(widths_pct):
            col.width = Cm(round(avail * widths_pct[i] / total, 2))


def table_borders(table, color="C7D2E0", inner="DCE3EC"):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge, col in (("top", color), ("left", color), ("bottom", color),
                      ("right", color), ("insideH", inner), ("insideV", inner)):
        borders.append(_el("w:" + edge, w_val="single", w_sz="6", w_space="0", w_color=col))
    tblPr.append(borders)


def cell_margins(table, top=60, bottom=60, left=100, right=100):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for name, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        mar.append(_el("w:" + name, w_w=str(val), w_type="dxa"))
    tblPr.append(mar)


def field(paragraph, instr):
    r = paragraph.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    r._r.append(fld)
    r2 = paragraph.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    r2._r.append(it)
    r3 = paragraph.add_run()
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "separate")
    r3._r.append(fld2)
    r4 = paragraph.add_run("1")
    r5 = paragraph.add_run()
    fld3 = OxmlElement("w:fldChar")
    fld3.set(qn("w:fldCharType"), "end")
    r5._r.append(fld3)
    return [r, r2, r3, r4, r5]


# --------------------------------------------------------------------------- #
# inline HTML -> runs
# --------------------------------------------------------------------------- #
def add_runs(p, node, bold=False, italic=False, color=None, size=None, mono=False):
    """Walk an lxml element and emit runs, honouring b/strong, i/em, code and <br>."""
    color = color if color is not None else BODYC
    if node.text:
        _emit(p, node.text, bold, italic, color, size, mono)
    for child in node:
        tag = child.tag if isinstance(child.tag, str) else ""
        nb, ni, nm, nc = bold, italic, mono, color
        if tag in ("b", "strong"):
            nb = True
        elif tag in ("i", "em"):
            ni = True
        elif tag == "code":
            nm = True
            nc = CODEC
        elif tag == "br":
            p.add_run().add_break()
        elif tag in ("span", "a", "u"):
            if tag == "a":
                nc = BLUE
        add_runs(p, child, nb, ni, nc, size, nm)
        if child.tail:
            _emit(p, child.tail, bold, italic, color, size, mono)


def _emit(p, text, bold, italic, color, size, mono):
    text = re.sub(r"\s+", " ", text)
    if not text or text == " ":
        if text == " ":
            r = p.add_run(" ")
            r.font.name = MONO_FONT if mono else BODY_FONT
        return
    r = p.add_run(text)
    r.font.name = MONO_FONT if mono else BODY_FONT
    r.font.size = Pt(size) if size else Pt(10)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = color
    if mono:
        run_shade(r, "EEF2F7")


def plain(node):
    return re.sub(r"\s+", " ", "".join(node.itertext())).strip()


# --------------------------------------------------------------------------- #
# document setup
# --------------------------------------------------------------------------- #
def new_doc():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(10)
    st.font.color.rgb = BODYC
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.13
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), BODY_FONT)

    for name, size, color, before, after in (
            ("Heading 1", 21, NAVY, 0, 10), ("Heading 2", 16, NAVY, 20, 7),
            ("Heading 3", 12.5, BLUE, 15, 5), ("Heading 4", 11, RGBColor(0x17, 0x3A, 0x63), 12, 4)):
        s = doc.styles[name]
        s.font.name = HEAD_FONT if name in ("Heading 1", "Heading 2") else BODY_FONT
        s.font.size = Pt(size)
        s.font.bold = True
        s.font.color.rgb = color
        s.font.italic = False
        s.paragraph_format.space_before = Pt(before)
        s.paragraph_format.space_after = Pt(after)
        s.paragraph_format.keep_with_next = True
        r = s.element.get_or_add_rPr()
        rf2 = r.find(qn("w:rFonts"))
        if rf2 is None:
            rf2 = OxmlElement("w:rFonts")
            r.append(rf2)
        for a in ("w:ascii", "w:hAnsi", "w:cs"):
            rf2.set(qn(a), s.font.name)

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    sec.header_distance = Cm(1.0)
    sec.footer_distance = Cm(1.0)
    return doc



def new_section(doc, landscape=False):
    """Start a new page section, optionally rotated to landscape."""
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    else:
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    sec.header_distance = Cm(1.0)
    sec.footer_distance = Cm(1.0)
    return sec


def is_landscape(doc):
    return doc.sections[-1].orientation == WD_ORIENT.LANDSCAPE


def usable_width_cm(doc):
    sec = doc.sections[-1]
    return (sec.page_width.cm - sec.left_margin.cm - sec.right_margin.cm)


def enable_update_fields(doc):
    """Ask Word to refresh TOC/PAGE fields when the document is opened."""
    el = doc.settings.element
    if el.find(qn("w:updateFields")) is None:
        uf = OxmlElement("w:updateFields")
        uf.set(qn("w:val"), "true")
        el.append(uf)


def add_toc_field(doc, levels="1-2"):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run()
    b = OxmlElement("w:fldChar"); b.set(qn("w:fldCharType"), "begin"); r._r.append(b)
    r2 = p.add_run()
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = r' TOC \o "%s" \h \z \u ' % levels
    r2._r.append(it)
    r3 = p.add_run()
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate"); r3._r.append(sep)
    r4 = p.add_run("Word populates this table of contents on open (it will offer to update "
                   "fields). If it does not, select this line and press F9.")
    r4.italic = True
    r4.font.size = Pt(9)
    r4.font.color.rgb = MUTED
    r4.font.name = BODY_FONT
    r5 = p.add_run()
    e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); r5._r.append(e)
    return p


def header_footer(doc, title_text):
    for sec in doc.sections:
        sec.different_first_page_header_footer = True
        h = sec.header.paragraphs[0]
        h.text = ""
        h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = h.add_run(title_text)
        r.font.size = Pt(8)
        r.font.color.rgb = MUTED
        r.font.name = BODY_FONT
        para_border(h, edges=("bottom",), color="C7D2E0", size=6, space=4)

        f = sec.footer.paragraphs[0]
        f.text = ""
        f.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = f.add_run("Internal — training use   ·   SAP-MIG-TRN-HB-001   ·   v1.0   ·   Page ")
        r1.font.size = Pt(8)
        r1.font.color.rgb = MUTED
        for rr in field(f, "PAGE"):
            rr.font.size = Pt(8)
            rr.font.color.rgb = MUTED
        r2 = f.add_run(" of ")
        r2.font.size = Pt(8)
        r2.font.color.rgb = MUTED
        for rr in field(f, "NUMPAGES"):
            rr.font.size = Pt(8)
            rr.font.color.rgb = MUTED
        para_border(f, edges=("top",), color="C7D2E0", size=6, space=4)


# --------------------------------------------------------------------------- #
# block emitters
# --------------------------------------------------------------------------- #
def emit_table(doc, headers, rows, widths=None, caption=None, fills=None,
               header_fill="0F2B4C", body_size=8.6, header_size=8.6, first_col_bold=True):
    if caption:
        p = doc.add_paragraph()
        r = p.add_run(caption.upper())
        r.font.size = Pt(7.8)
        r.bold = True
        r.font.color.rgb = MUTED
        r.font.name = BODY_FONT
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.space_before = Pt(8)
        keep_with_next(p)
    ncols = len(headers) if headers else max((len(r) for r in rows), default=1)
    nrows = len(rows) + (1 if headers else 0)
    t = doc.add_table(rows=nrows, cols=ncols)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.style = "Table Grid"
    table_borders(t)
    cell_margins(t)
    ri = 0
    if headers:
        for ci, htxt in enumerate(headers):
            c = t.cell(0, ci)
            c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            if isinstance(htxt, str):
                r = p.add_run(re.sub(r"<[^>]+>", "", htxt))
                r.bold = True
                r.font.size = Pt(header_size)
                r.font.color.rgb = WHITE
                r.font.name = BODY_FONT
            cell_shade(c, header_fill)
        repeat_header(t.rows[0])
        cant_split(t.rows[0])
        ri = 1
    for ridx, row in enumerate(rows):
        cant_split(t.rows[ri + ridx])
        for ci in range(ncols):
            val = row[ci] if ci < len(row) else ""
            c = t.cell(ri + ridx, ci)
            c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            if hasattr(val, "tag"):
                add_runs(p, val, bold=(first_col_bold and ci == 0),
                         size=body_size)
            else:
                for k, chunk in enumerate(str(val).split("\n")):
                    if k:
                        p = c.add_paragraph()
                        p.paragraph_format.space_after = Pt(1)
                        p.paragraph_format.space_before = Pt(1)
                    r = p.add_run(chunk)
                    r.font.size = Pt(body_size)
                    r.font.name = BODY_FONT
                    r.bold = first_col_bold and ci == 0
                    r.font.color.rgb = NAVY if (first_col_bold and ci == 0) else BODYC
            fill = None
            if fills and ridx < len(fills) and ci < len(fills[ridx]):
                fill = fills[ridx][ci]
            elif not headers and fills and ridx < len(fills):
                fill = fills[ridx][0] if isinstance(fills[ridx], str) else None
            if fill is None and headers and ridx % 2 == 1:
                fill = "FAFBFD"
            if fill:
                cell_shade(c, fill)
    if widths:
        try:
            set_col_widths(t, [float(str(w).replace("%", "")) for w in widths],
                           avail=usable_width_cm(doc))
        except (ValueError, TypeError):
            pass
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def emit_box(doc, kind, label, blocks):
    accent, fill, default_label = BOX_STYLE.get(kind, BOX_STYLE[""])
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(2)
    para_shade(p, fill)
    para_border(p, edges=("left", "top", "right"), color=accent, size=6, space=6)
    r = p.add_run((label or default_label).upper())
    r.bold = True
    r.font.size = Pt(8)
    r.font.name = BODY_FONT
    r.font.color.rgb = RGBColor.from_string(accent)
    keep_with_next(p)
    for i, b in enumerate(blocks):
        last = i == len(blocks) - 1
        emit_block(doc, b, inset=True, fill=fill, accent=accent, last=last)
    if not blocks:
        q = doc.add_paragraph()
        para_shade(q, fill)
        para_border(q, edges=("left", "bottom", "right"), color=accent, size=6, space=6)


def _br_lines(node):
    """Extract lines from a block where line breaks are <br> elements."""
    lines, cur = [], ""

    def walk(n):
        nonlocal cur
        cur += n.text or ""
        for c in n:
            if c.tag == "br":
                lines.append(cur)
                cur = ""
            else:
                walk(c)
            cur += c.tail or ""
    walk(node)
    lines.append(cur)
    return [l.replace("\u00a0", " ").rstrip() for l in lines if l.strip()]


def emit_cmd(doc, node):
    lines = _br_lines(node)
    for i, l in enumerate(lines):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6 if i == 0 else 0)
        p.paragraph_format.space_after = Pt(6 if i == len(lines) - 1 else 0)
        p.paragraph_format.left_indent = Cm(0.3)
        para_shade(p, "0E2340")
        para_border(p, edges=("left",), color="1B4F86", size=18, space=4)
        r = p.add_run(l if l.strip() else " ")
        r.font.name = MONO_FONT
        r.font.size = Pt(8.2)
        r.font.color.rgb = RGBColor(0xD6, 0xE4, 0xF5)
        if l.strip().startswith("#") or l.strip().startswith("--"):
            r.font.color.rgb = RGBColor(0x7F, 0xA2, 0xC8)


def emit_list(doc, node, ordered, inset=False, fill=None, accent=None):
    items = node.findall("./li")
    for i, li in enumerate(items):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm((1.0 if inset else 0.62) + (0.4 if ordered else 0))
        p.paragraph_format.first_line_indent = Cm(-0.4)
        if fill:
            para_shade(p, fill)
        if accent and i == 0:
            pass
        bullet = "%d.  " % (i + 1) if ordered else "▪  "
        r = p.add_run(bullet)
        r.font.size = Pt(9.5)
        r.font.color.rgb = BLUE if not ordered else NAVY
        r.bold = True
        r.font.name = BODY_FONT
        add_runs(p, li, size=9.8)


def emit_figure(doc, slug, caption):
    png = os.path.join(ASSETS, slug + ".png")
    if os.path.exists(png):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        keep_with_next(p)
        run = p.add_run()
        run.add_picture(png, width=Cm(min(usable_width_cm(doc), 24.7)))
        if caption is not None:
            cp = doc.add_paragraph()
            cp.paragraph_format.space_after = Pt(12)
            r = cp.add_run(re.sub(r"\s+", " ", caption.text_content()).strip())
            r.font.size = Pt(8.6)
            r.italic = True
            r.font.color.rgb = MUTED
            r.font.name = BODY_FONT
        return
    ops = DG.FIGS[slug]() if slug in DG.FIGS else None
    if not ops:
        return
    for op in ops:
        kind = op[0]
        if kind == "title":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(op[1])
            r.bold = True
            r.font.size = Pt(11.5)
            r.font.color.rgb = NAVY
            r.font.name = BODY_FONT
            keep_with_next(p)
        elif kind == "sub":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            r = p.add_run(op[1])
            r.font.size = Pt(8.8)
            r.italic = True
            r.font.color.rgb = MUTED
            r.font.name = BODY_FONT
            keep_with_next(p)
        elif kind == "band":
            txt, fillc = op[1], op[2]
            colr = RGBColor.from_string(op[3]) if len(op) > 3 else WHITE
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(2)
            para_shade(p, fillc)
            r = p.add_run(txt)
            r.bold = True
            r.font.size = Pt(8.6)
            r.font.color.rgb = colr
            r.font.name = BODY_FONT
        elif kind == "flow":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            para_shade(p, "F4F7FB")
            para_border(p, edges=("left",), color="1B4F86", size=18, space=6)
            for i, st in enumerate(op[1]):
                if i:
                    a = p.add_run("   →   ")
                    a.font.size = Pt(9)
                    a.font.color.rgb = RGBColor(0x9E, 0xC3, 0xEC)
                    a.bold = True
                r = p.add_run(st)
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = NAVY
                r.font.name = BODY_FONT
        elif kind == "table":
            _h, rows, widths, fills = op[1], op[2], op[3], op[4]
            emit_table(doc, _h, rows, widths=widths, fills=fills,
                       header_fill="0F2B4C" if _h else "FFFFFF", body_size=8.4)
        elif kind == "note":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(8)
            r = p.add_run(op[1])
            r.font.size = Pt(8)
            r.italic = True
            r.font.color.rgb = MUTED
            r.font.name = BODY_FONT
        elif kind == "gap":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
    if caption is not None:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        r = p.add_run(re.sub(r"\s+", " ", caption.text_content()).strip())
        r.font.size = Pt(8.6)
        r.italic = True
        r.font.color.rgb = MUTED
        r.font.name = BODY_FONT


def emit_block(doc, b, inset=False, fill=None, accent=None, last=False):
    tag = b.tag if isinstance(b.tag, str) else ""
    if tag == "p":
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2 if last else 6)
        p.paragraph_format.left_indent = Cm(0.3) if inset else None
        if fill:
            para_shade(p, fill)
        if inset and last and accent:
            para_border(p, edges=("left", "bottom", "right"), color=accent, size=6, space=6)
        elif inset and accent:
            para_border(p, edges=("left", "right"), color=accent, size=6, space=6)
        add_runs(p, b, size=9.4 if inset else 10)
    elif tag in ("ul", "ol"):
        emit_list(doc, b, tag == "ol", inset=inset, fill=fill, accent=accent)
        if inset and last and accent:
            p = doc.add_paragraph()
            para_shade(p, fill)
            para_border(p, edges=("left", "bottom", "right"), color=accent, size=6, space=6)
            p.paragraph_format.space_after = Pt(2)
    elif tag == "h5":
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.3) if inset else None
        if fill:
            para_shade(p, fill)
        r = p.add_run(plain(b).upper())
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = MUTED
        r.font.name = BODY_FONT
    elif tag in ("div",) and "grid" in (b.get("class") or ""):
        for card in b.iter("div"):
            cls = card.get("class") or ""
            if cls.startswith("card") or cls.startswith("kpi"):
                emit_card(doc, card, fill=fill)
    elif tag == "div" and b.get("class") and "box" in b.get("class"):
        kind = (b.get("class") or "").split()[1] if len((b.get("class") or "").split()) > 1 else ""
        lbl = b.find("./div[@class='lbl']")
        label = plain(lbl) if lbl is not None else ""
        inner = [c for c in b if c is not lbl]
        emit_box(doc, kind, label, inner)
    else:
        for c in b:
            emit_block(doc, c, inset=inset, fill=fill, accent=accent)


def emit_card(doc, card, fill=None):
    h = card.find("./h4")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(1)
    para_shade(p, fill or "F7F9FC")
    para_border(p, edges=("left",), color="9EC3EC", size=18, space=6)
    if h is not None:
        r = p.add_run(plain(h))
        r.bold = True
        r.font.size = Pt(9.6)
        r.font.color.rgb = NAVY
        r.font.name = BODY_FONT
    body = [c for c in card if c is not h]
    for c in body:
        emit_block(doc, c, inset=True, fill=fill or "F7F9FC", accent="9EC3EC")


# --------------------------------------------------------------------------- #
# checklist / qa
# --------------------------------------------------------------------------- #
def emit_checklist(doc, table_el):
    rows = table_el.findall("./tbody/tr")
    heads = [plain(th) for th in table_el.findall("./thead/tr/th")]
    data = []
    fills = []
    for tr in rows:
        tds = tr.findall("./td")
        item = plain(tds[1]) if len(tds) > 1 else ""
        status = tds[2].find(".//option") if len(tds) > 2 else None
        stat = plain(status) if status is not None else "Not Started"
        data.append(["☐", item, stat, ""])
        fills.append(["FFFFFF"] * 4)
    emit_table(doc, ["☐", heads[1] if len(heads) > 1 else "Check",
                     heads[2] if len(heads) > 2 else "Status",
                     heads[3] if len(heads) > 3 else "Evidence / remarks"],
               data, widths=[5, 47, 16, 32], fills=fills, body_size=8.8,
               first_col_bold=False)


def emit_qa(doc, details_list):
    for i, d in enumerate(details_list, 1):
        summ = d.find("./summary")
        ans = None
        for dv in d.findall("./div"):
            if "ans" in (dv.get("class") or ""):
                ans = dv
                break
        if summ is None:
            continue
        qtexts = [plain(s) for s in summ.findall("./span")]
        qtexts = [q for q in qtexts if q and q != "▶"]
        q = qtexts[0] if qtexts else ""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        para_shade(p, "F4F7FB")
        para_border(p, edges=("left", "top", "right"), color="9EC3EC", size=6, space=6)
        r = p.add_run("Q%d.  " % i)
        r.bold = True
        r.font.size = Pt(9.8)
        r.font.color.rgb = BLUE
        r.font.name = BODY_FONT
        r2 = p.add_run(re.sub(r"<[^>]+>", "", q))
        r2.bold = True
        r2.font.size = Pt(9.8)
        r2.font.color.rgb = NAVY
        r2.font.name = BODY_FONT
        keep_with_next(p)
        if ans is not None:
            kids = [c for c in ans]
            for j, c in enumerate(kids):
                emit_block(doc, c, inset=True, fill="FBFCFE", accent="9EC3EC", last=(j == len(kids) - 1))
            if not kids:
                p2 = doc.add_paragraph()
                para_shade(p2, "FBFCFE")
                para_border(p2, edges=("left", "bottom", "right"), color="9EC3EC", size=6, space=6)
                add_runs(p2, ans, size=9.6)


# --------------------------------------------------------------------------- #
# cover
# --------------------------------------------------------------------------- #
def emit_cover(doc, cover_el):
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("CONSOLIDATED TRAINING MATERIAL · 2026")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = BLUE
    r.font.name = BODY_FONT

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("SAP Migration")
    r.bold = True
    r.font.size = Pt(34)
    r.font.color.rgb = NAVY
    r.font.name = HEAD_FONT
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Training Handbook")
    r.bold = True
    r.font.size = Pt(34)
    r.font.color.rgb = NAVY
    r.font.name = HEAD_FONT

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(14)
    para_border(p, edges=("bottom",), color="1B4F86", size=18, space=8)

    lede = cover_el.find("./p[@class='lede']")
    if lede is not None:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(16)
        r = p.add_run(re.sub(r"\s+", " ", lede.text_content()).strip())
        r.font.size = Pt(11)
        r.font.color.rgb = BODYC
        r.font.name = BODY_FONT

    tags = cover_el.find("./div[@class='tags']")
    if tags is not None:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(18)
        for i, sp in enumerate(tags.findall("./span")):
            if i:
                sep = p.add_run("    ·    ")
                sep.font.size = Pt(9)
                sep.font.color.rgb = RGBColor(0x9E, 0xC3, 0xEC)
            r = p.add_run(re.sub(r"\s+", " ", sp.text_content()).strip())
            r.font.size = Pt(9)
            r.bold = True
            r.font.color.rgb = BLUE
            r.font.name = BODY_FONT

    ctl = cover_el.find("./dl[@class='docctl']")
    rows = []
    if ctl is not None:
        for div in ctl.findall("./div"):
            dt = div.find("./dt")
            dd = div.find("./dd")
            rows.append([plain(dt) if dt is not None else "", plain(dd) if dd is not None else ""])
    emit_table(doc, ["Field", "Value"], rows, widths=[28, 72], body_size=9,
               caption="Document control")

    stamp = cover_el.find("./p[@class='stamp']")
    if stamp is not None:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        para_shade(p, "F4F7FB")
        para_border(p, edges=("left",), color="1B4F86", size=18, space=6)
        add_runs(p, stamp, size=8.8, color=MUTED)
    doc.add_page_break()


# --------------------------------------------------------------------------- #
# main walk
# --------------------------------------------------------------------------- #
def _by_class(parent, cls, tag="div", direct=True):
    """Find the first child whose class list starts with `cls` (handles 'sec-h mod')."""
    for c in parent:
        if tag and c.tag != tag:
            continue
        classes = (c.get("class") or "").split()
        if classes and classes[0] == cls:
            return c
    return None


def emit_section(doc, sec, first=False):
    sid = sec.get("id") or ""
    head = _by_class(sec, "sec-h")
    num = title_txt = kick = None
    if head is not None:
        nd = head.find("./div[@class='num']")
        num = plain(nd) if nd is not None else None
        h2 = head.find(".//h2")
        title_txt = plain(h2) if h2 is not None else None
        k = head.find(".//div[@class='sec-kick']")
        kick = plain(k) if k is not None else None
    else:
        h2 = sec.find("./h2")
        title_txt = plain(h2) if h2 is not None else None
        k = sec.find("./div[@class='sec-kick']")
        kick = plain(k) if k is not None else None

    if not first:
        doc.add_page_break()
    if kick:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(kick.upper())
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = BLUE
        r.font.name = BODY_FONT
    label = ("%s  %s" % (num, title_txt)).strip() if num and num != "—" else (title_txt or "")
    if label:
        h = doc.add_heading(level=1)
        r = h.add_run(label)
        r.font.size = Pt(19)
        r.font.color.rgb = NAVY
        r.bold = True
        r.font.name = HEAD_FONT
        para_border(h, edges=("bottom",), color="1B4F86", size=12, space=5)
        h.paragraph_format.space_after = Pt(8)
    lead = sec.find("./p[@class='sec-lead']")
    if lead is not None:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        r = p.add_run(re.sub(r"\s+", " ", lead.text_content()).strip())
        r.font.size = Pt(10.5)
        r.italic = True
        r.font.color.rgb = MUTED
        r.font.name = BODY_FONT

    skip = {head}
    if lead is not None:
        skip.add(lead)
    kick_el = sec.find("./div[@class='sec-kick']")
    if kick_el is not None:
        skip.add(kick_el)
    for child in sec:
        if child in skip:
            continue
        emit_child(doc, child)


def emit_child(doc, el):
    tag = el.tag if isinstance(el.tag, str) else ""
    cls = el.get("class") or ""
    if tag == "h3":
        h = doc.add_heading(level=2)
        hn = el.find("./span[@class='hn']")
        num = plain(hn) if hn is not None else ""
        txt = plain(el)
        if num and txt.startswith(num):
            txt = txt[len(num):].strip()
        r = h.add_run(("%s  %s" % (num, txt)).strip())
        r.font.size = Pt(13)
        r.font.color.rgb = NAVY
        r.bold = True
        r.font.name = BODY_FONT
        para_border(h, edges=("bottom",), color="E8EDF3", size=6, space=3)
    elif tag == "h4":
        h = doc.add_heading(level=3)
        r = h.add_run(plain(el))
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x17, 0x3A, 0x63)
        r.bold = True
        r.font.name = BODY_FONT
    elif tag == "p":
        if "tnote" in cls:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(8)
            r = p.add_run(plain(el))
            r.font.size = Pt(8)
            r.italic = True
            r.font.color.rgb = MUTED
            r.font.name = BODY_FONT
        else:
            p = doc.add_paragraph()
            add_runs(p, el, size=10)
    elif tag in ("ul", "ol"):
        emit_list(doc, el, tag == "ol")
    elif tag == "div" and cls.startswith("tw"):
        t = el.find("./table")
        if t is None:
            return
        if "ck" in (t.get("class") or ""):
            emit_checklist(doc, t)
            return
        cap = t.find("./caption")
        heads = [th for th in t.findall("./thead/tr/th")]
        rows = t.findall("./tbody/tr")
        wide = len(heads) >= 6
        if wide:
            new_section(doc, landscape=True)
        widths = None
        cg = t.find("./colgroup")
        if cg is not None:
            ws = [c.get("style", "") for c in cg.findall("./col")]
            widths = [re.sub(r"[^\d.]", "", w) or "1" for w in ws]
        data = []
        for tr in rows:
            data.append([td for td in tr.findall("./td")])
        emit_table(doc,
                   [re.sub(r"<[^>]+>", "", plain(th)) for th in heads] if heads else None,
                   data, widths=widths, caption=plain(cap) if cap is not None else None,
                   body_size=8.6)
        if wide:
            new_section(doc, landscape=False)
    elif tag == "div" and cls.startswith("box"):
        parts = cls.split()
        kind = parts[1] if len(parts) > 1 else ""
        lbl = el.find("./div[@class='lbl']")
        label = plain(lbl) if lbl is not None else ""
        inner = [c for c in el if c is not lbl]
        emit_box(doc, kind, label, inner)
    elif tag == "div" and cls.startswith("grid"):
        cards = [c for c in el.iter("div") if (c.get("class") or "").startswith(("card", "kpi"))]
        seen = set()
        for c in cards:
            if id(c) in seen:
                continue
            seen.add(id(c))
            if (c.get("class") or "").split()[0] not in ("card", "kpi"):
                continue
            if (c.get("class") or "").startswith("kpi"):
                k = c.find("./div[@class='k']")
                v = c.find("./div[@class='v']")
                d = c.find("./div[@class='d']")
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(5)
                p.paragraph_format.space_after = Pt(1)
                para_shade(p, "F4F7FB")
                para_border(p, edges=("left",), color="1B4F86", size=18, space=6)
                r = p.add_run(plain(v) if v is not None else "")
                r.bold = True
                r.font.size = Pt(13)
                r.font.color.rgb = NAVY
                r.font.name = BODY_FONT
                r2 = p.add_run("   " + (plain(k) if k is not None else "").upper())
                r2.font.size = Pt(8)
                r2.bold = True
                r2.font.color.rgb = MUTED
                r2.font.name = BODY_FONT
                if d is not None:
                    p2 = doc.add_paragraph()
                    para_shade(p2, "F4F7FB")
                    para_border(p2, edges=("left",), color="1B4F86", size=18, space=6)
                    p2.paragraph_format.space_after = Pt(4)
                    r3 = p2.add_run(plain(d))
                    r3.font.size = Pt(8.6)
                    r3.font.color.rgb = MUTED
                    r3.font.name = BODY_FONT
            else:
                emit_card(doc, c)
    elif tag == "div" and cls.startswith("flowline"):
        steps = [plain(b) for b in el.findall("./b")]
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(8)
        para_shade(p, "F4F7FB")
        para_border(p, edges=("left",), color="1B4F86", size=18, space=6)
        for i, st in enumerate(steps):
            if i:
                a = p.add_run("  →  ")
                a.font.size = Pt(9)
                a.bold = True
                a.font.color.rgb = RGBColor(0x9E, 0xC3, 0xEC)
            r = p.add_run(st)
            r.bold = True
            r.font.size = Pt(9.2)
            r.font.color.rgb = NAVY
            r.font.name = BODY_FONT
    elif tag == "div" and cls.startswith("cmd"):
        emit_cmd(doc, el)
    elif tag == "figure":
        slug = (el.get("id") or "").replace("fig-", "")
        cap = el.find("./figcaption")
        new_section(doc, landscape=True)
        emit_figure(doc, slug, cap)
        new_section(doc, landscape=False)
    elif tag == "details":
        emit_qa(doc, [el])
    elif tag == "div" and cls.startswith("ck-tools"):
        return
    elif tag == "section":
        emit_section(doc, el)
    else:
        for c in el:
            emit_child(doc, c)


def build_toc(doc, tree):
    doc.add_heading("Table of contents", level=1)
    p = doc.paragraphs[-1]
    para_border(p, edges=("bottom",), color="1B4F86", size=12, space=5)
    secs = tree.xpath("//main//section")
    add_toc_field(doc, "1-2")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run("All headings carry Word outline levels, so the field above resolves to a live, "
                  "page-numbered, hyperlinked table of contents. The figure index and the detailed "
                  "contents live in the “Contents and figure index” section of the handbook itself.")
    r.font.size = Pt(8.4)
    r.italic = True
    r.font.color.rgb = MUTED
    r.font.name = BODY_FONT


def main():
    src = open(IN, encoding="utf-8").read()
    tree = LH.fromstring(src)
    doc = new_doc()
    core = doc.core_properties
    core.title = "SAP Migration Training Handbook"
    core.subject = "SAP → AWS Migration | HANA | Oracle | Basis Validation | Cutover | Hypercare"
    core.author = "Amit Prajapati"
    core.category = "Consolidated Training & Knowledge Transfer Handbook"
    core.comments = ("Version 1.0 — vetted release. Consolidated from the supplied training/MOM source "
                     "document. Internal training use; does not replace approved project runbooks.")
    core.keywords = "SAP, AWS, HANA, Oracle, Data Guard, migration, cutover, hypercare, Basis, validation"

    cover = tree.xpath("//header[@class='cover']")[0]
    if cover is not None:
        emit_cover(doc, cover)
    enable_update_fields(doc)
    header_footer(doc, "SAP Migration Training Handbook · v1.0 · Internal")
    build_toc(doc, tree)
    for sec in tree.xpath("//main//section"):
        emit_section(doc, sec)

    doc.save(OUT)
    size = os.path.getsize(OUT)
    print("built %s (%.1f KB, %d paragraphs, %d tables)"
          % (OUT, size / 1024, len(doc.paragraphs), len(doc.tables)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
