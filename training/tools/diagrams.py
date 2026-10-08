"""Handbook figures 1-8. Each function returns a self-contained SVG string."""

from __future__ import annotations

import os

from svgkit import (AMBER, AMBER_B, BLUE, BODY, GREEN, GREEN_B, GREY, GREY_B, MUTED, NAVY,
                    PLUM, PLUM_B, RED, RED_B, SKY, SKY_B, W, arrow, badge, callout, chip,
                    defs, diamond, footnote, legend, line, mtext, panel, path, rect,
                    stage_card, sub, sub_h, svg_open, text, title, wrap_px)


# --------------------------------------------------------------------------- #
# Figure 1 - End-to-end migration lifecycle
# --------------------------------------------------------------------------- #
def d1_lifecycle():
    stages = [
        ("Scope & Preparation", ["Confirm scope and systems", "Access + AWS account", "CMDB CI creation"], BLUE),
        ("Discovery & Baseline", ["Source parameters", "Interfaces and workload", "Baseline evidence"], BLUE),
        ("Sizing & Architecture", ["Consume approved sizing", "Target AWS design", "HA / DR design"], BLUE),
        ("Build Sheet", ["Prepare + peer review", "Customer finalisation", "Provisioning input"], BLUE),
        ("AWS Build", ["VPC, subnets, DNS", "Storage and resources", "Automation output"], BLUE),
        ("SAP / DB Build", ["Install and configure", "SAP + database ready", "Target validation"], BLUE),
        ("Pre-Cutover Validation", ["Source vs target compare", "Backup / recovery test", "Readiness checklist"], AMBER_B),
        ("Cutover", ["Shutdown + switchover", "DNS / IPAM update", "Technical validation"], AMBER_B),
        ("Go / No-Go", ["Evidence review", "Functional results", "Rollback readiness"], RED_B),
        ("Go-Live & Hypercare", ["Unlock users, resume jobs", "15 days of monitoring", "Issue classification"], GREEN_B),
    ]
    gates = {6: "GATE 1", 8: "GATE 2", 9: "GATE 3"}
    bw, bh, gx, gy = 316, 156, 40, 46
    x0, y0 = 40, 112
    H = y0 + 3 * (bh + gy) + 96
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 1 — End-to-end SAP-to-AWS migration lifecycle"))
    s.append(sub(40, 78, "Ten sequential stages. Amber and red stages are formal decision gates: work does not advance "
                         "without evidence and approval."))
    pos = {}
    for i, (name, items, accent) in enumerate(stages):
        r, c = divmod(i, 4)
        x, y = x0 + c * (bw + gx), y0 + r * (bh + gy)
        pos[i] = (x, y)
        s.append(stage_card(x, y, bw, bh, i + 1, name, items, accent))
        if i in gates:
            s.append(chip(x + bw - 46, y, gates[i], fill=accent, w=84, h=22, size=11))
    n = len(stages)
    rows = (n + 3) // 4
    for i in range(n - 1):
        r1, c1 = divmod(i, 4)
        r2, c2 = divmod(i + 1, 4)
        x, y = pos[i]
        nx, ny = pos[i + 1]
        if r1 == r2:
            s.append(arrow(x + bw, y + bh / 2, nx - 5, y + bh / 2, color="#8ea6c0", sw=2.4))
        else:
            midy = y + bh + gy / 2
            s.append(path("M%s %s V%s H%s V%s" % (x + bw / 2, y + bh, midy, nx + bw / 2, ny - 5),
                          color="#8ea6c0", sw=2.4))
    yy = y0 + 3 * (bh + gy) - 8
    s.append(rect(40, yy, W - 80, 76, fill=SKY, stroke=SKY_B, rx=10))
    s.append(text(64, yy + 28, "SEQUENCE TO REMEMBER", size=11.5, fill=BLUE, weight=800, anchor="start", spacing="1.2"))
    s.append(text(64, yy + 54, "Scope  →  Discovery  →  Inventory  →  Dependencies  →  Sizing  →  Architecture  →  "
                               "Build  →  Validation  →  Migration  →  Handover",
                  size=14.5, fill=NAVY, weight=700, anchor="start"))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 2 - Responsibility split (RACI swimlane)
