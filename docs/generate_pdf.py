#!/usr/bin/env python3
"""
Generate Tier-1 Enhanced PDF for AI SRE Copilot Dev Pilot
Using ReportLab Platypus. Professional consulting grade.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem,
    Image, Frame, PageTemplate, NextPageTemplate, BaseDocTemplate
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUT = "docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.pdf"

# Colors
NAVY = HexColor("#0B1F4A")
NAVY2 = HexColor("#132C63")
NAVY3 = HexColor("#1E3A8A")
TEAL = HexColor("#0E7490")
TEAL_LIGHT = HexColor("#ECFEFF")
GOLD = HexColor("#C5A880")
GOLD_DARK = HexColor("#A68B5B")
SLATE = HexColor("#475569")
SLATE_LIGHT = HexColor("#64748B")
SLATE_50 = HexColor("#F8FAFC")
SLATE_100 = HexColor("#F1F5F9")
SLATE_200 = HexColor("#E2E8F0")
GREEN = HexColor("#059669")
GREEN_LIGHT = HexColor("#ECFDF5")
AMBER = HexColor("#D97706")
AMBER_LIGHT = HexColor("#FFFBEB")
RED = HexColor("#DC2626")
RED_LIGHT = HexColor("#FEF2F2")
BLUE_LIGHT = HexColor("#EFF6FF")

W, H = A4

styles = getSampleStyleSheet()

# Custom styles
sTitle = ParagraphStyle('Title2', parent=styles['Title'], fontSize=28, leading=30, textColor=NAVY, fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=6)
sH1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, leading=19, textColor=NAVY, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8, keepWithNext=True)
sH2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, leading=15, textColor=NAVY, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6)
sH3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=10, leading=13, textColor=TEAL, fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4)
sKicker = ParagraphStyle('Kicker', parent=styles['Normal'], fontSize=7, leading=9, textColor=TEAL, fontName='Helvetica-Bold', spaceAfter=2, textTransform='uppercase')
sBody = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13.5, textColor=HexColor("#334155"), fontName='Helvetica', spaceAfter=6, alignment=TA_JUSTIFY)
sBodySmall = ParagraphStyle('BodySmall', parent=sBody, fontSize=8, leading=11.5, spaceAfter=4)
sBullet = ParagraphStyle('Bullet', parent=sBody, leftIndent=12, bulletIndent=0, spaceAfter=3, alignment=TA_LEFT)
sCaption = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=7, leading=9, textColor=SLATE_LIGHT, fontName='Helvetica-Oblique', alignment=TA_CENTER, spaceAfter=6)
sTableHead = ParagraphStyle('TableHead', parent=styles['Normal'], fontSize=7, leading=9, textColor=white, fontName='Helvetica-Bold', alignment=TA_CENTER)
sTableCell = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=HexColor("#334155"), fontName='Helvetica', alignment=TA_LEFT)
sTableCellSmall = ParagraphStyle('TableCellSmall', parent=sTableCell, fontSize=7, leading=9)
sCoverTitle = ParagraphStyle('CoverTitle', parent=styles['Title'], fontSize=32, leading=32, textColor=white, fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=6)
sCoverSub = ParagraphStyle('CoverSub', parent=styles['Normal'], fontSize=10, leading=14, textColor=HexColor("#DBEAFE"), fontName='Helvetica', alignment=TA_LEFT, spaceAfter=8)
sCoverMetaDt = ParagraphStyle('CoverMetaDt', parent=styles['Normal'], fontSize=6, leading=8, textColor=HexColor("#93C5FD"), fontName='Helvetica-Bold', alignment=TA_LEFT)
sCoverMetaDd = ParagraphStyle('CoverMetaDd', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=HexColor("#E0E7FF"), fontName='Helvetica', alignment=TA_LEFT)
sFooter = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=6, leading=7.5, textColor=SLATE_LIGHT, fontName='Helvetica', alignment=TA_LEFT)

def header_footer(canvas, doc):
    canvas.saveState()
    # Top thin line
    if doc.page == 1:
        canvas.restoreState()
        return
    # Header
    canvas.setStrokeColor(SLATE_200)
    canvas.setLineWidth(0.5)
    canvas.line(18*mm, H-14*mm, W-18*mm, H-14*mm)
    canvas.setFont("Helvetica-Bold", 6)
    canvas.setFillColor(NAVY)
    canvas.drawString(18*mm, H-11*mm, "QUANTUM INTEGRATORS  —  INTERNAL PROPOSAL")
    canvas.setFont("Helvetica", 6)
    canvas.setFillColor(SLATE_LIGHT)
    canvas.drawRightString(W-18*mm, H-11*mm, "QI-AI-SRE-2026-001  •  v2.0 Enhanced  •  Confidential")
    # Footer
    canvas.setStrokeColor(SLATE_200)
    canvas.line(18*mm, 14*mm, W-18*mm, 14*mm)
    canvas.setFont("Helvetica", 6)
    canvas.setFillColor(SLATE_LIGHT)
    canvas.drawString(18*mm, 11*mm, "Confidential — QI Internal • GSK excluded • AI proposes  •  Policy validates  •  Human approves  •  Workflow executes")
    canvas.drawRightString(W-18*mm, 11*mm, f"Page {doc.page}")
    # Confidential bar on each page top after header?
    canvas.restoreState()

def styled_table(data, col_widths, header=True, zebra=True, header_color=NAVY, font_size=7.5):
    """Create a styled table with header and zebra."""
    # Convert strings to Paragraphs if needed
    table_data = []
    for r_idx, row in enumerate(data):
        new_row = []
        for c_idx, cell in enumerate(row):
            if isinstance(cell, str):
                # check if header row
                if r_idx == 0 and header:
                    p = Paragraph(cell, sTableHead)
                else:
                    p = Paragraph(cell, ParagraphStyle('tc', parent=sTableCell, fontSize=font_size, leading=font_size+2.5))
                new_row.append(p)
            else:
                new_row.append(cell)
        table_data.append(new_row)
    t = Table(table_data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, SLATE_50]) if zebra else ('BACKGROUND', (0,0), (-1,0), header_color),
        ('BACKGROUND', (0,0), (-1,0), header_color) if header else ('BACKGROUND', (0,0), (-1,0), white),
        ('TEXTCOLOR', (0,0), (-1,0), white) if header else ('TEXTCOLOR', (0,0), (-1,0), SLATE),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]
    t.setStyle(TableStyle(style))
    return t

def callout(text_title, text_body, color_bg, color_border, color_icon_bg, icon="ℹ"):
    """Create a callout box as a table."""
    title = Paragraph(f"<b>{text_title}</b>", ParagraphStyle('calloutTitle', parent=sBody, fontSize=8, leading=10, textColor=NAVY, fontName='Helvetica-Bold', spaceAfter=2))
    body = Paragraph(text_body, ParagraphStyle('calloutBody', parent=sBody, fontSize=8, leading=11, textColor=HexColor("#334155"), alignment=TA_LEFT, spaceAfter=0))
    inner = [[title],[body]]
    inner_table = Table(inner, colWidths=[460])
    inner_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    icon_para = Paragraph(f"<font size=10>{icon}</font>", ParagraphStyle('icon', parent=sBody, alignment=TA_CENTER, textColor=NAVY, fontSize=10))
    icon_cell = Table([[icon_para]], colWidths=[22], rowHeights=[22])
    icon_cell.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_icon_bg),
        ('ROUNDEDCORNERS', [11,11,11,11]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    # Outer
    outer = Table([[icon_cell, inner_table]], colWidths=[28, 466])
    outer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_bg),
        ('BOX', (0,0), (-1,-1), 0.7, color_border),
        ('ROUNDEDCORNERS', [6,6,6,6]),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return outer

def kpi_card(icon, title, desc, bg=white):
    title_p = Paragraph(f"<b>{title}</b>", ParagraphStyle('kpiT', parent=sBody, fontSize=8, textColor=NAVY, fontName='Helvetica-Bold', spaceAfter=2, leading=10))
    desc_p = Paragraph(desc, ParagraphStyle('kpiD', parent=sBody, fontSize=7.5, leading=10, textColor=SLATE, spaceAfter=0))
    inner = Table([[title_p],[desc_p]], colWidths=[140])
    inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    icon_p = Paragraph(f"<font size=9>{icon}</font>", ParagraphStyle('kpiI', parent=sBody, alignment=TA_CENTER, fontSize=9, textColor=NAVY))
    icon_box = Table([[icon_p]], colWidths=[24], rowHeights=[24])
    icon_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), BLUE_LIGHT),('ROUNDEDCORNERS',[6,6,6,6]),('BOX',(0,0),(-1,-1),0.5, SLATE_200)]))
    outer = Table([[icon_box, inner]], colWidths=[30, 144])
    outer.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), bg),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('ROUNDEDCORNERS',[8,8,8,8]),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    return outer

def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=16*mm, bottomMargin=16*mm,
        title="AI SRE Copilot — Dev Pilot Proposal — Quantum Integrators — Enhanced Tier-1 Edition",
        author="Quantum Integrators"
    )

    story = []

    # COVER PAGE - custom drawing via flowables
    # We'll create cover as a series of elements with background color simulated via table
    # Cover background - full page color handled in onFirstPage
    def cover_background(canvas, doc):
        canvas.saveState()
        # Full navy background
        canvas.setFillColor(NAVY)
        canvas.rect(0,0,W,H, fill=1, stroke=0)
        # Gold line at bottom
        canvas.setFillColor(GOLD)
        canvas.rect(0, 12*mm, W, 3*mm, fill=1, stroke=0)
        # Subtle gradient effect via lighter rect
        canvas.setFillColor(NAVY3)
        canvas.setStrokeColor(HexColor("#1E3A8A"))
        # Top highlight
        canvas.setFillColor(HexColor("#1E3A8A"))
        canvas.setFillAlpha(0.5)
        canvas.rect(0, H-80*mm, W, 80*mm, fill=1, stroke=0)
        canvas.setFillAlpha(1)
        canvas.restoreState()
        # Header/footer not for cover
        header_footer(canvas, doc)  # but we skip page 1 logic

    # To make cover we will use a NextPageTemplate approach: first page is cover with custom background
    # Simplest: add cover content, then set onFirstPage to cover_background, onLaterPages to header_footer
    # We'll build story normally and assign page functions at doc.build

    # Cover content
    # Eyebrow
    story.append(Spacer(1, 6*mm))
    eyebrow = Paragraph('<font color="#93C5FD" size=6><b>INTERNAL DEVELOPMENT PILOT  •  GOOGLE CLOUD  •  GSK EXCLUDED</b></font>', ParagraphStyle('eyebrow', parent=sBody, textColor=HexColor("#93C5FD"), fontSize=6, alignment=TA_LEFT, spaceAfter=4))
    story.append(eyebrow)
    # Thin gold line
    story.append(HRFlowable(width="12%", thickness=1.2, color=GOLD, spaceAfter=6, spaceBefore=2, hAlign='LEFT'))
    # Title
    story.append(Paragraph('<font color="white">AI SRE Copilot</font>', ParagraphStyle('ct1', parent=sCoverTitle, fontSize=36, leading=34, textColor=white, fontName='Helvetica-Bold')))
    story.append(Paragraph('<font color="#93C5FD"><i>Dev Pilot</i></font>', ParagraphStyle('ct2', parent=sCoverTitle, fontSize=36, leading=34, textColor=HexColor("#93C5FD"), fontName='Helvetica-Oblique')))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('A controlled, evidence-linked AI diagnosis service with deterministic policy validation and mandatory human approval — built entirely in QI’s internal GCP project. No GSK data, credentials, or environments.', ParagraphStyle('csub', parent=sCoverSub, textColor=HexColor("#DBEAFE"), fontSize=10, leading=14)))
    story.append(Spacer(1, 4*mm))
    # Badges row as table
    badges = [
        Paragraph('<font color="#0B1F4A"><b>4–6 WEEKS</b></font>', ParagraphStyle('b1', parent=sBody, fontSize=6, textColor=NAVY, alignment=TA_CENTER, fontName='Helvetica-Bold')),
        Paragraph('<font color="white">≤ 20 Cloud Run services</font>', ParagraphStyle('b2', parent=sBody, fontSize=6, textColor=white, alignment=TA_CENTER)),
        Paragraph('<font color="white">USD 250 ceiling</font>', ParagraphStyle('b3', parent=sBody, fontSize=6, textColor=white, alignment=TA_CENTER)),
        Paragraph('<font color="white">Human-in-the-loop</font>', ParagraphStyle('b4', parent=sBody, fontSize=6, textColor=white, alignment=TA_CENTER)),
        Paragraph('<font color="white">Zero-trust IAM</font>', ParagraphStyle('b5', parent=sBody, fontSize=6, textColor=white, alignment=TA_CENTER)),
    ]
    # Create badge table
    badge_cells = []
    for i, b in enumerate(badges):
        bg = GOLD if i==0 else HexColor("#1F3A6E")
        t = Table([[b]], colWidths=[28*mm if i==0 else 32*mm], rowHeights=[7*mm])
        style = [
            ('BACKGROUND',(0,0),(-1,-1), bg),
            ('ROUNDEDCORNERS',[10,10,10,10]),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('BOX',(0,0),(-1,-1),0.5, GOLD if i==0 else HexColor("#2E4A8A")),
        ]
        if i!=0:
            style.append(('BACKGROUND',(0,0),(-1,-1), HexColor("#1F3A6E")))
            # ensure white text contrast by using brighter bg
        t.setStyle(TableStyle(style))
        badge_cells.append(t)
    # Put badges in a row table
    badge_row = Table([badge_cells], colWidths=[28*mm,32*mm,28*mm,30*mm,28*mm], hAlign='LEFT')
    badge_row.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),2),
        ('RIGHTPADDING',(0,0),(-1,-1),2),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(badge_row)
    story.append(Spacer(1, 6*mm))
    # Two column layout: left meta, right card
    # Left meta
    left_data = [
        [Paragraph('<font color="#93C5FD" size=6><b>ENVIRONMENT</b></font>', sCoverMetaDt), Paragraph('Quantum Integrators internal GCP project • us-east1 / us-central1', sCoverMetaDd)],
        [Paragraph('<font color="#93C5FD" size=6><b>PILOT COORDINATOR</b></font>', sCoverMetaDt), Paragraph('Gupteswar Mishra', sCoverMetaDd)],
        [Paragraph('<font color="#93C5FD" size=6><b>TECHNICAL LEAD</b></font>', sCoverMetaDt), Paragraph('Akshay Saxena', sCoverMetaDd)],
        [Paragraph('<font color="#93C5FD" size=6><b>SPONSORS / APPROVERS</b></font>', sCoverMetaDt), Paragraph('Ken / Prithiviraj — Business & Budget Authority', sCoverMetaDd)],
        [Paragraph('<font color="#93C5FD" size=6><b>DATE & VERSION</b></font>', sCoverMetaDt), Paragraph('16 October 2026 • v2.0 — Tier-1 Enhanced Edition (supersedes v1.0)', sCoverMetaDd)],
        [Paragraph('<font color="#93C5FD" size=6><b>CLASSIFICATION</b></font>', sCoverMetaDt), Paragraph('Confidential — QI Internal • Not for external distribution', sCoverMetaDd)],
    ]
    left_table = Table(left_data, colWidths=[32*mm, 62*mm])
    left_table.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),2),
        ('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,-2),0.3, HexColor("#1E3A8A")),
    ]))
    # Right card
    card_title = Paragraph('<font color="#0B1F4A" size=7><b>DECISION REQUESTED</b></font>', ParagraphStyle('cardT', parent=sBody, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold'))
    card_status = Paragraph('<font color="#059669" size=7><b>● Conditional Approval</b></font>', ParagraphStyle('cardS', parent=sBody, fontSize=7, textColor=GREEN, alignment=TA_RIGHT))
    card_head = Table([[card_title, card_status]], colWidths=[35*mm, 35*mm])
    card_head.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LINEBELOW',(0,0),(-1,-1),0.5, SLATE_200),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    # KV items inside card
    def kv(label, value, sub):
        p1 = Paragraph(f'<font color="#64748B" size=6><b>{label}</b></font>', ParagraphStyle('kvl', parent=sBody, fontSize=6, textColor=SLATE_LIGHT, alignment=TA_LEFT, spaceAfter=1))
        p2 = Paragraph(f'<font color="#0B1F4A" size=9><b>{value}</b></font>', ParagraphStyle('kvv', parent=sBody, fontSize=9, textColor=NAVY, alignment=TA_LEFT, fontName='Helvetica-Bold', spaceAfter=1, leading=10))
        p3 = Paragraph(f'<font color="#475569" size=5>{sub}</font>', ParagraphStyle('kvs', parent=sBody, fontSize=5, textColor=SLATE, alignment=TA_LEFT, leading=7))
        inner = Table([[p1],[p2],[p3]], colWidths=[32*mm])
        inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
        t = Table([[inner]], colWidths=[34*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1), SLATE_50),
            ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
            ('ROUNDEDCORNERS',[4,4,4,4]),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),2),
            ('RIGHTPADDING',(0,0),(-1,-1),2),
            ('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ]))
        return t
    kv1 = kv("ASK", "Approve", "QI-only pilot subject to gates")
    kv2 = kv("BUDGET CEILING", "USD 250", "Pending period validation")
    kv3 = kv("SCOPE", "≤ 20 services", "Start with 2, scale on evidence")
    kv4 = kv("RISK POSTURE", "Guardrailed", "Recommend-only • Approval-bound")
    kv_grid = Table([[kv1, kv2],[kv3, kv4]], colWidths=[35*mm,35*mm])
    kv_grid.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),3),
        ('RIGHTPADDING',(0,0),(-1,-1),3),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    # Footer inside card
    foot_icon = Paragraph('<font size=8>⚑</font>', ParagraphStyle('fi', parent=sBody, alignment=TA_CENTER))
    foot_icon_box = Table([[foot_icon]], colWidths=[7*mm], rowHeights=[7*mm])
    foot_icon_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), HexColor("#FEF3C7")),('ROUNDEDCORNERS',[10,10,10,10])]))
    foot_text = Paragraph('<font color="#92400E" size=6><b>Go / No-Go Rule:</b> Privileged remediation stays <u>disabled</u> until IAM isolation, approval-binding, and all negative bypass tests pass. This pilot does not certify production readiness and does not authorize any GSK implementation.</font>', ParagraphStyle('ft', parent=sBody, fontSize=6, leading=8, textColor=HexColor("#92400E")))
    foot_row = Table([[foot_icon_box, foot_text]], colWidths=[9*mm, 59*mm])
    foot_row.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), AMBER_LIGHT),
        ('BOX',(0,0),(-1,-1),0.5, HexColor("#FDE68A")),
        ('ROUNDEDCORNERS',[4,4,4,4]),
        ('LEFTPADDING',(0,0),(-1,-1),4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    card_content = Table([[card_head],[kv_grid],[foot_row]], colWidths=[72*mm])
    card_content.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), white),
        ('ROUNDEDCORNERS',[8,8,8,8]),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('LEFTPADDING',(0,0),(-1,-1),4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    # Combine left and right
    cover_grid = Table([[left_table, card_content]], colWidths=[96*mm, 74*mm])
    cover_grid.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(cover_grid)
    story.append(Spacer(1, 8*mm))
    # Document control on cover
    doc_ctrl = Paragraph('<font color="#93C5FD" size=6>Document ID: QI-AI-SRE-2026-001  •  Version 2.0 Enhanced  •  Supersedes v1.0 dated 16 Oct 2026  •  Prepared for Business Sponsors Ken / Prithiviraj  •  Page 1 — Cover</font>', ParagraphStyle('dc', parent=sBody, fontSize=6, textColor=HexColor("#93C5FD"), alignment=TA_LEFT))
    story.append(doc_ctrl)

    # After cover, need page break
    story.append(PageBreak())

    # TOC page
    story.append(Paragraph('<font color="#0B1F4A" size=7><b>CONTENTS</b></font>', sKicker))
    story.append(Paragraph('Enhanced Proposal — Tier-1 Edition', ParagraphStyle('tocTitle', parent=sH1, fontSize=16, textColor=NAVY)))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=4))
    story.append(Paragraph('This enhanced edition restructures the original 7-page working draft into a board-ready, audit-defensible pilot charter. Substance preserved; structure, rigor, and assurance elevated to Tier-1 consulting standards.', ParagraphStyle('tocSub', parent=sBody, fontSize=8, textColor=SLATE, spaceAfter=8)))
    toc_data = [
        ["0", "Executive Summary — One-page decision brief", "3"],
        ["1", "Strategic Context — Situation & Imperative", "4"],
        ["2", "Vision, Objectives & Outcomes — What success looks like", "4"],
        ["3", "Scope & Boundaries — In / Out & Stage Gates", "5"],
        ["4", "Target Architecture — Evidence-linked, policy-gated, workflow-executed", "6"],
        ["5", "Security, IAM & Responsible AI — Zero-trust, least-privilege", "7"],
        ["6", "Human Approval & Privileged Execution — Adversarial testing", "8"],
        ["7", "Delivery Plan & Milestones — Stage-gated 4–6 weeks", "9"],
        ["8", "Financial Model & Budget — USD 250 ceiling & unit economics", "10"],
        ["9", "Success Measures & Acceptance — Audited KPIs", "11"],
        ["10", "Risks, Assumptions, Issues & Dependencies — RAID", "12"],
        ["11", "Governance & Operating Model — RACI & Cadence", "13"],
        ["12", "Decisions Requested & Next Steps — What we need this week", "14"],
        ["A", "Appendices — References, schemas, assumptions, scenarios", "15"],
    ]
    toc_rows = []
    for num, title, pg in toc_data:
        num_p = Paragraph(f'<font color="white" size=7><b>{num}</b></font>', ParagraphStyle('tn', parent=sBody, alignment=TA_CENTER, textColor=white, fontSize=7, fontName='Helvetica-Bold'))
        num_box = Table([[num_p]], colWidths=[7*mm], rowHeights=[7*mm])
        bg = NAVY if num!="A" else TEAL
        num_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), bg),('ROUNDEDCORNERS',[4,4,4,4]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER')]))
        title_p = Paragraph(f'<font color="#0B1F4A" size=8><b>{title}</b></font>', ParagraphStyle('tt', parent=sBody, fontSize=8, textColor=NAVY, spaceAfter=0))
        pg_p = Paragraph(f'<font color="#64748B" size=7>{pg}</font>', ParagraphStyle('tp', parent=sBody, alignment=TA_RIGHT, fontSize=7, textColor=SLATE_LIGHT))
        # Dotted line simulation via HR? Just use spacing
        row = [num_box, title_p, pg_p]
        toc_rows.append(row)
    toc_table = Table(toc_rows, colWidths=[10*mm, 142*mm, 10*mm])
    toc_table.setStyle(TableStyle([
        ('LEFTPADDING',(0,0),(-1,-1),3),
        ('RIGHTPADDING',(0,0),(-1,-1),3),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LINEBELOW',(0,0),(-1,-1),0.5, SLATE_100),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 6*mm))
    # Key callout on TOC
    story.append(callout("How to use this document", "<b>Executives:</b> Cover + §0 + §12. &nbsp; <b>Engineering & Security:</b> §4–§6. &nbsp; <b>Finance & Platform:</b> §8. &nbsp; <b>All reviewers:</b> §9–§11. &nbsp; Print-friendly A4; page breaks optimized.", BLUE_LIGHT, HexColor("#BFDBFE"), HexColor("#DBEAFE"), "ℹ"))
    story.append(Spacer(1, 4*mm))
    # At-a-glance box
    glance = [
        [Paragraph('<font color="#0B1F4A" size=7><b>AT A GLANCE</b></font>', ParagraphStyle('g1', parent=sBody, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold', alignment=TA_CENTER)),
         Paragraph('<font color="#0B1F4A" size=7><b>DESIGN AXIOM</b></font>', ParagraphStyle('g2', parent=sBody, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold', alignment=TA_CENTER))],
        [Paragraph('<font color="#0B1F4A" size=16><b>5</b></font><font color="#64748B" size=6> scenarios</font> &nbsp; <font color="#0B1F4A" size=16><b>≥10</b></font><font color="#64748B" size=6> scored runs</font> &nbsp; <font color="#0B1F4A" size=16><b>100%</b></font><font color="#64748B" size=6> approval-bound</font> &nbsp; <font color="#DC2626" size=16><b>0</b></font><font color="#64748B" size=6> autonomous IAM/DB</font>', ParagraphStyle('g3', parent=sBody, fontSize=7, alignment=TA_CENTER)),
         Paragraph('<font color="#334155" size=7>AI proposes → deterministic policy validates → authorized human approves → protected workflow executes → health checks verify → audit records persist.</font>', ParagraphStyle('g4', parent=sBody, fontSize=7, alignment=TA_CENTER, textColor=HexColor("#334155")))],
    ]
    glance_table = Table(glance, colWidths=[82*mm, 82*mm])
    glance_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), SLATE_50),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('GRID',(0,0),(-1,-1),0.5, SLATE_200),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('ROUNDEDCORNERS',[6,6,6,6]),
    ]))
    story.append(glance_table)

    # Confidential bar as text after TOC
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=SLATE_200, spaceAfter=4, spaceBefore=4))
    story.append(Paragraph('<font color="#991B1B" size=6><b>CONFIDENTIAL — QI INTERNAL DEVELOPMENT PILOT — GSK IMPLEMENTATION, DATA, AND CREDENTIALS EXPLICITLY EXCLUDED</b></font>', ParagraphStyle('conf', parent=sBody, alignment=TA_CENTER, fontSize=6, textColor=HexColor("#991B1B"), fontName='Helvetica-Bold')))

    # SECTION 0 - Executive Summary
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('<font color="#0E7490" size=6><b>EXECUTIVE SUMMARY — ONE-PAGE DECISION BRIEF</b></font>', sKicker))
    story.append(Paragraph('0 &nbsp; The ask, the why, and the conditions', ParagraphStyle('s0h', parent=sH1, fontSize=14, textColor=NAVY)))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    # Executive summary card
    es_left = Paragraph(
        '<b>Situation:</b> SRE toil is dominated by alert triage, log correlation, and runbook lookup — slow, inconsistent, and audit-heavy. '
        '<b>Complication:</b> Naïve AI automation risks prompt injection, privilege creep, and unapproved changes. '
        '<b>Question:</b> Can we prove, in a safe QI sandbox, that an AI-assisted copilot <i>accelerates diagnosis</i> without weakening change control?<br/><br/>'
        '<b>Answer (pilot thesis):</b> Yes — <i>if</i> we enforce a hard separation: <b>AI proposes → deterministic policy validates → human approves → protected workflow executes → health checks verify → audit records persist</b>. '
        'The copilot never holds deployment credentials; the deployer never sees raw prompts.', ParagraphStyle('esL', parent=sBody, fontSize=8, leading=11))
    es_right_title = Paragraph('<font color="#0B1F4A" size=7><b>RECOMMENDATION</b></font>', ParagraphStyle('esR1', parent=sBody, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold', alignment=TA_CENTER))
    es_right_body = Paragraph('<font color="#0B1F4A" size=8>Conditionally approve the QI dev pilot. Release privileged remediation <i>only after</i> all negative tests pass.</font>', ParagraphStyle('esR2', parent=sBody, fontSize=8, textColor=NAVY, alignment=TA_CENTER, borderPadding=(6,6,6)))
    es_right_box = Table([[es_right_title],[es_right_body]], colWidths=[42*mm])
    es_right_box.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), SLATE_50),
        ('BACKGROUND',(0,1),(-1,1), white),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('ROUNDEDCORNERS',[6,6,6,6]),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))
    es_table = Table([[es_left, es_right_box]], colWidths=[108*mm, 46*mm])
    es_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), white),
        ('BOX',(0,0),(-1,-1),0.5, NAVY),
        ('LINEBEFORE',(1,0),(1,0),0.5, SLATE_200),
        ('BACKGROUND',(0,0),(0,0), white),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROUNDEDCORNERS',[6,6,6,6]),
    ]))
    story.append(es_table)
    story.append(Spacer(1, 4*mm))
    # Three columns
    col1 = [
        Paragraph('<b>Why now</b>', ParagraphStyle('cT', parent=sBody, fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
        Paragraph('• Grafana CE + Cloud Monitoring mature for bounded evidence<br/>• Vertex AI Gemini gives structured, citation-linked output<br/>• Workload Identity Federation enables short-lived, narrow creds<br/>• Existing GitHub Actions can enforce approval binding today', ParagraphStyle('cB', parent=sBody, fontSize=7, leading=10, textColor=SLATE, spaceAfter=0))
    ]
    col2 = [
        Paragraph('<b>What we will prove in 4–6 weeks</b>', ParagraphStyle('cT2', parent=sBody, fontSize=8, textColor=NAVY, fontName='Helvetica-Bold')),
        Paragraph('• ≥90% correct primary diagnosis across ≥10 scored runs<br/>• Zero changes outside approved workflows<br/>• 100% approval coverage for privileged actions<br/>• Median alert→approved-fix time vs. manual baseline', ParagraphStyle('cB2', parent=sBody, fontSize=7, leading=10, textColor=SLATE, spaceAfter=0))
    ]
    col3 = [
        Paragraph('<b>What we will NOT do</b>', ParagraphStyle('cT3', parent=sBody, fontSize=8, textColor=RED, fontName='Helvetica-Bold')),
        Paragraph('• No GSK env, creds, or data — ever in this pilot<br/>• No autonomous IAM / DB / quota / failover changes<br/>• No execution of arbitrary model-generated commands<br/>• No claim of production certification', ParagraphStyle('cB3', parent=sBody, fontSize=7, leading=10, textColor=SLATE, spaceAfter=0))
    ]
    def col_card(content):
        inner = Table([[c] for c in content], colWidths=[48*mm])
        inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
        outer = Table([[inner]], colWidths=[50*mm])
        outer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),white),('BOX',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6])]))
        return outer
    three_col = Table([[col_card(col1), col_card(col2), col_card(col3)]], colWidths=[52*mm,52*mm,52*mm], hAlign='CENTER')
    three_col.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(three_col)
    story.append(Spacer(1, 4*mm))
    story.append(callout("Value hypothesis (to be measured, not assumed)", "Industry SRE studies show 30–50% of MTTR is spent on correlation & runbook lookup. If the copilot cuts that slice by half, a 20–25% MTTR reduction is plausible on in-scope incidents — <b>without</b> increasing change risk, because every privileged action remains human-approved and audit-recorded. The pilot will quantify this against a manual baseline agreed at kickoff.", BLUE_LIGHT, HexColor("#BFDBFE"), HexColor("#DBEAFE"), "ℹ"))
    story.append(Spacer(1, 4*mm))
    # Conditions table
    cond_data = [
        ["Condition", "Gate & Evidence", "Owner"],
        ["Written scope & budget approval", "Signed decision log confirming USD 250 period (full pilot vs. monthly) + contingency rule", "Ken / Prithiviraj"],
        ["Named owners & approvers", "RACI confirmed; ≥2 authorized approvers in GitHub protected environment", "Gupteswar"],
        ["Access readiness", "GCP project, billing, IAM, GitHub plan/branch protection & WIF trust validated", "Cloud Platform"],
        ["Approval controls verified", "All bypass tests pass (see §6); remediation stays disabled until then", "CI/CD + Security"],
        ["Security review", "Data-handling, redaction, log-as-untrusted-input, retention reviewed", "Security Reviewer"],
    ]
    story.append(styled_table(cond_data, [42*mm, 88*mm, 26*mm]))
    story.append(Spacer(1, 4*mm))
    story.append(callout("Confidentiality & Scope Boundary — Read First", "This pilot is <b>QI-internal only</b>. It does not authorize access to, deployment in, or use of credentials or data from GSK. Any future GSK implementation requires a separate architecture, security, access, budget, and go-live approval package.", AMBER_LIGHT, HexColor("#FDE68A"), HexColor("#FEF3C7"), "⚠"))

    # SECTION 1
    story.append(Paragraph('<font color="#0E7490" size=6><b>1 &nbsp; STRATEGIC CONTEXT</b></font>', sKicker))
    story.append(Paragraph('Situation & Imperative — Why this pilot, why now', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    market_left = Paragraph('<b>Market & technology tailwinds</b><br/><br/>Observability (Cloud Monitoring + Grafana) and LLMs (Vertex AI Gemini) have converged to make <i>evidence-linked diagnosis</i> feasible. Workload Identity Federation removes the need for long-lived keys. Together they allow a <b>recommendation-first</b> copilot that is both useful and controllable — a materially better trade-off than 12 months ago.', ParagraphStyle('mL', parent=sBody, fontSize=8, leading=11))
    market_right = Paragraph('<b>QI-specific opportunity</b><br/><br/>QI runs lean, multi-region Cloud Run estates. SRE load is bursty. A copilot that correlates alerts, pulls bounded evidence, and surfaces runbook-backed next steps — <b>inside QI’s own project</b> — builds reusable IP before any client conversation. This pilot is an <b>internal capability bet</b>, not a client delivery commitment.', ParagraphStyle('mR', parent=sBody, fontSize=8, leading=11))
    market_table = Table([[market_left, market_right]], colWidths=[78*mm,78*mm])
    market_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), white),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('GRID',(0,0),(-1,-1),0.5, SLATE_200),
        ('ROUNDEDCORNERS',[6,6,6,6]),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(market_table)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Guiding Principles — Non-negotiables', sH2))
    principles = [
        ("1", "Human-in-command", "AI recommends; humans decide; workflows execute."),
        ("2", "Least privilege by design", "No identity holds more access than its job requires."),
        ("3", "Untrusted model output", "Every proposal is schema-validated and allowlist-checked."),
        ("4", "Auditability first", "If it isn’t recorded, it didn’t happen."),
        ("5", "Fail safe, fail closed", "Approval unavailable → remediation disabled."),
        ("6", "Progressive exposure", "2 services → measure → then scale to ≤20."),
    ]
    p_cards = []
    for num, title, desc in principles:
        num_p = Paragraph(f'<font color="white" size=7><b>{num}</b></font>', ParagraphStyle('pn', parent=sBody, alignment=TA_CENTER, textColor=white))
        num_box = Table([[num_p]], colWidths=[7*mm], rowHeights=[7*mm])
        num_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), NAVY),('ROUNDEDCORNERS',[4,4,4,4]),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
        title_p = Paragraph(f'<font color="#0B1F4A" size=7><b>{title}</b></font>', ParagraphStyle('pt', parent=sBody, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold', spaceAfter=1))
        desc_p = Paragraph(f'<font color="#475569" size=7>{desc}</font>', ParagraphStyle('pd', parent=sBody, fontSize=7, textColor=SLATE))
        inner = Table([[title_p],[desc_p]], colWidths=[40*mm])
        inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        outer = Table([[num_box, inner]], colWidths=[9*mm, 42*mm])
        outer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), SLATE_50),('BOX',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
        p_cards.append(outer)
    # Grid 3x2
    p_grid = Table([[p_cards[0], p_cards[1], p_cards[2]],[p_cards[3], p_cards[4], p_cards[5]]], colWidths=[53*mm,53*mm,53*mm])
    p_grid.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(p_grid)

    # SECTION 2
    story.append(Paragraph('<font color="#0E7490" size=6><b>2 &nbsp; VISION, OBJECTIVES & OUTCOMES</b></font>', sKicker))
    story.append(Paragraph('What success looks like', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    obj_data = [
        ["#", "Objective (Outcome)", "Key Result (Measurable)", "Evidence"],
        ["O1", "Detect representative incidents early", "Grafana alerts + SLOs firing on all 5 scenarios within SLO window", "Dashboard + alert history"],
        ["O2", "Correlate & collect bounded evidence", "Per incident: alert graph, log slice, deploy metadata & runbook link", "Incident evidence bundle"],
        ["O3", "Generate evidence-linked diagnosis", "≥90% correct primary diagnosis across ≥10 scored runs (see §9)", "Scored test log"],
        ["O4", "Route via approved CI/CD only", "Zero infra changes outside protected GitHub workflows", "Workflow audit trail"],
        ["O5", "Enforce human approval", "100% of privileged remediations have pre-execution approval", "Approval record"],
        ["O6", "Prove auditability & time value", "Full trace (evidence→recommendation→decision→outcome) + median alert-to-fix vs. baseline", "Audit log + timing report"],
    ]
    story.append(styled_table(obj_data, [12*mm, 46*mm, 62*mm, 36*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(callout("Definition of Done for the pilot", "A pilot is <b>done</b> when all five scenarios have been exercised, at least ten runs are scored and traceable, all approval-bypass negative tests pass, spend is reconciled, and a <b>Proceed / Extend with Conditions / Stop</b> recommendation is presented at the Week-6 review. Demo is live, not slideware.", GREEN_LIGHT, HexColor("#A7F3D0"), HexColor("#D1FAE5"), "✓"))

    # SECTION 3
    story.append(Paragraph('<font color="#0E7490" size=6><b>3 &nbsp; SCOPE & BOUNDARIES</b></font>', sKicker))
    story.append(Paragraph('In scope, out of scope, and stage gates', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    in_scope = Paragraph(
        '<b><font color="#059669">✓ In Scope</font></b><br/>'
        '• Up to 10–20 lightweight Cloud Run services across <i>us-east1</i> & <i>us-central1</i> (start with 2, scale on cost signal)<br/>'
        '• Grafana Community Edition dashboards, alerts & representative SLOs<br/>'
        '• Authenticated incident intake, deduplication & correlation<br/>'
        '• Bounded AI diagnosis with Vertex AI Gemini + approved runbooks (synthetic / QI-approved data only)<br/>'
        '• Predefined CI/CD allowlist actions with mandatory approval & health checks<br/>'
        '• <b>Five controlled fault scenarios:</b> bad deployment, crash loop / startup failure, quota exhaustion, disabled API, configuration drift<br/>'
        '• ≥10 scored runs + negative tests (approval rejection, duplicate delivery, invalid model output, workflow failure)', ParagraphStyle('ins', parent=sBody, fontSize=7.5, leading=10))
    out_scope = Paragraph(
        '<b><font color="#DC2626">✕ Out of Scope — Explicitly Excluded</font></b><br/>'
        '• Any GSK environment access, credential use, data processing, or deployment<br/>'
        '• Autonomous infra changes or direct execution of arbitrary AI-generated commands<br/>'
        '• Automated IAM changes, database operations, regional failover, quota increases<br/>'
        '• Production rollout, production-readiness certification, or implied GSK authorization<br/>'
        '• New paid GitHub / SaaS subscriptions unless separately approved<br/>'
        '• Broad Data Access audit logging before cost validation', ParagraphStyle('outs', parent=sBody, fontSize=7.5, leading=10))
    scope_table = Table([[in_scope, out_scope]], colWidths=[80*mm, 76*mm])
    scope_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0), GREEN_LIGHT),
        ('BACKGROUND',(1,0),(1,0), RED_LIGHT),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('GRID',(0,0),(-1,-1),0.5, SLATE_200),
        ('ROUNDEDCORNERS',[6,6,6,6]),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(scope_table)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Allow-listed Actions Only (pilot)', ParagraphStyle('allow', parent=sH3, fontSize=7, textColor=SLATE)))
    allow_tags = Paragraph(
        '<font color="#059669" size=6><b>✓ Rollback to previous revision</b></font> &nbsp; '
        '<font color="#059669" size=6><b>✓ Redeploy approved revision</b></font> &nbsp; '
        '<font color="#059669" size=6><b>✓ Restart / scale within bounds</b></font> &nbsp; '
        '<font color="#059669" size=6><b>✓ Toggle feature flag (pre-approved)</b></font><br/>'
        '<font color="#DC2626" size=6><b>✕ IAM changes</b></font> &nbsp; '
        '<font color="#DC2626" size=6><b>✕ DB writes / migrations</b></font> &nbsp; '
        '<font color="#DC2626" size=6><b>✕ Quota increase</b></font> &nbsp; '
        '<font color="#DC2626" size=6><b>✕ Regional failover</b></font> &nbsp; '
        '<font color="#DC2626" size=6><b>✕ Arbitrary shell/commands</b></font>', ParagraphStyle('allowTags', parent=sBody, fontSize=7, leading=10, alignment=TA_LEFT, borderPadding=(6,6,6), backColor=SLATE_50))
    # Wrap allow_tags in a box
    allow_box = Table([[allow_tags]], colWidths=[156*mm])
    allow_box.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('BACKGROUND',(0,0),(-1,-1), SLATE_50)]))
    story.append(allow_box)

    # SECTION 4
    story.append(Paragraph('<font color="#0E7490" size=6><b>4 &nbsp; TARGET ARCHITECTURE</b></font>', sKicker))
    story.append(Paragraph('Evidence-linked, policy-gated, workflow-executed', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    story.append(Paragraph('<b>Design axiom:</b> <i>AI proposes; deterministic policy validates; authorized human approves; protected workflow executes; automated checks and audit records verify the outcome.</i> No step can be bypassed; each has a distinct identity and minimal scope.', ParagraphStyle('axiom', parent=sBody, fontSize=8, leading=11, textColor=HexColor("#334155"), borderPadding=(6,6,6), backColor=BLUE_LIGHT)))
    story.append(Spacer(1, 3*mm))
    # Architecture diagram as table with arrows
    arch_headers = [
        Paragraph('<font color="#0B1F4A" size=6><b>TELEMETRY</b></font><br/><font color="#475569" size=5>Monitoring, Logging, Grafana</font><br/><font color="#0E7490" size=5>Read-only</font>', ParagraphStyle('ah', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
        Paragraph('<font color="#0B1F4A" size=6><b>INTAKE</b></font><br/><font color="#475569" size=5>Authn, validate, dedupe</font><br/><font color="#0E7490" size=5>No privilege</font>', ParagraphStyle('ah2', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
        Paragraph('<font color="#0B1F4A" size=6><b>AI DIAGNOSIS</b></font><br/><font color="#475569" size=5>Vertex AI + runbooks</font><br/><font color="#0E7490" size=5>Read-only identity</font>', ParagraphStyle('ah3', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
        Paragraph('<font color="#0B1F4A" size=6><b>POLICY</b></font><br/><font color="#475569" size=5>Allowlist, schema, idemp.</font><br/><font color="#0E7490" size=5>Reject unknown</font>', ParagraphStyle('ah4', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
        Paragraph('<font color="#0B1F4A" size=6><b>APPROVAL</b></font><br/><font color="#475569" size=5>Protected env • Bound</font><br/><font color="#0E7490" size=5>Human decision</font>', ParagraphStyle('ah5', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
        Paragraph('<font color="#0B1F4A" size=6><b>EXECUTION</b></font><br/><font color="#475569" size=5>GitHub Actions</font><br/><font color="#0E7490" size=5>Short-lived creds</font>', ParagraphStyle('ah6', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
        Paragraph('<font color="#0B1F4A" size=6><b>AUDIT</b></font><br/><font color="#475569" size=5>Health checks + ledger</font><br/><font color="#0E7490" size=5>Traceable</font>', ParagraphStyle('ah7', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8)),
    ]
    # Create arrow row
    arrow = Paragraph('<font color="#0B1F4A" size=8><b>→</b></font>', ParagraphStyle('arr', parent=sBody, alignment=TA_CENTER, fontSize=8, textColor=NAVY))
    # Build arch table with 13 columns (7 boxes + 6 arrows)
    arch_cells = []
    for i, h in enumerate(arch_headers):
        box = Table([[h]], colWidths=[19*mm], rowHeights=[16*mm])
        box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), white),('BOX',(0,0),(-1,-1),0.7, NAVY),('ROUNDEDCORNERS',[4,4,4,4]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3)]))
        arch_cells.append(box)
        if i < 6:
            arch_cells.append(arrow)
    col_ws = []
    for i in range(13):
        if i % 2 == 0:
            col_ws.append(19*mm)
        else:
            col_ws.append(5*mm)
    arch_table = Table([arch_cells], colWidths=col_ws, hAlign='CENTER')
    arch_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),1),('RIGHTPADDING',(0,0),(-1,-1),1)]))
    arch_box = Table([[arch_table]], colWidths=[162*mm])
    arch_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), SLATE_50),('BOX',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[8,8,8,8]),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]))
    story.append(arch_box)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('<font color="#64748B" size=6>QI boundary • Privileged creds never available to AI job; only to protected execution job post-approval • Telemetry treated as untrusted input</font>', ParagraphStyle('archCap', parent=sCaption, fontSize=6, textColor=SLATE_LIGHT)))
    story.append(Spacer(1, 3*mm))
    arch_detail = [
        ["Layer", "Responsibilities", "Security Boundary", "Failure Mode → Behavior"],
        ["Telemetry", "Metrics, logs, audit logs, Grafana dashboards & SLOs", "Read-only; approved sources only", "Source down → alert on intake health"],
        ["Incident Intake", "Authn, payload validation, dedupe, correlation", "No privileged execution perms", "Invalid payload → reject, no incident"],
        ["AI Diagnosis", "Bounded evidence + runbooks → Vertex AI → structured proposal", "Read-only identity; no infra write", "Malformed output → schema reject"],
        ["Policy Validation", "Allowlist, param bounds, scope, idempotency", "Model output = untrusted input", "Unknown action → reject"],
        ["Approval", "Present exact proposal to authorized reviewers", "Bound to incident+proposal hash", "Stale/changed → approval invalidated"],
        ["Execution", "Invoke predefined protected workflow", "Short-lived, narrow IAM", "Duplicate dispatch → idempotency blocks"],
        ["Validation & Audit", "Health checks; full ledger (evidence→outcome)", "Immutable record; retention-limited", "Inconclusive → escalate"],
    ]
    story.append(styled_table(arch_detail, [24*mm, 52*mm, 40*mm, 40*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    tech_left = Paragraph('<b>Technology Stack (pilot)</b><br/>• Compute: Cloud Run (scale-to-zero)<br/>• Observability: Cloud Monitoring, Logging, Audit Logs, Grafana CE<br/>• AI: Vertex AI — Gemini (structured, token-bounded, runbook-augmented)<br/>• CI/CD: GitHub Actions + Protected Environments<br/>• Identity: Workload Identity Federation (short-lived), Artifact Registry', ParagraphStyle('tl', parent=sBody, fontSize=7, leading=10))
    tech_right = Paragraph('<b>Data & Evidence Bounds</b><br/>• Per-incident token & log-volume budgets; strict truncation & redaction<br/>• Secrets / PII redacted <i>before</i> model invocation<br/>• Only synthetic or QI-approved data — no production PII<br/>• Logs & runbooks treated as untrusted — prompt-injection hardened<br/>• Request limits, timeouts, schema validation, safe fallback', ParagraphStyle('tr', parent=sBody, fontSize=7, leading=10))
    tech_table = Table([[tech_left, tech_right]], colWidths=[78*mm,78*mm])
    tech_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(tech_table)

    # SECTION 5
    story.append(Paragraph('<font color="#0E7490" size=6><b>5 &nbsp; SECURITY, IAM & RESPONSIBLE AI</b></font>', sKicker))
    story.append(Paragraph('Zero-trust, least-privilege, audit-first', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    story.append(callout("Security thesis", "Usefulness without trust expansion. The AI is the <i>least privileged</i> actor in the system. Privilege is concentrated in a single, audited, approval-gated workflow — and is unavailable everywhere else.", BLUE_LIGHT, HexColor("#BFDBFE"), HexColor("#DBEAFE"), "⬢"))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Identity Separation — Minimum Necessary Access', sH2))
    iam_data = [
        ["Identity", "Can Do (Allow)", "Cannot Do (Deny) — Enforced", "Test"],
        ["Telemetry Collector", "Read approved metrics, logs, service metadata", "No deployment, no IAM writes, no secret access", "Negative IAM probe"],
        ["AI Diagnosis Service", "Invoke Vertex AI; read selected evidence & runbooks", "No infra modification, no workflow execution", "Negative IAM probe"],
        ["Incident Intake", "Authenticate, validate, record incident events", "No privileged GCP access", "Authn bypass test"],
        ["Workflow Dispatcher", "Invoke <i>only</i> the approved workflow via WIF", "No broad admin roles; no direct mutation", "Scope test"],
        ["Remediation Executor", "Approved action on designated QI resources only", "No Owner/Editor; no GSK; no cross-project", "Negative IAM + scope"],
        ["Human Approver", "Approve/reject via protected environment", "No implicit authority from model output", "Bypass test"],
    ]
    story.append(styled_table(iam_data, [28*mm, 52*mm, 52*mm, 24*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Mandatory Security Controls — Checklist (preflight)', sH2))
    sec1 = Paragraph('<b>Identity & Access</b><br/>• WIF with short-lived creds; <b>no long-lived SA keys</b><br/>• Federation trust restricted to QI org / repo / branch / env / workflow<br/>• Narrow roles + SA impersonation only where required<br/>• Privileged creds only in protected job post-approval', ParagraphStyle('sec1', parent=sBody, fontSize=7, leading=10))
    sec2 = Paragraph('<b>Data & AI Safety</b><br/>• Redact secrets <i>before</i> model call; synthetic / QI-approved data only<br/>• Treat logs & runbooks as <b>untrusted input</b><br/>• No prompt content can alter policy or invoke tools<br/>• Token budgets, timeouts, schema validation, safe failure', ParagraphStyle('sec2', parent=sBody, fontSize=7, leading=10))
    sec3 = Paragraph('<b>Platform Hardening</b><br/>• Grafana + intake: authn/authz, restricted network, rate limits<br/>• Audit logging enabled (cost-assessed); retention limits<br/>• Artifact & secret storage scoped to executor only<br/>• Branch + environment protection on GitHub', ParagraphStyle('sec3', parent=sBody, fontSize=7, leading=10))
    sec4 = Paragraph('<b>Cost & Abuse Controls</b><br/>• Request limits, concurrency caps, token budgets<br/>• Budget alerts at 50/75/90/100% — <i>notify</i>, not hard caps<br/>• Daily spend review during fault-testing<br/>• Idempotency + deduplication', ParagraphStyle('sec4', parent=sBody, fontSize=7, leading=10))
    sec_grid = Table([[sec1, sec2],[sec3, sec4]], colWidths=[78*mm,78*mm])
    sec_grid.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(sec_grid)
    story.append(Spacer(1, 3*mm))
    story.append(callout("Responsible AI guardrails", "Every recommendation must include: <b>evidence citations, confidence, risk, validation result, and rollback plan</b>. Low-confidence or uncited proposals are auto-rejected by policy. Human reviewers are shown the <i>exact</i> bounded evidence the model saw — no hidden context.", AMBER_LIGHT, HexColor("#FDE68A"), HexColor("#FEF3C7"), "⚠"))

    # SECTION 6
    story.append(Paragraph('<font color="#0E7490" size=6><b>6 &nbsp; HUMAN APPROVAL & PRIVILEGED EXECUTION</b></font>', sKicker))
    story.append(Paragraph('Approval-bound by design, tested by adversarial cases', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    # 7-step flow as boxes
    flow_steps = [
        "1 • Propose<br/><font size=6>Incident ID, target, action, revision, evidence, risk & rollback</font>",
        "2 • Validate<br/><font size=6>Deterministic allowlist: schema, scope, params</font>",
        "3 • Protect<br/><font size=6>Protected env: required reviewers + branch restrictions</font>",
        "4 • Bind<br/><font size=6>Approval bound to hash; change → re-approval</font>",
        "5 • Isolate<br/><font size=6>Privileged creds only to protected job</font>",
        "6 • Dedupe<br/><font size=6>Idempotency keys + concurrency</font>",
        "7 • Verify<br/><font size=6>Health checks; record outcome; escalate on fail</font>",
    ]
    flow_cells = []
    for fs in flow_steps:
        p = Paragraph(f'<font color="#0B1F4A" size=6>{fs}</font>', ParagraphStyle('fs', parent=sBody, alignment=TA_CENTER, fontSize=6, leading=8, textColor=NAVY))
        box = Table([[p]], colWidths=[20*mm], rowHeights=[14*mm])
        box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), white),('BOX',(0,0),(-1,-1),0.5, NAVY),('ROUNDEDCORNERS',[4,4,4,4]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3)]))
        flow_cells.append(box)
    # interleave arrows - for simplicity just show boxes in one row truncated; we will show as 7 boxes in a row with small gaps
    flow_row = Table([flow_cells], colWidths=[22*mm]*7, hAlign='CENTER')
    flow_row.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    flow_box = Table([[flow_row]], colWidths=[162*mm])
    flow_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), SLATE_50),('BOX',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[8,8,8,8]),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(flow_box)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Approval Bypass — Adversarial Test Matrix (must all pass before remediation is enabled)', sH2))
    bypass_data = [
        ["Adversarial Test", "Expected Result", "Evidence", "Gate"],
        ["No approval / rejected approval → dispatch", "No infra change", "Workflow logs + resource state", "Blocking"],
        ["Expired / cancelled approval → replay", "No infra change", "Approval validity check", "Blocking"],
        ["Proposal mutated post-approval", "Approval invalidated — re-approval required", "Hash comparison", "Blocking"],
        ["Duplicate incident / repeated dispatch", "No duplicate remediation", "Idempotency + concurrency log", "Blocking"],
        ["Unauthorized branch / actor → invoke", "Cannot obtain privileged creds", "WIF trust + branch protection", "Blocking"],
        ["Workflow rerun with stale approval", "Fresh validity checks required", "Rerun audit", "Blocking"],
        ["Approval controls unavailable", "Remediation remains disabled", "Fail-closed log", "Blocking"],
        ["Model proposes allowlist violation", "Rejected by policy — no approval surface", "Policy validation log", "Blocking"],
    ]
    story.append(styled_table(bypass_data, [48*mm, 52*mm, 36*mm, 20*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    story.append(callout("Go / No-Go Rule — Non-negotiable", "Privileged remediation remains <b>disabled</b> until every applicable bypass test demonstrates enforcement. The pilot coordinator + security reviewer must jointly sign the gate. No exceptions, no “temporarily allow”.", RED_LIGHT, HexColor("#FECACA"), HexColor("#FEE2E2"), "⛔"))
    story.append(Spacer(1, 3*mm))
    rollback_left = Paragraph('<b>Rollback discipline</b><br/>Post-action health checks run automatically. <b>Failed or inconclusive recovery is escalated</b>; rollback follows a <i>separately authorized</i> path — never an auto-rollback triggered by model output. Rollback proposals are themselves subject to approval binding.', ParagraphStyle('rbL', parent=sBody, fontSize=7, leading=10))
    rollback_right = Paragraph('<b>GitHub protections (to be confirmed at readiness gate)</b><br/>Protected environment with <b>required reviewers</b>, branch restrictions, and environment-scoped secrets. Verify QI repo plan supports required protections; if not, document limitation and alternate compensating control before Week-1.', ParagraphStyle('rbR', parent=sBody, fontSize=7, leading=10))
    rb_table = Table([[rollback_left, rollback_right]], colWidths=[78*mm,78*mm])
    rb_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(rb_table)

    # SECTION 7
    story.append(Paragraph('<font color="#0E7490" size=6><b>7 &nbsp; DELIVERY PLAN & MILESTONES</b></font>', sKicker))
    story.append(Paragraph('Stage-gated, 4–6 weeks, exit criteria at every gate', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    phases = [
        ("Phase 0 — Approval & Readiness", "Before Week 1 • Gate 0", "Confirm scope, budget period, named owners, access, GitHub plan, approvers, and data-handling. Complete preflight IAM + quota + WIF checks. <b>No provisioning before Gate 0.</b>", "Decision log signed • RACI confirmed • Security review scheduled<br/>Preflight: GCP project, billing, IAM, quotas, WIF, branch protection validated", "Exit Gate 0: All readiness checks green; otherwise timeline does not start.", NAVY),
        ("Phase 1 — Foundation & Security", "Week 1", "Configure billing, APIs, IAM, federation, audit, budget alerts, and <b>two representative Cloud Run services</b>. Prove AI identity is non-privileged via negative IAM tests.", "Budget alerts at 50/75/90/100% live • Audit logging cost-assessed<br/>Negative IAM test evidence: AI identity cannot deploy", "Exit Gate 1: IAM isolation demonstrated; cost alerts firing in test.", TEAL),
        ("Phase 2 — Monitoring & Intake", "Week 2", "Deploy restricted Grafana CE, dashboards, SLOs, authenticated alert delivery, deduplication, and incident evidence schema.", "Grafana authn/authz + network restriction + rate limits<br/>Evidence schema: alert snapshot + log slice + deploy metadata + runbook ref", "Exit Gate 2: Alert → incident → evidence bundle traceable end-to-end.", GOLD),
        ("Phase 3 — AI Diagnosis", "Week 3", "Integrate Vertex AI Gemini with bounded evidence, approved runbooks, schema validation, redaction, action allowlist, and safe failure handling.", "Structured output: diagnosis, citations, confidence, risk, rollback plan<br/>Invalid / low-confidence output → policy reject", "Exit Gate 3: ≥5 dry-run diagnoses scored; policy correctly rejects violations.", NAVY),
        ("Phase 4 — CI/CD & Approval", "Week 4", "Integrate protected GitHub workflows, approval binding, expiry/rejection paths, idempotency, post-action health checks, and audit trail.", "Approval bound to proposal hash; mutation → re-approval<br/>Privileged creds only in protected job; bypass tests executed", "Exit Gate 4: All 8 bypass tests pass; remediation enabled only now.", TEAL),
        ("Phase 5 — Scenario Evaluation", "Week 5", "Run five fault scenarios and <b>at least 10 scored runs</b>; test negative paths, approval bypass, duplicate delivery, invalid model output, and service/workflow failures. Label live vs. simulated evidence.", "5 scenarios: bad deploy, crash loop, quota exhaustion, disabled API, config drift<br/>Every run links evidence → recommendation → decision → execution → outcome", "Exit Gate 5: Scorecard complete; §9 acceptance criteria assessed.", GOLD),
        ("Phase 6 — Review & Clean-up", "Week 6 or earlier", "Review results, spend, limitations, and risks. Live demo. Remove test resources and revoke temporary access unless retention is formally approved. Present <b>Proceed / Extend with Conditions / Stop</b> recommendation.", "Spend reconciliation • Limitations register • Risk burn-down<br/>Clean-up attestation or retention justification signed", "Exit Gate 6: Final review signed; clean-up verified; GSK-separation attestation filed.", NAVY),
    ]
    for title, timing, desc, bullets, gate, col in phases:
        # Title bar
        t_p = Paragraph(f'<font color="white" size=7><b>{title}</b></font> &nbsp; <font color="#DBEAFE" size=6>{timing}</font>', ParagraphStyle('phaseT', parent=sBody, textColor=white, fontSize=7, leading=10))
        t_box = Table([[t_p]], colWidths=[156*mm], rowHeights=[7*mm])
        t_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), col),('ROUNDEDCORNERS',[4,4,4,4]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
        story.append(t_box)
        story.append(Spacer(1, 2*mm))
        desc_p = Paragraph(f'<font size=7>{desc}</font>', ParagraphStyle('phaseD', parent=sBody, fontSize=7, leading=10, textColor=HexColor("#334155")))
        bullet_p = Paragraph(f'<font size=7>{bullets}</font>', ParagraphStyle('phaseB', parent=sBody, fontSize=7, leading=10, textColor=SLATE))
        gate_p = Paragraph(f'<font color="#065F46" size=7><b>✓ {gate}</b></font>', ParagraphStyle('phaseG', parent=sBody, fontSize=7, textColor=GREEN, backColor=GREEN_LIGHT, borderPadding=(4,4,4)))
        inner = Table([[desc_p],[bullet_p],[gate_p]], colWidths=[150*mm])
        inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),('VALIGN',(0,0),(-1,-1),'TOP')]))
        outer = Table([[inner]], colWidths=[156*mm])
        outer.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('BACKGROUND',(0,0),(-1,-1), white),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(outer)
        story.append(Spacer(1, 3*mm))
    story.append(callout("Schedule discipline", "Timeline starts <i>only after</i> Gate 0. If Gate 0 is not green, Week-1 does not start. Each phase has a single exit gate; a red gate stops downstream work. Daily stand-ups during fault-testing; weekly steering with sponsors.", BLUE_LIGHT, HexColor("#BFDBFE"), HexColor("#DBEAFE"), "ℹ"))

    # SECTION 8
    story.append(Paragraph('<font color="#0E7490" size=6><b>8 &nbsp; FINANCIAL MODEL & BUDGET</b></font>', sKicker))
    story.append(Paragraph('USD 250 ceiling — unit economics, not just a total', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    story.append(callout("Budget period — Decision required before spend", "The table below is a <b>planning estimate, not a validated quotation</b>. Approval is <i>conditional</i> on confirming whether <b>USD 250 covers the entire 4–6 week pilot or a single monthly period</b>. Engineering effort is excluded; no new paid GitHub/software subscription is included; taxes, FX, and data-transfer must be checked.", AMBER_LIGHT, HexColor("#FDE68A"), HexColor("#FEF3C7"), "⚠"))
    story.append(Spacer(1, 3*mm))
    budget_data = [
        ["Cost Category", "Allocation", "Share", "Key Drivers & Validation Needed", "Owner"],
        ["Cloud Run — services & copilot runtime", "USD 45", "18%", "Service count (2→20), requests, vCPU/memory, scale-to-zero, regions (2)", "Platform"],
        ["Grafana hosting & storage", "USD 40", "16%", "Host size, uptime, disk, retention; CE license is free but hosting is not", "Platform"],
        ["Vertex AI — Gemini usage", "USD 55", "22%", "Model, region, token volume (input+output), retries, runbook augmentation", "Tech Lead"],
        ["Logging, monitoring & audit storage", "USD 30", "12%", "Log volume, audit categories enabled, retention; Data Access logs costed separately", "Platform"],
        ["Artifact storage, secrets & networking", "USD 20", "8%", "Container registry, Secret Manager, egress; keep synthetic data small", "Platform"],
        ["Contingency (coordinator-gated)", "USD 60", "24%", "Reserved for variance; use requires pilot coordinator review & log entry", "Gupteswar"],
        ["TOTAL CEILING", "USD 250", "100%", "Subject to confirmation & pricing validation before Gate 0", ""],
    ]
    # Custom widths
    story.append(styled_table(budget_data, [42*mm, 18*mm, 12*mm, 64*mm, 20*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    # Budget bar visual as table
    bar_data = [
        [Paragraph('<font size=5> </font>', sBody)]*6
    ]
    bar_colors = [NAVY, NAVY3, TEAL, SLATE, HexColor("#94A3B8"), GOLD]
    bar_widths = [28*mm, 25*mm, 34*mm, 19*mm, 13*mm, 37*mm]
    bar_cells = []
    for i, c in enumerate(bar_colors):
        t = Table([[Paragraph('', sBody)]], colWidths=[bar_widths[i]], rowHeights=[4*mm])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), c),('ROUNDEDCORNERS',[2,2,2,2])]))
        bar_cells.append(t)
    bar_row = Table([bar_cells], colWidths=bar_widths, hAlign='LEFT')
    bar_row.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),1),('RIGHTPADDING',(0,0),(-1,-1),1)]))
    story.append(bar_row)
    legend_text = Paragraph('<font color="#475569" size=6><b><font color="#0B1F4A">■</font> Cloud Run 18%</b> &nbsp; <b><font color="#1E3A8A">■</font> Grafana 16%</b> &nbsp; <b><font color="#0E7490">■</font> Vertex AI 22%</b> &nbsp; <b><font color="#475569">■</font> Logs 12%</b> &nbsp; <b><font color="#94A3B8">■</font> Artifacts 8%</b> &nbsp; <b><font color="#C5A880">■</font> Contingency 24%</b></font>', ParagraphStyle('legend', parent=sBody, alignment=TA_CENTER, fontSize=6, textColor=SLATE))
    story.append(legend_text)
    story.append(Spacer(1, 4*mm))
    # Three cards for spend controls etc.
    spend1 = Paragraph('<b>Spend controls</b><br/>• Start with 2 services; expand only after measuring unit cost<br/>• Daily spend review during fault testing; pause nonessential at 90%<br/>• Budget alerts at 50/75/90/100% are <i>notify</i> — test operational stop separately<br/>• Contingency draw requires coordinator entry + reason', ParagraphStyle('sp1', parent=sBody, fontSize=7, leading=10))
    spend2 = Paragraph('<b>What’s excluded</b><br/>• Engineering effort (QI staff time)<br/>• New paid GitHub / SaaS subscriptions<br/>• Taxes, currency conversion, material data-transfer<br/>• Broad Data Access audit logging (validate cost before enabling)', ParagraphStyle('sp2', parent=sBody, fontSize=7, leading=10))
    spend3 = Paragraph('<b>Sensitivity — What moves the needle</b><br/>• <b>Vertex AI tokens:</b> ±40% if evidence bounds loosen<br/>• <b>Grafana uptime:</b> 24/7 vs. test-window-only = ~2×<br/>• <b>Log retention:</b> 7d vs. 30d = +30–50%<br/>• <b>Service count:</b> 20 ≠ 10× if scale-to-zero holds — but verify', ParagraphStyle('sp3', parent=sBody, fontSize=7, leading=10))
    spend_table = Table([[spend1, spend2, spend3]], colWidths=[52*mm,52*mm,52*mm])
    spend_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(spend_table)

    # SECTION 9
    story.append(Paragraph('<font color="#0E7490" size=6><b>9 &nbsp; SUCCESS MEASURES & ACCEPTANCE</b></font>', sKicker))
    story.append(Paragraph('From diagnostic accuracy to time-to-fix — all audited', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    success_data = [
        ["Measure", "Acceptance Criterion (pilot)", "How Measured", "Type"],
        ["Diagnostic accuracy", "≥90% correct primary diagnosis across ≥10 scored runs", "Independent scoring vs. ground truth", "Go/No-Go"],
        ["Scenario coverage", "All 5 scenarios exercised", "Evidence bundle per scenario", "Go/No-Go"],
        ["Pipeline enforcement", "Zero infra changes outside approved workflows", "Workflow audit vs. resource log", "Zero-tol"],
        ["Human approval", "100% of privileged remediations have pre-execution approval", "Approval → execution correlation", "Zero-tol"],
        ["Restricted actions", "Zero automated IAM / DB / failover / quota actions", "Policy log + IAM audit", "Zero-tol"],
        ["Auditability", "Every run links evidence → recommendation → decision → outcome", "Trace completeness check", "Go/No-Go"],
        ["Duplicate protection", "Repeated delivery of same incident → no duplicate remediation", "Idempotency test", "Go/No-Go"],
        ["Time improvement", "Median alert→approved-fix vs. manual baseline; target at kickoff", "Timed runs; manual baseline Week 1", "Directional"],
        ["Budget", "Spend within confirmed approved envelope", "Daily cost report + reconciliation", "Envelope"],
        ["Isolation", "No GSK resources, creds, or data used", "IAM + project scope attestation", "Zero-tol"],
    ]
    story.append(styled_table(success_data, [28*mm, 58*mm, 46*mm, 24*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    story.append(callout("Measurement caveat — Read with rigor", "Ten runs provide an <b>initial pilot signal, not statistical evidence</b> of production reliability. The 90% threshold must be assessed <i>alongside</i> scenario coverage, failure evidence, and reviewer notes — not as a standalone pass/fail. A strong score with weak coverage is not a green light.", AMBER_LIGHT, HexColor("#FDE68A"), HexColor("#FEF3C7"), "⚠"))
    story.append(Spacer(1, 3*mm))
    lead = Paragraph('<b>Leading indicators (weekly)</b><br/>• Evidence completeness per incident (target: 100%)<br/>• Policy reject rate & reasons (expect 10–20% on adversarial)<br/>• Approval latency (p50 / p95)<br/>• Idempotency block rate on duplicate injects', ParagraphStyle('lead', parent=sBody, fontSize=7, leading=10))
    lag = Paragraph('<b>Lagging indicators (end of pilot)</b><br/>• Scored diagnostic accuracy + inter-rater agreement<br/>• Median alert→approved-fix delta vs. manual<br/>• Zero-tolerance violations: count (must be 0)<br/>• Spend vs. envelope; contingency draw reasons', ParagraphStyle('lag', parent=sBody, fontSize=7, leading=10))
    ll_table = Table([[lead, lag]], colWidths=[78*mm,78*mm])
    ll_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(ll_table)

    # SECTION 10
    story.append(Paragraph('<font color="#0E7490" size=6><b>10 &nbsp; RISKS, ASSUMPTIONS, ISSUES & DEPENDENCIES</b></font>', sKicker))
    story.append(Paragraph('RAID — what could derail us and what we’ll do', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    risks = [
        ("1 • Incorrect AI recommendation → wrong remediation proposed", "High — could mislead approver. Likelihood: Medium.", "High", "Med", "Tech Lead", "Evidence citations + confidence + approved runbooks required; deterministic allowlist rejects unsupported actions; human approval mandatory; post-action health checks verify outcome."),
        ("2 • Approval bypass — privileged change without valid approval", "High — breaks trust model. Likelihood: Low if controls hold.", "High", "Low", "CI/CD + Security", "Separate identities, protected environment, proposal-hash binding, 8 adversarial bypass tests (blocking gate). Fail-closed on control unavailability."),
        ("3 • Sensitive data exposure via logs / prompts", "High — compliance. Likelihood: Medium.", "High", "Med", "Security", "Synthetic / QI-approved data only; redaction before model call; least privilege; security review at Gate 0 and Gate 4."),
        ("4 • Prompt injection via telemetry (logs as attack vector)", "Medium. Likelihood: Medium.", "Med", "Med", "Tech Lead", "Treat all telemetry as untrusted; never let prompt content alter policy or invoke tools; schema validation + allowlist as hard boundary."),
        ("5 • Cost overrun (token / log / uptime variance)", "Medium. Likelihood: Medium.", "Med", "Med", "Platform / Coordinator", "Progressive scale (2 → ≤20), daily review, token/log budgets, alerts at 50/75/90/100%, pause at 90% pending forecast, tested stop procedure."),
        ("6 • Missing permissions / quotas — schedule slip", "Medium. Likelihood: Medium.", "Med", "Med", "Platform", "Complete preflight before Week-1; quotas checked at Gate 0; no provisioning before green."),
        ("7 • Duplicate remediation on retried alerts", "Medium. Likelihood: Medium.", "Med", "Med", "Tech Lead", "Idempotency keys, concurrency controls, and repeated-delivery testing (blocking gate)."),
        ("8 • Fault testing impacts shared QI resources", "Medium. Likelihood: Low.", "Med", "Low", "Platform", "Isolated services, bounded fault injection, documented recovery, agreed test windows, no shared prod touch."),
    ]
    for title, impact, imp_level, lik_level, owner, mitigation in risks:
        # Color based on impact
        if imp_level == "High":
            border = RED
            bg = RED_LIGHT
        elif imp_level == "Med":
            border = AMBER
            bg = AMBER_LIGHT
        else:
            border = GREEN
            bg = GREEN_LIGHT
        title_p = Paragraph(f'<b>{title}</b>', ParagraphStyle('riskT', parent=sBody, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold', leading=9))
        impact_p = Paragraph(f'<font color="#475569" size=7>{impact}</font>', ParagraphStyle('riskI', parent=sBody, fontSize=7, textColor=SLATE, leading=9))
        mitigation_p = Paragraph(f'<b>Mitigation:</b> {mitigation}', ParagraphStyle('riskM', parent=sBody, fontSize=7, leading=10, textColor=HexColor("#334155")))
        meta = Paragraph(f'<font color="#991B1B" size=6><b>Impact: {imp_level}</b></font> &nbsp; <font color="#92400E" size=6><b>Likelihood: {lik_level}</b></font> &nbsp; <font color="#475569" size=6>Owner: {owner}</font>', ParagraphStyle('riskMeta', parent=sBody, fontSize=6, textColor=SLATE))
        inner = Table([[title_p],[impact_p],[meta],[mitigation_p]], colWidths=[152*mm])
        inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
        outer = Table([[inner]], colWidths=[154*mm])
        outer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), white),('BOX',(0,0),(-1,-1),0.5, SLATE_200),('LINEBEFORE',(0,0),(0,0),3, border),('ROUNDEDCORNERS',[6,6,6,6]),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2)]))
        story.append(outer)
        story.append(Spacer(1, 2*mm))
    story.append(Paragraph('Key Assumptions (to be validated at Gate 0)', sH2))
    a1 = Paragraph('<b>A1.</b> GitHub plan supports protected environments + required reviewers. <i>If not → compensating control or plan upgrade.</i>', ParagraphStyle('a1', parent=sBody, fontSize=7, leading=10))
    a2 = Paragraph('<b>A2.</b> Vertex AI Gemini quotas and token pricing as estimated. <i>Validate region + model before Week-3.</i>', ParagraphStyle('a2', parent=sBody, fontSize=7, leading=10))
    a3 = Paragraph('<b>A3.</b> Two reviewers available for approvals during test windows. <i>Confirm names at kickoff.</i>', ParagraphStyle('a3', parent=sBody, fontSize=7, leading=10))
    a4 = Paragraph('<b>A4.</b> USD 250 period clarified (full pilot vs. monthly). <i>Blocking for spend authorization.</i>', ParagraphStyle('a4', parent=sBody, fontSize=7, leading=10))
    assump_table = Table([[a1,a2],[a3,a4]], colWidths=[78*mm,78*mm])
    assump_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(assump_table)

    # SECTION 11
    story.append(Paragraph('<font color="#0E7490" size=6><b>11 &nbsp; GOVERNANCE & OPERATING MODEL</b></font>', sKicker))
    story.append(Paragraph('Who decides, who does, who reviews', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    gov_data = [
        ["Role", "Proposed Owner", "Accountability", "RACI"],
        ["Business Sponsors", "Ken / Prithiviraj", "Budget & pilot authorization; final Proceed/Stop", "A"],
        ["Pilot Coordinator", "Gupteswar Mishra", "Scope, dependencies, stakeholder reviews, final recommendation", "R"],
        ["Technical Lead", "Akshay Saxena", "Blueprint, build, integration, scoring & testing", "R"],
        ["Cloud / Platform", "Assigned Engineer", "GCP project, billing, IAM, quotas, infra, cost monitoring", "R"],
        ["CI/CD Owner", "Assigned Engineer", "Workflow integration, approval gates, deployment perms", "R"],
        ["Security Reviewer", "Assigned Reviewer", "Data handling, access controls, guardrails, bypass review", "C"],
        ["Remediation Approvers", "Named Engineers (≥2)", "Approve / reject each privileged proposal", "A"],
    ]
    story.append(styled_table(gov_data, [30*mm, 32*mm, 72*mm, 22*mm], font_size=6.5))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('<font color="#64748B" size=6>* RACI highlights primary accountability per activity; detailed RACI matrix to be confirmed at kickoff. Named owners & approvers must be confirmed before Gate 0.</font>', ParagraphStyle('raciNote', parent=sBody, fontSize=6, textColor=SLATE_LIGHT)))
    story.append(Spacer(1, 3*mm))
    cadence_left = Paragraph('<b>Operating cadence</b><br/>• <b>Daily stand-up</b> (15 min) during build & fault-testing<br/>• <b>Weekly steering</b> with sponsors + security (30 min) — gates, spend, risks<br/>• <b>Gate reviews</b> at 0,1,2,3,4,5,6 — written sign-off<br/>• <b>Incident review</b>: every scored run has a one-paragraph debrief', ParagraphStyle('cadL', parent=sBody, fontSize=7, leading=10))
    cadence_right = Paragraph('<b>Controls & assurance</b><br/>• Separation of duties: proposer ≠ approver ≠ executor<br/>• All privileged actions traceable: evidence → proposal → approval → workflow → outcome<br/>• Retention limits enforced; audit logs cost-assessed<br/>• GSK-separation attestation filed at Gate 6', ParagraphStyle('cadR', parent=sBody, fontSize=7, leading=10))
    cad_table = Table([[cadence_left, cadence_right]], colWidths=[78*mm,78*mm])
    cad_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(cad_table)

    # SECTION 12
    story.append(Paragraph('<font color="#A68B5B" size=6><b>12 &nbsp; DECISIONS REQUESTED & NEXT STEPS</b></font>', sKicker))
    story.append(Paragraph('What we need from you — this week', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    dec_data = [
        ["#", "Decision", "Options", "Required By"],
        ["D1", "Approve QI-only pilot scope; explicitly exclude GSK", "Approve / Amend / Reject", "Sponsors — before Gate 0"],
        ["D2", "Confirm USD 250 period (full 4–6 weeks vs. monthly)", "Full pilot / Monthly / Revised ceiling", "Sponsors + Finance — before Gate 0"],
        ["D3", "Confirm named owners, authorized approvers & escalation contacts", "Names + backups", "Coordinator — kickoff"],
        ["D4", "Confirm GitHub plan supports required approval controls", "Confirm / Compensating control / Upgrade", "CI/CD Owner — Gate 0"],
        ["D5", "Approve synthetic / QI-approved data use with Vertex AI + redaction", "Approve / Amend data scope", "Security + Sponsors — Gate 0"],
        ["D6", "Authorize provisioning only after readiness gate (Gate 0)", "Authorize / Conditional", "Sponsors — Gate 0 sign-off"],
        ["D7", "Require final review before any extension, prod rollout, or GSK proposal", "Mandate separate approvals", "Sponsors — standing"],
    ]
    story.append(styled_table(dec_data, [12*mm, 68*mm, 48*mm, 28*mm], font_size=6.5))
    story.append(Spacer(1, 4*mm))
    # Recommendation + Next steps side by side
    rec_left = Paragraph(
        '<b><font color="#0B1F4A">▶ Recommendation (Tier-1 view)</font></b><br/>'
        '<b>Conditionally approve</b> the pilot in principle. Begin with <b>2 services + recommendation-only</b> flow. Enable privileged remediation <i>only after</i> IAM isolation, approval enforcement, auditability, and all negative tests pass. Keep spend within the confirmed envelope and document every limitation. A successful QI pilot <b>does not</b> authorize GSK work.', ParagraphStyle('recL', parent=sBody, fontSize=7, leading=10, textColor=HexColor("#334155")))
    rec_right = Paragraph(
        '<b><font color="white">◈ Immediate next steps (5 days)</font></b><br/>'
        '<font color="#DBEAFE">• <b><font color="white">Day 1–2:</font></b> Decision log (D1–D7) + named RACI + approver list<br/>'
        '• <b><font color="white">Day 3:</font></b> Gate 0 preflight (IAM, WIF, quotas, GitHub protections)<br/>'
        '• <b><font color="white">Day 4:</font></b> Security review of data-handling & redaction<br/>'
        '• <b><font color="white">Day 5:</font></b> Gate 0 sign-off → authorize provisioning → Week 1 starts</font>', ParagraphStyle('recR', parent=sBody, fontSize=7, leading=10, textColor=white))
    rec_table = Table([[rec_left, rec_right]], colWidths=[78*mm,78*mm])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0), white),
        ('BACKGROUND',(1,0),(1,0), NAVY),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('GRID',(0,0),(-1,-1),0.5, SLATE_200),
        ('ROUNDEDCORNERS',[6,6,6,6]),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 3*mm))
    story.append(callout("What “conditional” means here", "Approval to <i>prepare</i> is not approval to <i>execute privileged changes</i>. The second authorization is gated by evidence — specifically, the bypass-test report at Gate 4. Sponsors retain a stop/pause right at any gate.", GREEN_LIGHT, HexColor("#A7F3D0"), HexColor("#D1FAE5"), "✓"))

    # APPENDICES
    story.append(Paragraph('<font color="#0E7490" size=6><b>APPENDICES</b></font>', sKicker))
    story.append(Paragraph('Reference, assumptions & traceability', sH1))
    story.append(HRFlowable(width="100%", thickness=0.8, color=GOLD, spaceAfter=6, spaceBefore=2))
    story.append(Paragraph('Appendix A — Reference Documentation', sH2))
    ref_data = [
        ["Topic", "Reference"],
        ["Workload Identity Federation — security best practices", "Google Cloud — WIF best practices<br/>https://docs.cloud.google.com/iam/docs/best-practices-for-using-workload-identity-federation"],
        ["Service accounts — security best practices", "Google Cloud — Service accounts<br/>https://docs.cloud.google.com/iam/docs/best-practices-service-accounts"],
        ["Deployment protection & approvals", "GitHub Actions — Deployment protection<br/>https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments"],
        ["Billing budgets & alerts", "Google Cloud — Budgets & alerts<br/>https://docs.cloud.google.com/billing/docs/how-to/budgets"],
        ["SAP / Grafana / Vertex AI details", "To be finalized during technical design & preflight validation (Gate 0–1)"],
    ]
    story.append(styled_table(ref_data, [50*mm, 106*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Appendix B — Proposal Schema & Allowlist (illustrative)', sH2))
    schema_left = Paragraph('<b>Proposal record (required fields)</b><br/><font size=6>incident_id • target {service, region, revision} • action_type (allowlist enum) • exact_params • evidence_citations[] • confidence • risk • validation_result • rollback_plan • proposal_hash • idempotency_key</font><br/><br/><font size=6>Approval is bound to <b>proposal_hash</b>. Any mutation → new hash → re-approval required.</font>', ParagraphStyle('schL', parent=sBody, fontSize=7, leading=10))
    schema_right = Paragraph('<b>Workflow spec (predefined)</b><br/>• Single protected workflow: <i>.github/workflows/remediate.yml</i> on protected branch + environment<br/>• Inputs validated against allowlist before execution<br/>• Executor SA: narrow resource permissions, 15-min TTL<br/>• Post-action: health check + audit record (actor, evidence, decision, outcome)', ParagraphStyle('schR', parent=sBody, fontSize=7, leading=10))
    schema_table = Table([[schema_left, schema_right]], colWidths=[78*mm,78*mm])
    schema_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5, SLATE_200),('GRID',(0,0),(-1,-1),0.5, SLATE_200),('ROUNDEDCORNERS',[6,6,6,6]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(schema_table)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Appendix C — Cost Model Assumptions', sH2))
    cost_assump = [
        ["Assumption", "Value Used", "Sensitivity"],
        ["Cloud Run services", "2 → 10–20, scale-to-zero, <1 vCPU avg", "Linear if scale-to-zero fails"],
        ["Grafana uptime", "Test windows + limited 24/7; small VM", "×2 if 24/7 on larger host"],
        ["Vertex AI tokens", "Bounded evidence (~4–8k in, ~1–2k out per incident), limited retries", "±40% if bounds loosen"],
        ["Log retention", "7 days pilot; no broad Data Access logs", "+30–50% at 30d or broad audit"],
        ["Regions", "2 (us-east1, us-central1) — no multi-region failover", "Cost doubles if 3+ regions"],
    ]
    story.append(styled_table(cost_assump, [32*mm, 66*mm, 58*mm], font_size=6.5))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Appendix D — Test Scenarios & Scoring Protocol', sH2))
    scen_data = [
        ["#", "Scenario", "Fault Injected", "Expected Diagnosis", "Scoring"],
        ["S1", "Bad deployment", "Push faulty revision (500s spike)", "Regression to revision N-1; evidence: error rate + deploy timestamp", "Primary diagnosis correct?"],
        ["S2", "Startup failure / crash loop", "Bad env var / missing secret", "Startup probe failure; evidence: crash log + config diff", "Primary diagnosis correct?"],
        ["S3", "Quota exhaustion", "Throttle to quota limit", "Quota metric + throttling log; no infra change", "Allowlist respected?"],
        ["S4", "Disabled API", "Disable dependent API", "API disabled error; evidence: audit log + API state", "Citations present?"],
        ["S5", "Configuration drift", "Drift flag / traffic split error", "Config diff + mismatch; bounded remediation", "Params in scope?"],
    ]
    story.append(styled_table(scen_data, [10*mm, 28*mm, 38*mm, 48*mm, 32*mm], font_size=6.5))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('Each scenario run is scored blind against ground truth. Live vs. simulated evidence is labelled. A run scores “correct” only if primary diagnosis matches and citations support it. Negative tests are scored separately as pass/fail on enforcement.', ParagraphStyle('scenNote', parent=sBody, fontSize=6, leading=8, textColor=SLATE)))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Appendix E — Document Control', sH2))
    ctrl_data = [
        ["Version", "Date", "Author", "Changes", "Status"],
        ["v1.0", "16 Oct 2026", "Gupteswar Mishra", "Initial working draft (7 pages)", "Superseded"],
        ["v2.0", "16 Oct 2026", "QI — Enhanced by Tier-1 Restructure", "Full restructure: pyramid summary, zero-trust detail, stage gates, unit-economics, RAID, RACI, approval matrix, appendices; visual upgrade — substance preserved", "Current — Awaiting approval"],
    ]
    story.append(styled_table(ctrl_data, [14*mm, 20*mm, 30*mm, 70*mm, 22*mm], font_size=6.5))
    story.append(Spacer(1, 4*mm))
    story.append(callout("How to use this document", "<b>Executives:</b> Read cover + §0 + §12. <b>Engineering & Security:</b> §4–§6. <b>Finance & Platform:</b> §8. <b>All reviewers:</b> §9–§11. Print via browser or PDF — this document is print-optimized to A4.", BLUE_LIGHT, HexColor("#BFDBFE"), HexColor("#DBEAFE"), "ℹ"))
    story.append(Spacer(1, 6*mm))
    # Final footer box
    final_box = Table([
        [Paragraph('<font color="#0B1F4A" size=7><b>QUANTUM INTEGRATORS — INTERNAL PROPOSAL</b></font>', ParagraphStyle('fb1', parent=sBody, alignment=TA_CENTER, fontSize=7, textColor=NAVY, fontName='Helvetica-Bold'))],
        [Paragraph('<font color="#0B1F4A" size=8><b>AI SRE Copilot — Dev Pilot • QI-AI-SRE-2026-001 • v2.0 Enhanced</b></font>', ParagraphStyle('fb2', parent=sBody, alignment=TA_CENTER, fontSize=8, textColor=NAVY))],
        [Paragraph('<font color="#475569" size=6>Confidential • QI Internal • GSK Excluded • 16 October 2026 • Prepared by Gupteswar Mishra & Akshay Saxena • Sponsors: Ken / Prithiviraj</font>', ParagraphStyle('fb3', parent=sBody, alignment=TA_CENTER, fontSize=6, textColor=SLATE))],
        [Paragraph('<font color="#64748B" size=6>This enhanced edition preserves all substance from v1.0 and elevates it for executive, audit, and client-readiness review. Original retained as <i>AI_SRE_Copilot_Dev_Pilot_Proposal_QI.pdf</i>.</font>', ParagraphStyle('fb4', parent=sBody, alignment=TA_CENTER, fontSize=6, textColor=SLATE_LIGHT))],
    ], colWidths=[156*mm])
    final_box.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), SLATE_50),
        ('BOX',(0,0),(-1,-1),0.5, SLATE_200),
        ('ROUNDEDCORNERS',[8,8,8,8]),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(final_box)

    # Build with custom page functions
    # We need to handle first page differently: cover background navy
    # So we will build with onFirstPage=cover_background, onLaterPages=header_footer
    # But our cover_background already draws navy; our story's first page will be navy, second page onwards will have header/footer
    # However reportlab's SimpleDocTemplate will call onFirstPage for page 1, onLaterPages for rest.
    # We defined cover_background to draw navy full page, and header_footer to draw header/footer for non-cover pages.
    # But header_footer currently skips page 1, so it's fine to use cover_background for first page, header_footer for later.
    # However cover_background currently also calls header_footer logic? We separated. Let's set onFirstPage to cover_background, onLaterPages to header_footer.
    doc.build(story, onFirstPage=cover_background, onLaterPages=header_footer)
    print(f"Generated {OUT}")

if __name__ == "__main__":
    build()
