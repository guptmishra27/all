"""Native Word diagrams used by the DOCX build.

Word cannot embed the handbook's inline SVG, so each figure is re-expressed as a
styled, fully editable table composition. Every function returns a list of
"draw ops" consumed by md2docx.py:

  ("title", text)
  ("sub", text)
  ("band", text, fill_hex)                full-width coloured banner
  ("table", headers, rows, widths, fills) shaded grid (None = no header row)
  ("flow", [steps])                       arrow strip
  ("note", text)
  ("gap",)
"""

from __future__ import annotations

NAVY = "0F2B4C"
BLUE = "1B4F86"
SKY = "E8F0FB"
GREEN = "E6F4EA"
GREEN_D = "123B2A"
AMBER = "FDF3D8"
RED = "FDECEC"
GREY = "F3F5F9"
WHITE = "FFFFFF"


def title(t):
    return ("title", t)


def sub(t):
    return ("sub", t)


def band(t, fill=NAVY, color=WHITE):
    return ("band", t, fill, color)


def gap():
    return ("gap",)


def note(t):
    return ("note", t)


def flow(steps):
    return ("flow", steps)


def grid(headers, rows, widths=None, fills=None):
    return ("table", headers, rows, widths, fills)


# --------------------------------------------------------------------------- #
def fig1():
    stages = [
        ("1  Scope & Preparation", "Confirm scope, systems, access, AWS account, customer expectations", SKY),
        ("2  Discovery & Baseline", "Source configuration, interfaces, workload, dependencies, inventory, evidence", SKY),
        ("3  Sizing & Architecture", "Consume approved sizing; confirm target AWS architecture, HA/DR, connectivity", SKY),
        ("4  Build Sheet", "Prepare, peer review, finalise with customer; input for provisioning", SKY),
        ("5  AWS Build", "Provision via automation; validate VPC, subnets, DNS, storage, resources", SKY),
        ("6  SAP / DB Build", "Install and configure SAP and database; validate target readiness", SKY),
        ("7  Pre-Cutover Validation  [GATE 1]", "Source/target comparison, backup-recovery testing, readiness checks", AMBER),
        ("8  Cutover", "Shutdown, switchover or recovery, network updates, technical validation", AMBER),
        ("9  Go / No-Go  [GATE 2]", "Evidence, approvals, functional results, rollback readiness", RED),
        ("10  Go-Live & Hypercare  [GATE 3]", "Unlock users, resume jobs, monitor, resolve migration-related issues", GREEN),
    ]
    ops = [title("Figure 1 — End-to-end SAP-to-AWS migration lifecycle"),
           sub("Ten sequential stages. Amber and red stages are formal decision gates: work does not advance "
               "without evidence and approval."),
           grid(["Stage", "Purpose"], [[a, b] for a, b, _ in stages], widths=[34, 66],
                fills=[[c, WHITE] for _, _, c in stages]),
           gap(),
           flow(["Scope", "Discovery", "Inventory", "Dependencies", "Sizing", "Architecture",
                 "Build", "Validation", "Migration", "Handover"]),
           note("Sequence to remember. Skipping discovery, dependencies or validation converts a planned "
                "risk into an unplanned incident.")]
    return ops


def fig2():
    phases = ["Discovery & Baseline", "Build Sheet & AWS Build", "SAP / DB Build",
              "Pre-Cutover Validation", "Cutover Window", "Go / No-Go", "Hypercare"]
    lanes = [
        ("Automation / Cloud", ["R", "A/R", "C", "R", "C", "I", "C"]),
        ("Basis / Migration", ["A/R", "A", "A/R", "A/R", "A/R", "R", "A/R"]),
        ("DBA", ["C", "C", "R", "R", "A/R", "R", "R"]),
        ("Linux / OS", ["C", "R", "R", "R", "R", "I", "C"]),
        ("Network / DNS / IPAM", ["C", "R", "C", "C", "R", "I", "C"]),
        ("Security / AD", ["C", "C", "C", "R", "R", "C", "C"]),
        ("Application / Functional", ["I", "I", "C", "R", "C", "A/R", "R"]),
        ("PMO / Stakeholders", ["I", "C", "I", "C", "I", "A", "A"]),
    ]
    fills = {"A": RED, "R": SKY, "C": GREY, "I": WHITE}
    rows = []
    rowfills = []
    for name, marks in lanes:
        rows.append([name] + marks)
        rowfills.append([WHITE] + [fills[m[0]] for m in marks])
    ops = [title("Figure 2 — Responsibility split across the migration lifecycle"),
           sub("A = Accountable (single owner), R = Responsible (does the work), C = Consulted, I = Informed. "
               "Every activity needs exactly one A."),
           grid(["Team"] + phases, rows, widths=[18] + [12] * 7, fills=rowfills),
           gap(),
           band("OWNERSHIP PRINCIPLE"),
           grid(None, [["One accountable owner per assigned SID/system, with a named guide/support person and "
                         "controlled change. Multiple engineers must not independently modify the same assigned "
                         "system — that is how conflicting changes and unclear accountability enter a migration."]],
                widths=[100], fills=[[AMBER]])]
    return ops