# --------------------------------------------------------------------------- #
def d2_raci():
    phases = ["Discovery &\nBaseline", "Build Sheet &\nAWS Build", "SAP / DB\nBuild",
              "Pre-Cutover\nValidation", "Cutover\nWindow", "Go / No-Go", "Hypercare"]
    lanes = [
        ("Automation / Cloud", ["R", "A · R", "C", "R", "C", "I", "C"]),
        ("Basis / Migration", ["A · R", "A", "A · R", "A · R", "A · R", "R", "A · R"]),
        ("DBA", ["C", "C", "R", "R", "A · R", "R", "R"]),
        ("Linux / OS", ["C", "R", "R", "R", "R", "I", "C"]),
        ("Network / DNS / IPAM", ["C", "R", "C", "C", "R", "I", "C"]),
        ("Security / AD", ["C", "C", "C", "R", "R", "C", "C"]),
        ("Application / Functional", ["I", "I", "C", "R", "C", "A · R", "R"]),
        ("PMO / Stakeholders", ["I", "C", "I", "C", "I", "A", "A"]),
    ]
    x0, y0, cw, ch, lw = 300, 138, 148, 54, 260
    colors = {"A": (RED, RED_B), "R": (SKY, BLUE), "C": (GREY, "#7b8794"), "I": ("#ffffff", "#c7d2e0")}
    H = y0 + len(lanes) * ch + 210
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 2 — Responsibility split across the migration lifecycle"))
    s.append(sub(40, 78, "A = Accountable (single owner), R = Responsible (does the work), C = Consulted, I = Informed. "
                         "Every activity needs exactly one A; ambiguity here is how conflicting changes reach production."))
    for j, p in enumerate(phases):
        x = x0 + j * cw
        s.append(rect(x + 3, y0 - 48, cw - 6, 42, fill="url(#hdr)", stroke="none", rx=8))
        s.append(mtext(x + cw / 2, y0 - 27, p.split("\n"), size=12.5, fill="#ffffff", weight=700, lh=15))
    for i, (lane, marks) in enumerate(lanes):
        y = y0 + i * ch
        s.append(rect(x0, y, cw * len(phases), ch, fill="#ffffff" if i % 2 == 0 else "#fafbfd", stroke="none", rx=0))
        s.append(rect(40, y + 6, lw, ch - 12, fill=NAVY if i % 2 == 0 else "#173a63", stroke="none", rx=8))
        s.append(text(56, y + ch / 2 + 1, lane, size=12.5, fill="#ffffff", weight=700, anchor="start"))
        for j, m in enumerate(marks):
            x = x0 + j * cw
            fill, stroke = colors[m.split(" · ")[0]]
            s.append(rect(x + 12, y + 11, cw - 24, ch - 22, fill=fill, stroke=stroke, rx=7, sw=1.4))
            s.append(text(x + cw / 2, y + ch / 2 + 5, m.replace(" · ", " / "), size=12.5, fill=stroke, weight=800))
        s.append(line(x0, y + ch, x0 + cw * len(phases), y + ch, color="#e2e8f0", sw=1))
    yb = y0 + len(lanes) * ch + 24
    s.append(legend([("box", RED, "A — Accountable"), ("box", SKY, "R — Responsible"),
                     ("box", GREY, "C — Consulted"), ("box", "#ffffff", "I — Informed")], 40, yb + 12))
    s.append(callout(40, yb + 34, W - 80, 118, "OWNERSHIP PRINCIPLE",
                     ["One accountable owner per assigned SID/system, with a named guide/support person and controlled change.",
                      "Multiple engineers must not independently modify the same assigned system."],
                     size=13.5, lh=26))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 3 - Target AWS reference architecture
