# SAP Migration Training Handbook

Consolidated training and knowledge-transfer handbook for SAP → AWS migrations
(HANA, Oracle, Basis validation, cutover, hypercare).

**Version 1.0 — vetted release · Training period September–October 2026 · Primary trainer: Amit Prajapati**

---

## Deliverables

| Artefact | Path | Use |
|---|---|---|
| **Training handbook (HTML)** | [`handbook/index.html`](handbook/index.html) | Primary deliverable. Open in any browser: sticky navigation, interactive checklists with saved progress, collapsible knowledge check. Use **Print / save as PDF** for a paginated A4 PDF. |
| **Training handbook (Word)** | [`handbook/SAP-Migration-Training-Handbook-v1.0.docx`](handbook/SAP-Migration-Training-Handbook-v1.0.docx) | Consolidated Word edition: live TOC field (updates on open), landscape plates for the wide figures and matrices, all eight figures embedded as images, 71 tables and 15 checklists. |
| **Pocket reference (Word)** | [`handbook/SAP-Migration-Pocket-Reference-v1.0.docx`](handbook/SAP-Migration-Pocket-Reference-v1.0.docx) | Condensed field companion for the cutover bridge: run-card, the five checklists, quick references, return codes, Oracle/HANA cards, evidence naming, escalation. |
| **Diagrams (SVG)** | `handbook/assets/d*.svg` | The eight figures as standalone vector files — reusable in slides, runbooks and Confluence pages. |
| **Diagrams (PNG)** | `handbook/assets/d*.png` | High-resolution raster versions (2880 px wide) — these are what the Word document embeds. |
| **Diagrams (HTML viewers)** | `handbook/assets/d*.html` | Each figure on its own page, for review or printing individually. |

No build step is needed to read any of these — the HTML is a single self-contained
file with no external assets, no fonts to download and no network calls.

## Contents

Front matter (how to use, document control, revision history, approval, contents
and figure index), then:

1. Executive training overview
2. Training objectives and learning outcomes
3. End-to-end SAP-to-AWS migration lifecycle — **Figure 1**
4. Module 1 · Preparation, discovery and source baseline
5. Module 2 · Target architecture, AWS readiness and build — **Figures 2, 3**
6. Module 3 · SAP HANA MDC, backup and recovery — **Figure 4**
7. Module 4 · SAP post-migration validation
8. Module 5 · Performance monitoring and troubleshooting — **Figure 7**
9. Module 6 · Oracle database migration and switchover — **Figure 5**
10. Module 7 · Cutover, Go/No-Go, rollback and hypercare — **Figure 6**
11. SAP transaction and technology quick reference
12. Consolidated validation checklists (OS, SAP, database, performance, cutover)
13. Evidence and documentation strategy — **Figure 8**
14. Ownership and operating model
15. Troubleshooting playbook and common failure modes
16. Key lessons and practical guidance
17. Final knowledge check (16 questions with answers)

Appendices: A source coverage map · B training completion record · C glossary
(53 terms) · D technical review and vetting notes · E version control.

By the numbers: 25 sections, 8 vector figures (SVG in HTML, embedded PNG in Word),
70+ tables, 15 checklists with 209 checkable items, 12 troubleshooting scenarios,
~24,000 words.

## Regenerating the artefacts

The handbook is generated from source, so edits are made in `tools/` and rebuilt —
not in the output files.

```bash
# 1. Rebuild the HTML handbook + standalone SVG/HTML diagrams (stdlib only)
python3 training/tools/build_handbook.py

# 2. Rebuild the Word version from the generated HTML
#    (needs python-docx + lxml; any venv works)
python3 -m venv .venv && .venv/bin/pip install python-docx lxml
.venv/bin/python training/tools/md2docx.py

# 3. Render the figures to PNG for the Word build (needs matplotlib)
.venv/bin/python training/tools/render_png.py

# 3b. Word editions (full handbook + pocket reference)
.venv/bin/python training/tools/md2docx.py
.venv/bin/python training/tools/md2pocket.py

# 4. Verify diagram geometry (no text overflowing its container or the viewBox)
python3 training/tools/svg_qa.py "training/handbook/assets/*.svg"
```

`build_handbook.py` runs a QC pass on every build: tag balance, duplicate ids,
broken internal anchors, figure well-formedness and leaked template placeholders.
It exits non-zero if any check fails.

### Source layout

```
training/
├── handbook/
│   ├── index.html                          generated — do not edit by hand
│   ├── SAP-Migration-Training-Handbook-v1.0.docx   generated
│   └── assets/                             generated figures (.svg + .html viewers)
└── tools/
    ├── build_handbook.py                   HTML assembler + QC gate
    ├── content_a.py                        front matter, sections 1–6
    ├── content_b.py                        sections 7–10 (modules 4–7)
    ├── content_c.py                        sections 11–17 + appendices, glossary, quiz
    ├── htmlkit.py                          HTML building blocks (tables, checklists, callouts)
    ├── style.py                            stylesheet + client-side JS
    ├── diagrams.py                         the eight figures
    ├── svgkit.py                           SVG drawing primitives
    ├── svg_qa.py                           geometric diagram checker
    ├── mplkit.py                           Matplotlib backend for the diagram primitives
    ├── render_png.py                       SVG-primitive layout → high-res PNGs
    ├── docx_diagrams.py                    Word-native fallback versions of the figures
    ├── md2docx.py                          HTML → DOCX renderer (TOC field, landscape plates, PNGs)
    └── md2pocket.py                        condensed pocket-reference DOCX builder
```

## Conventions

- Source terminology from the training/MOM material is preserved verbatim. Items
  that are client-specific or unverifiable are tagged in the document and listed in
  **Appendix D.3** rather than silently rewritten.
- Technical clarifications made during the vetting pass are recorded in
  **Appendix D.2**, with the source statement, the finding and the action taken.
- This handbook is internal training material. It does not replace approved project
  runbooks, architecture baselines or change-management procedures.