def fig3():
    ops = [title("Figure 3 — Target AWS reference architecture"),
           sub("Training reference only. Region, AZ count, instance types, storage classes, HA design and "
               "connectivity always come from the approved sizing report and build sheet — never from a diagram."),
           band("AWS REGION  ·  Route 53 hosted zone + resolver rules", BLUE),
           grid(["Availability Zone A — app subnet", "Availability Zone A — DB subnet",
                 "Availability Zone B — app subnet", "Availability Zone B — standby"],
                [["ASCS · ERS/CRS · PAS\n(+ AAS per sizing)",
                  "SAP HANA (MDC) or Oracle DB\nprimary on a certified EC2 storage class",
                  "AAS · SAProuter/bastion · Web Dispatcher",
                  "HANA System Replication or Oracle Data Guard standby\n(broker + observer where designed)"]],
                widths=[25, 25, 25, 25], fills=[[SKY, GREEN, SKY, GREEN]]),
           gap(),
           grid(["Shared / managed services", "Role in the migration"],
                [["Amazon S3", "HANA backup via Backint; Oracle backup and packages"],
                 ["Amazon EFS", "NFS replacement for shared and interface directories"],
                 ["Route 53", "Private zones, records and the CNAME flip at cutover"],
                 ["EC2 snapshots", "Rollback recovery point taken before switchover"],
                 ["AWS KMS", "Encryption keys for storage, backups and snapshots"],
                 ["Connectivity", "Source landscape: on-prem SAP, external agents (Control-M, NetBackup, "
                                  "OEM/OBM), interfaces, SSO, NFS"]],
                widths=[28, 72]),
           gap(),
           band("VALIDATE, DON'T ASSUME", "8A6410", AMBER),
           grid(None, [["VPC, AZs, subnets, free IPs  ·  DNS and Route 53 resolution  ·  S3 bucket, folders, "
                         "policies  ·  read/write and backend connectivity  ·  CMDB CI, relationship, status  ·  "
                         "details match the build sheet"]], widths=[100], fills=[[AMBER]]),
           note("This is a teaching reference, not an approved architecture artefact.")]
    return ops


def fig4():
    ops = [title("Figure 4 — SAP HANA MDC architecture, S3 backup backend and recovery flow"),
           sub("SystemDB and TenantDB are database containers inside one HANA system. They are not an HA design: "
               "high availability is a separate infrastructure-level decision (HSR, cluster, storage)."),
           grid(["Three-tier validation (bottom-up)", "HANA host — one EC2 instance / VM (or an HSR pair)",
                 "Backup backend"],
                [["3  UI / presentation layer\nSAP GUI, Fiori, browser\n\n2  Application layer\nPAS / AAS work processes\n\n"
                  "1  Database layer\nHANA SystemDB + TenantDB\n\nRecovery order: database first, then start and "
                  "validate the application servers.",
                  "SystemDB (SYSTEMDB)\nCentral management and monitoring; own login context and credentials "
                  "(SYSTEM user); holds the backup catalogue for all tenants.\n\nTenantDB (for example PRD)\n"
                  "Application and data workload; own login context and credentials; own backup configuration "
                  "and data volume.\n\nServices: nameserver (SystemDB), indexserver (per tenant).",
                  "Amazon S3 bucket\nBackint agent or file-based backup; bucket and folders, read/write policy, "
                  "connectivity from the HANA host.\n\nPre-checks: sizing, shared file system, INI files, S3 "
                  "backend, DB server status, THP, kernel and HANA version, global INI, index/name server, "
                  "evidence."]],
                widths=[30, 40, 30], fills=[[SKY, GREEN, SKY]]),
           gap(),
           band("RECOVERY FLOW", BLUE),
           flow(["Source backup", "Configuration file", "S3 backend", "Target configuration", "Recovery", "Validation"]),
           gap(),
           band("CUTOVER RULE", "8A6410", AMBER),
           grid(None, [["Test backup and recovery BEFORE cutover. During cutover take the final backup, validate it, "
                         "and only then stop the source system. The source stays available until the required final "
                         "backup activity completes successfully — that backup is also your rollback anchor."]],
                widths=[100], fills=[[AMBER]])]
    return ops