# --------------------------------------------------------------------------- #
def d3_aws():
    H = 880
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 3 — Target AWS reference architecture"))
    s.append(sub(40, 78, "Training reference only. Region, AZ count, instance types, storage classes, HA design and "
                         "connectivity always come from the approved sizing report and build sheet — never from a diagram."))
    s.append(rect(330, 110, 1070, 646, fill="#fbfcfe", stroke=SKY_B, rx=14, sw=2))
    s.append(chip(394, 110, "AWS REGION", fill=BLUE, w=126, h=28, size=12))
    s.append(text(1376, 132, "Route 53 hosted zone + inbound/outbound resolver rules", size=12,
                  fill="#7b8794", weight=600, anchor="end"))
    for name, x in (("AVAILABILITY ZONE A", 360), ("AVAILABILITY ZONE B", 900)):
        s.append(rect(x, 152, 470, 452, fill="#ffffff", stroke=GREY_B, rx=12, dash="7 5"))
        s.append(chip(x + 110, 152, name, fill="#5b7288", w=204, h=24, size=11))
    s.append(panel(382, 186, 426, 176, "App subnet — SAP application tier"))
    for label, x, note in (("ASCS", 404, "central services"), ("ERS / CRS", 520, "failover partner"),
                           ("PAS", 664, "primary app server")):
        s.append(rect(x, 240, 108, 62, fill=SKY, stroke=BLUE, rx=8))
        s.append(text(x + 54, 266, label, size=13.5, fill=NAVY, weight=800))
        s.append(text(x + 54, 287, note, size=10.5, fill=MUTED, weight=600))
    s.append(text(595, 338, "Additional dialog instances (AAS) per sizing", size=11.5, fill="#7b8794", weight=600))
    s.append(panel(922, 186, 426, 176, "App subnet — SAP application tier"))
    for label, x, note in (("AAS", 944, "additional app"), ("SAProuter /\nbastion", 1060, "secure access"),
                           ("Web Dispatcher", 1216, "HTTP(S) entry")):
        s.append(rect(x, 240, 120, 62, fill=SKY, stroke=BLUE, rx=8))
        s.append(mtext(x + 60, 262, label.split("\n"), size=12.5, fill=NAVY, weight=800, lh=15))
        s.append(text(x + 60, 292, note, size=10.5, fill=MUTED, weight=600))
    s.append(panel(382, 386, 426, 196, "DB subnet — database tier", hfill="#123b2a"))
    s.append(rect(404, 440, 382, 118, fill=GREEN, stroke=GREEN_B, rx=9))
    s.append(text(595, 466, "SAP HANA (MDC)  or  Oracle DB", size=14, fill="#123b2a", weight=800))
    s.append(mtext(595, 502, ["Primary instance on a certified EC2 storage class",
                              "HSR system replication or Data Guard standby as designed"],
                   size=11.5, fill="#2f6b46", weight=600, lh=17))
    s.append(panel(922, 386, 426, 196, "Standby / HA partner", hfill="#123b2a"))
    s.append(rect(944, 440, 382, 118, fill=GREEN, stroke=GREEN_B, rx=9))
    s.append(text(1135, 466, "HANA System Replication / Data Guard", size=13, fill="#123b2a", weight=800))
    s.append(mtext(1135, 502, ["Sync or async replication per the agreed RPO",
                               "Broker + observer node where failover is designed"],
                   size=11.5, fill="#2f6b46", weight=600, lh=17))
    s.append(path("M786 499 H940", color=GREEN_B, sw=2.6, dash="7 5"))
    s.append(text(863, 486, "redo / log shipping", size=11, fill="#2f6b46", weight=700))
    s.append(rect(360, 620, 1010, 112, fill="#ffffff", stroke=GREY_B, rx=12))
    s.append(text(384, 646, "SHARED / MANAGED SERVICES", size=11.5, fill=BLUE, weight=800, anchor="start", spacing="1.1"))
    services = [("Amazon S3", "HANA backup via Backint,\nOracle backup / packages"),
                ("Amazon EFS", "NFS replacement for shared\nand interface directories"),
                ("Route 53", "Private zones, records and\nthe CNAME flip at cutover"),
                ("EC2 snapshots", "Rollback recovery point taken\nbefore switchover"),
                ("KMS", "Encryption keys for storage,\nbackups and snapshots")]
    for i, (n, d) in enumerate(services):
        x = 384 + i * 196
        s.append(rect(x, 658, 180, 60, fill=SKY, stroke=SKY_B, rx=8))
        s.append(text(x + 90, 678, n, size=12.5, fill=NAVY, weight=800))
        s.append(mtext(x + 90, 700, d.split("\n"), size=9.8, fill=MUTED, weight=600, lh=12))
    s.append(rect(40, 200, 250, 300, fill=GREY, stroke=GREY_B, rx=12, shadow=True))
    s.append(text(165, 232, "SOURCE LANDSCAPE", size=12.5, fill=NAVY, weight=800, spacing="0.8"))
    for i, (n, d) in enumerate((("On-prem / source DC", "SAP on Oracle or HANA"),
                                ("External agents", "Control-M, NetBackup,\nOEM/OBM"),
                                ("Interfaces", "SAP↔SAP, middleware,\nRFC, SSO, NFS"))):
        y = 254 + i * 78
        s.append(rect(58, y, 214, 66, fill="#ffffff", stroke=GREY_B, rx=8))
        s.append(text(165, y + 22, n, size=12, fill=NAVY, weight=700))
        s.append(mtext(165, y + 45, d.split("\n"), size=10, fill=MUTED, weight=600, lh=12))
    s.append(path("M290 350 H378", color="#8ea6c0", sw=3))
    s.append(text(334, 338, "connectivity", size=10.5, fill=MUTED, weight=700))
    s.append(path("M290 300 H318 V246 H378", color="#8ea6c0", sw=2.2, dash="6 5"))
    s.append(callout(40, 540, 250, 216, "VALIDATE,\nDON'T ASSUME".replace("\n", " "),
                     ["VPC, AZs, subnets, free IPs", "DNS and Route 53 resolution", "S3 bucket, folders, policies",
                      "Read/write and backend connect", "CMDB CI, relationship, status", "Details match the build sheet"],
                     size=11.5, lh=22, bullet=True))
    s.append(footnote(40, H - 24, "This is a teaching reference, not an approved architecture artefact. It does not replace "
                                  "the project build sheet, architecture baseline or change-management procedure."))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 4 - HANA MDC, backup and recovery
# --------------------------------------------------------------------------- #
def d4_hana():
    H = 900
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 4 — SAP HANA MDC architecture, S3 backup backend and recovery flow"))
    s.append(sub(40, 78, "SystemDB and TenantDB are database containers inside one HANA system. They are not an HA design: "
                         "high availability is a separate infrastructure-level decision (HSR, cluster, storage)."))
    s.append(panel(40, 110, 300, 470, "Three-tier application validation"))
    tiers = [("1  UI / Presentation layer", "SAP GUI, Fiori, browser", SKY, BLUE),
             ("2  Application layer", "PAS / AAS work processes", SKY, BLUE),
             ("3  Database layer", "HANA SystemDB + TenantDB", GREEN, "#123b2a")]
    for i, (n, d, f, b) in enumerate(tiers):
        y = 180 + i * 120
        s.append(rect(64, y, 252, 88, fill=f, stroke=b, rx=10, shadow=True))
        s.append(text(190, y + 36, n, size=13.5, fill=NAVY, weight=800))
        s.append(text(190, y + 60, d, size=11.5, fill=MUTED, weight=600))
        if i < 2:
            s.append(arrow(190, y + 88, 190, y + 116, color="#8ea6c0", sw=2.4))
    s.append(rect(64, 520, 252, 44, fill=AMBER, stroke=AMBER_B, rx=8))
    s.append(mtext(190, 543, ["Recovery order: database first,", "then start and validate app servers"],
                   size=11.5, fill="#8a6410", weight=700, lh=15))
    s.append(panel(390, 110, 520, 470, "HANA host — one EC2 instance / VM (or an HSR pair)"))
    s.append(rect(414, 176, 472, 150, fill=PLUM, stroke=PLUM_B, rx=10, shadow=True))
    s.append(text(650, 202, "SystemDB  (SYSTEMDB)", size=14, fill="#4a2a5c", weight=800))
    s.append(mtext(650, 244, ["Central management and monitoring",
                              "Own login context and credentials (SYSTEM user)",
                              "Holds the backup catalogue for all tenants"],
                   size=11.5, fill="#6b4a80", weight=600, lh=18))
    s.append(rect(414, 344, 472, 150, fill=GREEN, stroke=GREEN_B, rx=10, shadow=True))
    s.append(text(650, 370, "TenantDB  (for example PRD)", size=14, fill="#123b2a", weight=800))
    s.append(mtext(650, 412, ["Application and data workload",
                              "Own login context and credentials",
                              "Own backup configuration and data volume"],
                   size=11.5, fill="#2f6b46", weight=600, lh=18))
    s.append(arrow(650, 326, 650, 340, color=PLUM_B, sw=2.4))
    s.append(rect(414, 512, 472, 52, fill="#ffffff", stroke=GREY_B, rx=8))
    s.append(mtext(650, 538, ["Services: nameserver (SystemDB) · indexserver (per tenant)",
                              "Pre-checks: sizing, shared FS, INI files, THP,",
                              "kernel/HANA version, evidence"],
                   size=11.3, fill=MUTED, weight=600, lh=16))
    s.append(panel(950, 110, 450, 470, "Backup backend and recovery sequence"))
    s.append(rect(974, 176, 402, 92, fill=SKY, stroke=BLUE, rx=10, shadow=True))
    s.append(text(1175, 204, "Amazon S3 bucket", size=14, fill=NAVY, weight=800))
    s.append(mtext(1175, 238, ["Backint agent or file-based backup", "Bucket + folders, RW policy, connectivity"],
                   size=11.5, fill=BODY, weight=600, lh=17))
    flow = [("Source backup completed and validated on the source system"),
            ("Configuration files available: global.ini, nameserver.ini, topology"),
            ("Backup data on the S3 backend, permissions and path verified"),
            ("Target HANA configured, restore path and credentials set"),
            ("Recovery initiated from the SystemDB / tenant context"),
            ("Database and application connectivity validated, evidence captured")]
    for i, l in enumerate(flow):
        y = 300 + i * 44
        s.append(badge(996, y, i + 1, r=14, fill=BLUE, size=12.5))
        lines = wrap_px(l, 11.8, 330, weight=600)
        s.append(mtext(1016, y - 1, lines, size=11.8, fill=BODY, weight=600, lh=15, anchor="start"))
    s.append(rect(40, 610, W - 80, 106, fill=NAVY, stroke="none", rx=12, shadow=True))
    s.append(text(64, 640, "RECOVERY FLOW", size=11.5, fill="#8fb4de", weight=800, anchor="start", spacing="1.2"))
    steps = ["Source backup", "Configuration file", "S3 backend", "Target configuration", "Recovery", "Validation"]
    for i, st in enumerate(steps):
        x = 64 + i * 216
        s.append(rect(x, 654, 190, 42, fill="#1b4f86", stroke="#4b7cb3", rx=8))
        s.append(text(x + 95, 680, st, size=12.8, fill="#ffffff", weight=700))
        if i < len(steps) - 1:
            s.append(text(x + 203, 682, "›", size=20, fill="#8fb4de", weight=700))
    s.append(callout(40, 736, W - 80, 112, "CUTOVER RULE",
                     ["Test backup and recovery BEFORE cutover. During cutover take the final backup, validate it, and only then stop the source system.",
                      "The source stays available until the required final backup activity completes successfully — that backup is also your rollback anchor."],
                     size=13, lh=24))
    s.append(footnote(40, H - 22, "Source terminology preserved. Confirm Backint versus file-based backup, the exact INI/parameter set and "
                                  "the tenant naming convention against the project HANA standard before execution."))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 5 - Oracle Data Guard switchover