def fig5():
    ops = [title("Figure 5 — Oracle Data Guard migration: switchover, SCN synchronisation and rollback"),
           sub("A switchover is a planned, reversible role swap. A failover is disaster recovery and is not "
               "reversible in the same way. This module covers the planned switchover only."),
           grid(["SOURCE — on-premises / source DC", "TARGET — AWS"],
                [["PRIMARY\nOpen and serving SAP; generates archive/redo.\n\nAFTER SWITCHOVER\nShut down after "
                  "final validation and snapshot.\n\nSCN source: SELECT current_scn FROM v$database;",
                  "STANDBY\nManaged recovery applying redo shipped from source.\n\nNEW PRIMARY\nActivated and "
                  "opened after switchover.\n\nSCN target — values must match before switchover."]],
                widths=[50, 50], fills=[[RED, GREEN]]),
           grid(None, [["Redo transport: source primary → target standby  ·  apply / gap check in the reverse "
                         "direction  ·  apply lag must be zero (or within the agreed tolerance) at the moment of change"]],
                widths=[100], fills=[[SKY]]),
           gap(),
           grid(["#", "Step", "Detail"],
                [["1", "Pre-checks", "Listener and SQL*Net, Data Guard parameters, SID settings, Broker, observer node, patch alignment"],
                 ["2", "Synchronisation review", "Log switching reviewed, apply lag checked, source and target SCN compared"],
                 ["3", "Evidence + approval", "Outputs attached to the Jira/change ticket; approval before production changes"],
                 ["4", "Snapshot", "AWS disk-level snapshot of the target — the rollback recovery point"],
                 ["5", "Shutdown source", "Application shutdown complete and DBA handover confirmed; source primary closed"],
                 ["6", "Switchover / activate", "Target standby activated and opened as the new primary database"],
                 ["7", "Post-validation", "New primary validated; DBVERIFY for block corruption; RMAN backup; OEM agent verified"],
                 ["8", "DNS / IPAM", "Virtual hostname unchanged, target IP updated, CNAME repointed, stale host entries cleaned"]],
                widths=[5, 24, 71],
                fills=[[WHITE, WHITE, WHITE], [WHITE, WHITE, WHITE], [WHITE, WHITE, WHITE],
                       [WHITE, AMBER, WHITE], [WHITE, WHITE, WHITE], [WHITE, WHITE, WHITE],
                       [WHITE, GREEN, WHITE], [WHITE, WHITE, WHITE]]),
           gap(),
           grid(["Rollback path", "Validation gate"],
                [["Restore target volumes from the pre-switchover snapshot, revert DNS/CNAME to the source, restart "
                  "the source primary. Rollback readiness is maintained until the migration is declared safe.",
                  "DBVERIFY clean (no corrupted blocks) → RMAN backup successful → OEM agent reporting. Only then "
                  "is the new primary considered technically accepted."]],
                widths=[50, 50], fills=[[RED, AMBER]]),
           note("Command-level detail (DGMGRL versus ALTER DATABASE SWITCHOVER, Broker configuration, observer "
                "placement) is defined in the project runbook, not in this handbook.")]
    return ops


def fig6():
    ops = [title("Figure 6 — Cutover execution sequence with Go/No-Go decision and rollback path"),
           sub("Each lane hands over explicitly. Nothing starts before the previous lane confirms completion and "
               "the evidence is attached to the change record."),
           grid(["APPLICATION", "DBA", "BASIS / MIGRATION", "FUNCTIONAL + PMO"],
                [["1  Cooldown / ramp-up complete\n2  Application + web services stopped\n3  Handover to DBA confirmed",
                  "4  Final backup + AWS snapshot\n5  Switchover or HANA recovery\n6  DBVERIFY, RMAN, DB validation",
                  "7  rsync global directory; clean host/IPAM\n8  Profile parameters, kernel permissions, root scripts\n"
                  "9  R3trans -d must return 0000\n10  Start SAP; validate SNC/SSO, Gateway, RFC",
                  "11  Business transaction tests, interfaces, printers, evidence"]],
                widths=[25, 25, 30, 20], fills=[[GREY, GREEN, SKY, AMBER]]),
           gap(),
           band("GO / NO-GO — technical + functional + owner sign-off", "8A6410", AMBER),
           grid(["If GO", "If NO-GO"],
                [["Unlock users · resume background jobs and Control-M · complete EDG / SAProuter configuration · "
                  "15 days of hypercare · classify each issue as migration-related or pre-existing and route it to "
                  "the owning team.",
                  "Execute the agreed rollback procedure: restore the snapshot or recover the source, revert "
                  "DNS/CNAME, restart the source, re-open the incident path. Record the reason and the evidence "
                  "for the No-Go."]],
                widths=[50, 50], fills=[[GREEN, RED]]),
           note("A No-Go with documented reasons is a successful use of the gate.")]
    return ops