# --------------------------------------------------------------------------- #
def d5_oracle():
    seq = [
        ("Pre-checks", "Listener and SQL*Net, Data Guard parameters, SID settings, Broker, observer node, patch-level alignment"),
        ("Synchronisation review", "Log switching reviewed, apply lag checked, source and target SCN compared for consistency"),
        ("Evidence + approval", "Outputs and screenshots attached to the Jira/change ticket; approval obtained before production changes"),
        ("Snapshot", "AWS disk-level snapshot of the target taken — this is the rollback recovery point"),
        ("Shutdown source", "Application shutdown complete and DBA handover confirmed; source primary closed"),
        ("Switchover / activate", "Target standby activated and opened as the new primary database"),
        ("Post-validation", "New primary validated; DBVERIFY run for block corruption; RMAN backup taken; OEM agent verified"),
        ("DNS / IPAM", "Virtual hostname unchanged, target IP updated, CNAME repointed, resolution verified, stale host entries cleaned"),
    ]
    y0 = 402
    yb = y0 + len(seq) * 52 + 40
    H = yb + 172
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 5 — Oracle Data Guard migration: switchover, SCN synchronisation and rollback"))
    s.append(sub(40, 78, "A switchover is a planned, reversible role swap. A failover is disaster recovery and is not reversible "
                         "in the same way. This module covers the planned switchover only."))
    s.append(panel(60, 116 + sub_h("A switchover is a planned, reversible role swap. A failover is disaster recovery and is not reversible "
                                   "in the same way. This module covers the planned switchover only."),
                   560, 250, "SOURCE — on-premises / source DC", hfill="#5c2b2b"))
    base = 116 + sub_h("A switchover is a planned, reversible role swap. A failover is disaster recovery and is not reversible "
                       "in the same way. This module covers the planned switchover only.")
    s.append(rect(88, base + 64, 236, 100, fill=RED, stroke=RED_B, rx=10))
    s.append(text(206, base + 96, "PRIMARY", size=15, fill="#7d2b30", weight=800))
    s.append(mtext(206, base + 128, ["Open and serving SAP", "Generates archive/redo"], size=11.5,
                   fill="#8d4a4e", weight=600, lh=17))
    s.append(rect(356, base + 64, 236, 100, fill=GREY, stroke=GREY_B, rx=10))
    s.append(text(474, base + 96, "AFTER SWITCHOVER", size=13, fill=BODY, weight=800))
    s.append(mtext(474, base + 128, ["Shut down after final", "validation and snapshot"], size=11.5,
                   fill=MUTED, weight=600, lh=17))
    s.append(rect(88, base + 184, 504, 40, fill="#ffffff", stroke=GREY_B, rx=8))
    s.append(text(340, base + 209, "SCN source:  SELECT current_scn FROM v$database;", size=12,
                  fill=BODY, weight=600))
    s.append(panel(820, base, 560, 250, "TARGET — AWS", hfill="#123b2a"))
    s.append(rect(848, base + 64, 236, 100, fill=SKY, stroke=BLUE, rx=10))
    s.append(text(966, base + 96, "STANDBY", size=15, fill=NAVY, weight=800))
    s.append(mtext(966, base + 128, ["Managed recovery applying", "redo shipped from source"], size=11.5,
                   fill=BODY, weight=600, lh=17))
    s.append(rect(1116, base + 64, 236, 100, fill=GREEN, stroke=GREEN_B, rx=10))
    s.append(text(1234, base + 96, "NEW PRIMARY", size=14, fill="#123b2a", weight=800))
    s.append(mtext(1234, base + 128, ["Activated and opened", "after switchover"], size=11.5,
                   fill="#2f6b46", weight=600, lh=17))
    s.append(rect(848, base + 184, 504, 40, fill="#ffffff", stroke=GREY_B, rx=8))
    s.append(text(1100, base + 209, "SCN target  →  values must match before switchover", size=12,
                  fill=BODY, weight=600))
    s.append(path("M620 %s H816" % (base + 98), color=BLUE, sw=3))
    s.append(text(718, base + 84, "redo transport", size=11.5, fill=BLUE, weight=700))
    s.append(path("M816 %s H624" % (base + 134), color="#8ea6c0", sw=2, dash="6 5"))
    s.append(text(718, base + 156, "apply / gap check", size=11, fill=MUTED, weight=600))
    s.append(rect(60, y0 - 14, W - 120, len(seq) * 52 + 26, fill="#ffffff", stroke=GREY_B, rx=12, shadow=True))
    for i, (n, d) in enumerate(seq):
        y = y0 + i * 52 + 14
        col = BLUE
        if i == 3:
            col = AMBER_B
        if i == 6:
            col = GREEN_B
        s.append(badge(104, y, i + 1, r=16, fill=col, size=13.5))
        s.append(text(136, y + 1, n, size=13.5, fill=NAVY, weight=800, anchor="start"))
        s.append(text(336, y + 1, d, size=12.3, fill=BODY, weight=500, anchor="start"))
        if i < len(seq) - 1:
            s.append(line(104, y + 17, 104, y + 37, color="#dbe3ec", sw=2))
    s.append(callout(60, yb, 660, 118, "ROLLBACK PATH",
                     ["Restore target volumes from the pre-switchover snapshot, revert DNS/CNAME to the source, restart the source primary.",
                      "Rollback readiness is maintained until the migration is declared safe."],
                     fill=RED, stroke=RED_B, kfill="#7d2b30", bfill="#7d2b30", size=12.5, lh=22))
    s.append(callout(760, yb, 620, 118, "VALIDATION GATE",
                     ["DBVERIFY clean (no corrupted blocks) → RMAN backup successful → OEM agent reporting.",
                      "Only then is the new primary considered technically accepted."],
                     size=12.5, lh=22))
    s.append(footnote(60, H - 22, "Command-level detail (DGMGRL versus ALTER DATABASE SWITCHOVER, Broker configuration, observer placement) "
                                  "is defined in the project runbook, not in this handbook."))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 6 - Cutover sequence, Go/No-Go and rollback
# --------------------------------------------------------------------------- #
def d6_cutover():
    H = 1000
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 6 — Cutover execution sequence with Go/No-Go decision and rollback path"))
    s.append(sub(40, 78, "Each lane hands over explicitly. Nothing starts before the previous lane confirms completion and the "
                         "evidence is attached to the change record."))
    lanes = [("APPLICATION", "#5b7288"), ("DBA", "#123b2a"), ("BASIS / MIGRATION", BLUE), ("FUNCTIONAL + PMO", "#8a6410")]
    lw, x0 = 330, 60
    for i, (n, c) in enumerate(lanes):
        x = x0 + i * (lw + 14)
        s.append(rect(x, 106, lw, 566, fill="#fbfcfe", stroke=GREY_B, rx=12))
        s.append(rect(x, 106, lw, 40, fill=c, stroke="none", rx=12))
        s.append(rect(x, 132, lw, 14, fill=c, stroke="none", rx=0))
        s.append(text(x + lw / 2, 132, n, size=12.5, fill="#ffffff", weight=800, spacing="0.8"))
    steps = {
        0: [(1, "Cooldown / ramp-up activities complete", 176),
            (2, "Application and web services stopped", 250),
            (3, "Handover to the DBA team confirmed", 324)],
        1: [(4, "Final backup and AWS disk-level snapshot", 250),
            (5, "Data Guard switchover or HANA recovery", 340),
            (6, "DBVERIFY, RMAN and database validation", 430)],
        2: [(7, "rsync SAP global directory; clean host/IPAM entries", 430),
            (8, "Validate profile parameters, kernel permissions, root scripts", 504),
            (9, "R3TRANS -d must return code 0000 before SAP start", 578),
            (10, "Start SAP; validate SNC/SSO, certificates, Gateway, RFC", 636)],
        3: [(11, "Business transaction tests, interfaces, printers, evidence", 636)],
    }
    for lane_i, items in steps.items():
        x = x0 + lane_i * (lw + 14)
        for n, label, y in items:
            s.append(rect(x + 18, y, lw - 36, 56, fill="#ffffff", stroke=SKY_B, rx=9, shadow=True))
            s.append(badge(x + 44, y + 28, n, r=13, fill=BLUE, size=12))
            s.append(mtext(x + 62, y + 28, wrap_px(label, 11.6, 232, weight=600), size=11.6, fill=BODY, weight=600,
                           lh=15, anchor="start"))
    s.append(path("M372 352 H392 V278 H416", color="#8ea6c0", sw=2.4))
    s.append(text(392, 392, "handover", size=10.5, fill=MUTED, weight=700))
    s.append(path("M716 458 H736 V458 H760", color="#8ea6c0", sw=2.4))
    s.append(path("M1046 664 H1090 V664 H1104", color="#8ea6c0", sw=2.4))
    dy = 706
    s.append(path("M720 672 V%s" % dy, color="#8ea6c0", sw=2.6))
    s.append(diamond(W / 2, dy + 62, 300, 124))
    s.append(text(W / 2, dy + 56, "Go / No-Go", size=17, fill="#8a6410", weight=800))
    s.append(text(W / 2, dy + 80, "technical + functional + owner sign-off", size=11.5, fill="#8a6410", weight=600))
    s.append(path("M%s %s H1120 V%s" % (W / 2 + 150, dy + 62, dy + 152), color=GREEN_B, sw=3))
    s.append(chip(W / 2 + 250, dy + 62, "GO", fill=GREEN_B, w=64, h=26, size=12.5))
    s.append(rect(760, dy + 152, 620, 100, fill=GREEN, stroke=GREEN_B, rx=12, shadow=True))
    s.append(text(784, dy + 182, "GO-LIVE & HYPERCARE", size=11.5, fill="#123b2a", weight=800,
                  anchor="start", spacing="1.1"))
    s.append(mtext(1070, dy + 218, ["Unlock users · resume background jobs and Control-M · complete EDG / SAProuter configuration",
                                     "15 days of hypercare · classify each issue as migration-related or pre-existing and route it"],
                   size=12, fill="#2f6b46", weight=600, lh=19))
    s.append(path("M%s %s H320 V%s" % (W / 2 - 150, dy + 62, dy + 152), color=RED_B, sw=3))
    s.append(chip(W / 2 - 250, dy + 62, "NO-GO", fill=RED_B, w=84, h=26, size=12.5))
    s.append(rect(60, dy + 152, 660, 100, fill=RED, stroke=RED_B, rx=12, shadow=True))
    s.append(text(84, dy + 182, "ROLLBACK", size=11.5, fill="#7d2b30", weight=800, anchor="start", spacing="1.1"))
    s.append(mtext(390, dy + 218, ["Execute the agreed rollback procedure: restore the snapshot or recover the source, revert DNS/CNAME,",
                                    "restart the source and re-open the incident path. Record the reason and evidence for the No-Go."],
                   size=12, fill="#7d2b30", weight=600, lh=19))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 7 - Performance monitoring and troubleshooting