def fig7():
    ops = [title("Figure 7 — Performance monitoring, memory escalation and troubleshooting path"),
           sub("Top-down triage: workload statistics first, individual records second, memory and buffer behaviour "
               "third, root cause before any parameter change."),
           grid(["ST02 — SAP memory escalation", "Troubleshooting path"],
                [["Roll area / roll memory — per work process, rolled-out user context\n"
                  "↓\nExtended memory (EM) — shared pool used first for user context\n"
                  "↓  (when EM is exhausted)\nHeap / private memory — process mode becomes PRIVATE\n↓\n"
                  "Paging and swaps — paging memory, roll-in/roll-out activity\n\n"
                  "Buffer memory — program, single record, table, export/import buffers; watch utilisation and hit ratio",
                  "1  Symptom reported — slow dialog, timeout, batch overrun, complaint\n"
                  "2  ST03/ST03N workload — response, DB, CPU, wait; daily/weekly/monthly\n"
                  "3  STAD detailed records — the specific slow steps and users\n"
                  "4  Classify the bottleneck — high DB time → database/SQL/network; high CPU → ABAP/app; "
                  "high wait → memory, enqueue, RFC\n5  ST02 memory and buffers\n"
                  "6  Find the root cause — index, access path, custom code, parameter, volume, infrastructure\n"
                  "7  Fix with the owning team — parameter change via RZ10 (persistent) or RZ11 (dynamic)\n"
                  "8  Re-baseline and attach before/after evidence"]],
                widths=[42, 58], fills=[[SKY, WHITE]]),
           gap(),
           grid(["RZ10", "RZ11"],
                [["Persistent profile parameter. Import and activate; a restart is required for many parameters. "
                  "Use when the change must survive a restart.",
                  "Dynamic/temporary change where the parameter supports it. Not a permanent configuration change; "
                  "mirror it in RZ10 or it disappears at the next restart."]],
                widths=[50, 50], fills=[[SKY, GREY]]),
           gap(),
           band("THRESHOLD CAUTION", "8A6410", AMBER),
           grid(None, [["The source training quoted ≈1200 ms response time and ≈40% average database request time as "
                         "discussion values. Validate them against the applicable SAP and client baseline before using "
                         "them as production alerting thresholds. Never raise a memory parameter before identifying what "
                         "is consuming the memory."]], widths=[100], fills=[[AMBER]]),
           note("ST03N is the current workload transaction; ST03 is retained because the source material and many "
                "runbooks still reference it. STAD reads the statistical records behind the workload.")]
    return ops


def fig8():
    ops = [title("Figure 8 — Evidence lifecycle: baseline, compare, correct, retest, handover"),
           sub("Working before migration should work after migration. Evidence is what turns that principle into "
               "something you can actually prove."),
           flow(["1 Capture source baseline", "2 Execute migration/cutover", "3 Capture target evidence",
                 "4 Compare source vs target", "5 Identify deviations", "6 Correct with the responsible team",
                 "7 Retest the check", "8 Capture final evidence", "9 Complete handover"]),
           note("Deviation not cleared → correct, then return to step 4 and re-compare."),
           gap(),
           grid(["Classifying a failure", "Action"],
                [["Working before, failing now", "Migration-related → owning team corrects and retests"],
                 ["Failing before, failing now", "Pre-existing condition → document it, do not absorb it as a defect"],
                 ["Failing before, working now", "Improvement → record it so it is not rolled back later"],
                 ["No baseline evidence exists", "Escalate: you cannot classify what you cannot prove"]],
                widths=[34, 66], fills=[[SKY, WHITE], [WHITE, WHITE], [SKY, WHITE], [RED, WHITE]]),
           gap(),
           band("EVIDENCE HYGIENE", "8A6410", AMBER),
           grid(None, [["Name files so SID, check, phase and date are obvious without opening them.  ·  Capture full "
                         "output, not a cropped success line.  ·  Attach evidence to the change/Jira record at the gate "
                         "it supports.  ·  Store per project retention and data-handling rules.  ·  Source and target "
                         "evidence must be comparable: same check, scope and tooling."]],
                widths=[100], fills=[[AMBER]])]
    return ops


FIGS = {"d1-lifecycle": fig1, "d2-responsibility": fig2, "d3-aws-architecture": fig3,
        "d4-hana-mdc": fig4, "d5-oracle-dataguard": fig5, "d6-cutover": fig6,
        "d7-performance": fig7, "d8-evidence": fig8}