# --------------------------------------------------------------------------- #
def d7_perf():
    H = 830
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 7 — Performance monitoring, memory escalation and troubleshooting path"))
    s.append(sub(40, 78, "Top-down triage: workload statistics first, individual records second, memory and buffer behaviour third, "
                         "root cause before any parameter change."))
    s.append(panel(60, 116, 430, 470, "ST02 — SAP memory escalation"))
    mem = [("Roll area / roll memory", "Per work process; rolled-out user context", SKY, BLUE),
           ("Extended memory (EM)", "Shared pool used first for user context", SKY, BLUE),
           ("Heap / private memory", "Used when EM is exhausted — process goes PRIVATE", AMBER, AMBER_B),
           ("Paging and swaps", "Paging memory, roll-in / roll-out activity", RED, RED_B),
           ("Buffer memory", "Program, single record, table, export/import buffers", GREY, MUTED)]
    for i, (n, d, f, b) in enumerate(mem):
        y = 180 + i * 78
        s.append(rect(84, y, 382, 62, fill=f, stroke=b, rx=9))
        s.append(text(275, y + 25, n, size=13, fill=NAVY, weight=800))
        s.append(text(275, y + 46, d, size=11, fill=MUTED, weight=600))
        if i < 4:
            s.append(arrow(275, y + 62, 275, y + 74, color="#8ea6c0", sw=2.2))
    s.append(text(470, 340, "EM exhausted", size=11, fill=AMBER_B, weight=800, anchor="end"))
    s.append(panel(530, 116, 850, 470, "Troubleshooting path"))
    flow = [
        ("Symptom reported", "Slow dialog, timeout, batch overrun, user complaint", SKY, BLUE),
        ("ST03 / ST03N workload", "Response, DB, CPU and wait time — daily, weekly, monthly trend", SKY, BLUE),
        ("STAD detailed records", "Isolate the slow transactions, users, DB-intensive or CPU-intensive steps", SKY, BLUE),
        ("Classify the bottleneck", "High DB time → database/SQL/network · high CPU → ABAP/app · high wait → memory, enqueue, RFC", AMBER, AMBER_B),
        ("ST02 memory and buffers", "EM, heap/private, roll, paging, buffer utilisation and hit ratio", AMBER, AMBER_B),
        ("Find the root cause", "Missing index, poor access path, custom code, parameter, volume growth, infrastructure", RED, RED_B),
        ("Fix with the owning team", "DBA / ABAP / Linux / Network; parameter change via the approved route (RZ10 vs RZ11)", GREEN, GREEN_B),
        ("Re-baseline and evidence", "Re-measure against the pre-migration baseline and attach before/after evidence", GREEN, GREEN_B),
    ]
    for i, (n, d, f, b) in enumerate(flow):
        y = 176 + i * 50
        s.append(rect(556, y, 800, 42, fill=f, stroke=b, rx=8))
        s.append(badge(582, y + 21, i + 1, r=13, fill=b, size=12))
        s.append(text(606, y + 18, n, size=12.8, fill=NAVY, weight=800, anchor="start"))
        s.append(text(606, y + 34, d, size=10.8, fill=MUTED, weight=600, anchor="start"))
    s.append(rect(60, 610, 660, 156, fill="#ffffff", stroke=GREY_B, rx=12, shadow=True))
    s.append(text(84, 640, "RZ10 vs RZ11 — PICK THE RIGHT TOOL", size=11, fill=BLUE, weight=800,
                  anchor="start", spacing="1.0"))
    s.append(rect(84, 654, 296, 92, fill=SKY, stroke=BLUE, rx=9))
    s.append(text(232, 680, "RZ10", size=14, fill=NAVY, weight=800))
    s.append(mtext(232, 714, ["Persistent profile parameter;", "import and activate; a restart", "is often required"],
                   size=11, fill=BODY, weight=600, lh=15))
    s.append(rect(400, 654, 296, 92, fill=GREY, stroke=MUTED, rx=9))
    s.append(text(548, 680, "RZ11", size=14, fill=NAVY, weight=800))
    s.append(mtext(548, 714, ["Dynamic / temporary change where", "the parameter supports it — not a", "permanent configuration change"],
                   size=11, fill=BODY, weight=600, lh=15))
    s.append(callout(760, 610, 620, 156, "THRESHOLD CAUTION",
                     ["The source training quoted ≈1200 ms response time and ≈40% average database request time as discussion values.",
                      "Validate them against the applicable SAP and client baseline before using them as production alerting thresholds.",
                      "Never raise a memory parameter before identifying what is consuming the memory."],
                     size=12, lh=22))
    s.append(footnote(60, H - 22, "ST03N is the current workload transaction; ST03 is retained here because the source material and many runbooks "
                                  "still reference it. STAD reads the statistical records behind the workload statistics."))
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------------------- #
# Figure 8 - Evidence lifecycle
# --------------------------------------------------------------------------- #
def d8_evidence():
    H = 620
    s = [svg_open(H), defs(), rect(0, 0, W, H, fill="url(#grid)", stroke="none", rx=0)]
    s.append(title(40, 52, "Figure 8 — Evidence lifecycle: baseline, compare, correct, retest, handover"))
    s.append(sub(40, 78, "Working before migration should work after migration. Evidence is what turns that principle into "
                         "something you can actually prove."))
    steps = ["Capture source\nbaseline evidence", "Execute migration /\ncutover activities",
             "Capture equivalent\ntarget evidence", "Compare source\nagainst target",
             "Identify and log\ndeviations", "Correct with the\nresponsible team",
             "Retest the affected\ncheck", "Capture final\nevidence", "Complete handover\nand sign-off"]
    bw, bh, gap = 140, 96, 12
    x0 = (W - (len(steps) * bw + (len(steps) - 1) * gap)) / 2
    y0 = 156
    cols = [BLUE, BLUE, BLUE, AMBER_B, AMBER_B, RED_B, GREEN_B, GREEN_B, NAVY]
    fills = {BLUE: SKY, AMBER_B: AMBER, RED_B: RED, GREEN_B: GREEN, NAVY: "#e9edf3"}
    for i, st in enumerate(steps):
        x = x0 + i * (bw + gap)
        c = cols[i]
        s.append(rect(x, y0, bw, bh, fill=fills[c], stroke=c, rx=10, shadow=True))
        s.append(badge(x + bw / 2, y0 - 2, i + 1, r=14, fill=c, size=12.5))
        s.append(mtext(x + bw / 2, y0 + bh / 2 + 6, st.split("\n"), size=12, fill=NAVY, weight=700, lh=16))
        if i < len(steps) - 1:
            s.append(text(x + bw + gap / 2, y0 + bh / 2 + 6, "›", size=20, fill="#8ea6c0", weight=700))
    xloop = x0 + 6 * (bw + gap) + bw / 2
    xback = x0 + 3 * (bw + gap) + bw / 2
    s.append(path("M%s %s V%s H%s V%s" % (xloop, y0 + bh, y0 + bh + 42, xback, y0 + bh + 6),
                  color=RED_B, sw=2.4, dash="7 5"))
    s.append(text(x0 + 4.5 * (bw + gap), y0 + bh + 62,
                  "deviation not cleared → correct, then re-compare", size=11.5, fill=RED_B, weight=700))
    s.append(rect(60, 340, 640, 210, fill="#ffffff", stroke=GREY_B, rx=12, shadow=True))
    s.append(text(84, 372, "CLASSIFYING A FAILURE", size=11.5, fill=BLUE, weight=800, anchor="start", spacing="1.1"))
    rows = [("Working before, failing now", "Migration-related → owning team corrects and retests"),
            ("Failing before, failing now", "Pre-existing condition → document it, do not absorb it"),
            ("Failing before, working now", "Improvement → record it so it is not rolled back later"),
            ("No baseline evidence exists", "Escalate: you cannot classify what you cannot prove")]
    for i, (a, b) in enumerate(rows):
        y = 394 + i * 36
        s.append(rect(84, y, 250, 30, fill=SKY, stroke=SKY_B, rx=6))
        s.append(text(209, y + 20, a, size=11.3, fill=NAVY, weight=700))
        s.append(text(350, y + 20, b, size=11.3, fill=BODY, weight=500, anchor="start"))
    s.append(callout(740, 340, 640, 210, "EVIDENCE HYGIENE",
                     ["Name files so SID, check, phase and date are obvious without opening them.",
                      "Capture full output, not a cropped success line — context makes it defensible.",
                      "Attach evidence to the change/Jira record at the gate it supports, not at the end.",
                      "Store it per project retention and data-handling rules.",
                      "Source and target evidence must be comparable: same check, scope and tooling."],
                     size=12, lh=26, bullet=True))
    s.append("</svg>")
    return "".join(s)


ALL = {
    "d1-lifecycle": ("Figure 1 — End-to-end SAP-to-AWS migration lifecycle", d1_lifecycle),
    "d2-responsibility": ("Figure 2 — Responsibility split across the migration lifecycle", d2_raci),
    "d3-aws-architecture": ("Figure 3 — Target AWS reference architecture", d3_aws),
    "d4-hana-mdc": ("Figure 4 — HANA MDC, S3 backup backend and recovery flow", d4_hana),
    "d5-oracle-dataguard": ("Figure 5 — Oracle Data Guard switchover sequence", d5_oracle),
    "d6-cutover": ("Figure 6 — Cutover sequence, Go/No-Go and rollback", d6_cutover),
    "d7-performance": ("Figure 7 — Performance monitoring and troubleshooting path", d7_perf),
    "d8-evidence": ("Figure 8 — Evidence lifecycle", d8_evidence),
}


def write_standalone(outdir):
    os.makedirs(outdir, exist_ok=True)
    for slug, (label, fn) in ALL.items():
        body = fn()
        doc = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
               "<title>%s</title><style>body{margin:0;padding:24px;background:#fff}</style></head>"
               "<body>%s</body></html>" % (label, body))
        with open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8") as fh:
            fh.write(doc)
        with open(os.path.join(outdir, slug + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(body)
    return list(ALL)


if __name__ == "__main__":
    import sys
    print("\n".join(write_standalone(sys.argv[1] if len(sys.argv) > 1 else ".")))
