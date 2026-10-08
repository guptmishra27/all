"""Handbook content, part 1: front matter, sections 1-6."""

from htmlkit import (box, bullets, cards, checklist, cmd, e, figure, flow, h3, kpis,
                     para, pill, qa, section, steps, table)

FIG = {}  # slug -> svg, injected by build_handbook.py


# --------------------------------------------------------------------------- #
def cover():
    ctl = [
        ("Document title", "SAP Migration Training Handbook"),
        ("Document ID", "SAP-MIG-TRN-HB-001"),
        ("Version", "1.0 — vetted release"),
        ("Status", "Issued for training delivery"),
        ("Document type", "Consolidated training &amp; knowledge-transfer handbook"),
        ("Training scope", "SAP migration planning, build readiness, validation, troubleshooting, cutover"),
        ("Training period", "September – October 2026"),
        ("Primary trainer", "Amit Prajapati"),
        ("Prepared from", "Consolidated training / MOM source document"),
        ("Applies to", "SAP → AWS migrations on SAP HANA and Oracle, including Basis validation, cutover and hypercare"),
        ("Classification", "Internal — project and training use"),
        ("Retention", "Per programme record-retention standard"),
    ]
    cells = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(k), v) for k, v in ctl)
    tags = ["SAP → AWS Migration", "SAP HANA MDC", "Oracle Data Guard", "Basis Validation",
            "Cutover &amp; Go/No-Go", "Hypercare", "Evidence Model"]
    return f"""
<header class="cover" id="top">
  <div class="eyebrow">CONSOLIDATED TRAINING MATERIAL · 2026</div>
  <h1>SAP Migration<br>Training Handbook</h1>
  <p class="lede">A single, evidence-driven reference for engineers executing SAP-to-AWS migrations: preparation and source
  baselining, target architecture and AWS build validation, SAP HANA MDC backup and recovery, Basis post-migration validation,
  performance troubleshooting, Oracle Data Guard switchover, cutover, Go/No-Go governance, rollback and hypercare.</p>
  <div class="tags">{''.join('<span>%s</span>' % t for t in tags)}</div>
  <div class="rule"></div>
  <dl class="docctl">{cells}</dl>
  <p class="stamp"><b>Source basis.</b> This handbook consolidates the supplied training/MOM material. It preserves the source
  terminology and practical guidance, and it does not replace approved project runbooks, architecture baselines or
  change-management procedures. Where the source material was ambiguous or client-specific, the item is flagged rather than
  silently rewritten — see <a href="#app-d" style="color:#9fc4ea">Appendix D: Technical review and vetting notes</a>.</p>
</header>
<div class="topbar no-print">
  <span class="dot"></span>
  <span><b>SAP Migration Training Handbook</b> · v1.0 · Internal</span>
  <span class="sp"></span>
  <button class="btn" data-expand="1" data-scope="body">Expand all answers</button>
  <button class="btn" data-expand="0" data-scope="body">Collapse</button>
  <button class="btn primary" data-print="1">Print / save as PDF</button>
</div>
"""


# --------------------------------------------------------------------------- #
def rail(sections):
    groups = [("Front matter", 0), ("Core handbook", 4), ("Modules", 7), ("Reference", 15), ("Appendices", 21)]
    out = ['<aside class="rail"><div class="brand">TRAINING HANDBOOK</div>',
           '<div class="ttl">SAP Migration</div>',
           '<div class="subttl">SAP → AWS · HANA · Oracle · Basis validation · Cutover · Hypercare</div>',
           '<div class="prog"><i></i></div><div class="progtxt"></div>', "<nav>"]
    gi = 0
    for i, (num, sid, label) in enumerate(sections):
        if gi < len(groups) and i == groups[gi][1]:
            out.append('<div class="grp">%s</div>' % e(groups[gi][0]))
            gi += 1
        out.append('<a href="#%s"><span class="n">%s</span><span>%s</span></a>' % (e(sid), e(num), e(label)))
    out.append('</nav><div class="railfoot">Version 1.0 · Sept–Oct 2026<br>Primary trainer: Amit Prajapati<br>'
               'Internal — training use</div></aside>')
    return "".join(out)


# --------------------------------------------------------------------------- #
def s_howto():
    out = [section("howto", "—", "How to use this handbook", kick="Front matter",
                   lead="This is a working document, not a read-once handout. Use it to prepare for a migration, to run a "
                        "training session, and as the index that points you to the right project runbook at cutover.")]
    out.append(h3("0.1", "Reading paths by role"))
    out.append(table(
        ["Role", "Read first", "Then", "Use at cutover"],
        [["Basis / migration engineer", "Sections 1–3, Modules 1–4", "Modules 5, 7 and Section 15", "Sections 10, 12, 16"],
         ["DBA (Oracle / HANA)", "Section 3, Module 3", "Module 6", "Sections 10, 12.3, 12.5"],
         ["Automation / cloud engineer", "Section 3, Module 2", "Section 14", "Section 10.2"],
         ["Linux / OS engineer", "Module 1, Section 7.2", "Section 14", "Sections 10, 12.1"],
         ["Network / DNS / IPAM", "Module 1, Section 9.5", "Module 2", "Section 10.2"],
         ["Application / functional lead", "Sections 1–3, Module 7", "Sections 13, 14", "Sections 10.4, 10.6"],
         ["Project manager / stakeholder", "Sections 1–3", "Sections 13, 14, 16", "Section 10.5"]],
        caption="Suggested reading order", widths=["22%", "26%", "26%", "26%"]))
    out.append(h3("0.2", "Conventions used in this handbook"))
    out.append(table(
        ["Convention", "Meaning"],
        [[pill("MUST") + " " + pill("Gate", "r"), "Mandatory step or formal gate. Work does not proceed without it and without recorded evidence."],
         [pill("SHOULD", "g"), "Strongly recommended practice. Deviation needs a recorded reason and the accountable owner's agreement."],
         [pill("MAY", "n"), "Optional, context-dependent, or dependent on the customer's design."],
         [pill("Source term", "a"), "Terminology taken verbatim from the supplied training/MOM material. It may be client-specific — confirm it against the project standard before use."],
         [pill("Validate", "r"), "Assumption from the source material that must be verified against the applicable SAP, AWS or client baseline before it is relied on."]],
        caption="Legend", widths=["24%", "76%"], cls="plain"))
    out.append(h3("0.3", "Checklist behaviour"))
    out.append(bullets([
        "Every checklist in Section 12 is interactive: tick a check, choose a status and add an evidence reference. Progress is saved in your browser (local storage only — nothing leaves the device).",
        "Checklists are training and readiness aids. The authoritative record is the project's validation workbook or change ticket; transfer your results there before sign-off.",
        'Use <b>Print / save as PDF</b> to produce a static copy. Printing expands all knowledge-check answers and renders each section on its own page.',
        "Figures are vector diagrams. They can be lifted from <code>assets/</code> as standalone SVG files for slides or runbooks."]))
    out.append(box("warn", "Scope limitation",
                   para("This handbook teaches the method and the checks. It is not a runbook, not an approved architecture, and not "
                        "a substitute for the customer's change-management process. Command syntax, parameter names, thresholds and "
                        "instance types must always be taken from the approved project documentation for the specific system, release "
                        "and landscape you are working on.")))
    out.append("</section>")
    return "".join(out)


def s_fm():
    out = [section("fm", "—", "Document control, revision history and approval", kick="Front matter", cls="nobreak")]
    out.append(h3("0.4", "Revision history"))
    out.append(table(
        ["Version", "Date", "Author / editor", "Description of change", "Reviewed by", "Status"],
        [["0.1", "Sep 2026", "Amit Prajapati", "Initial consolidation of training sessions and MOM notes into a single draft.", "—", "Draft"],
         ["0.2", "Sep 2026", "Amit Prajapati", "Modules reorganised into the migration lifecycle; checklists and evidence model added.", "Delivery team", "Draft"],
         ["0.9", "Oct 2026", "Amit Prajapati", "Figures 1–8 added; source terminology cross-checked; open items flagged.", "Basis + DBA leads", "In review"],
         ["1.0", "Oct 2026", "Amit Prajapati", "Professional review and vetting pass: technical corrections, glossary, troubleshooting playbook, Appendix D review notes.", "Programme lead", "Issued"]],
        caption="Revision history", widths=["8%", "10%", "17%", "41%", "13%", "11%"]))
    out.append(h3("0.5", "Approval and distribution"))
    out.append(table(
        ["Role", "Name", "Responsibility for this document", "Signature", "Date"],
        [["Primary trainer / author", "Amit Prajapati", "Content accuracy, delivery, consolidation of MOM material", "", ""],
         ["Technical reviewer — Basis", "", "SAP validation, monitoring and cutover content", "", ""],
         ["Technical reviewer — DBA", "", "Oracle Data Guard and HANA backup/recovery content", "", ""],
         ["Programme / project manager", "", "Approval, distribution list, version control", "", ""],
         ["Client system owner (per SID)", "", "Confirmation that the material matches the approved landscape", "", ""]],
        caption="Approval record", widths=["22%", "16%", "38%", "14%", "10%"], cls="plain"))
    out.append(table(
        ["Distribution", "Purpose"],
        [["Migration / Basis delivery team", "Primary audience — training and execution reference"],
         ["DBA, Linux, network, security and automation teams", "Interface and responsibility clarity"],
         ["Application / functional leads", "Validation and Go/No-Go participation"],
         ["PMO and stakeholders", "Governance, approvals and hypercare oversight"],
         ["New joiners to the programme", "Onboarding and knowledge transfer"]],
        caption="Intended distribution", widths=["42%", "58%"], cls="plain"))
    out.append(box("key", "Disclaimer",
                   para("SAP, SAP HANA, ABAP, NetWeaver and the transaction codes referenced here are trademarks of SAP SE. "
                        "AWS, Amazon S3, Amazon EFS, Route 53 and EC2 are trademarks of Amazon.com, Inc. or its affiliates. "
                        "Oracle is a trademark of Oracle Corporation. Other product names (Control-M, NetBackup, Chef, ServiceNow, "
                        "webMethods, MuleSoft) belong to their respective owners.",
                        "This handbook is internal training material. It carries no warranty for production use, and every technical "
                        "value it quotes must be validated against the applicable vendor documentation, SAP Note, and the customer's "
                        "approved design before being applied to a live system.")))
    out.append("</section>")
    return "".join(out)


def s_toc():
    out = [section("toc", "—", "Contents and figure index", kick="Front matter", cls="nobreak")]
    out.append('<div class="grid g2">')
    left = [("1", "Executive training overview", "#overview"), ("2", "Training objectives and learning outcomes", "#objectives"),
            ("3", "End-to-end SAP-to-AWS migration lifecycle", "#lifecycle"),
            ("4", "Module 1 — Preparation, discovery and source baseline", "#m1"),
            ("5", "Module 2 — Target architecture, AWS readiness and build", "#m2"),
            ("6", "Module 3 — SAP HANA MDC, backup and recovery", "#m3"),
            ("7", "Module 4 — SAP post-migration validation", "#m4"),
            ("8", "Module 5 — Performance monitoring and troubleshooting", "#m5")]
    right = [("9", "Module 6 — Oracle database migration and switchover", "#m6"),
             ("10", "Module 7 — Cutover, Go/No-Go, rollback and hypercare", "#m7"),
             ("11", "SAP transaction and technology quick reference", "#tcode"),
             ("12", "Consolidated validation checklists", "#checklists"),
             ("13", "Evidence and documentation strategy", "#evidence"),
             ("14", "Ownership and operating model", "#ownership"),
             ("15", "Troubleshooting playbook and common failure modes", "#playbook"),
             ("16", "Key lessons and practical guidance", "#lessons"),
             ("17", "Final knowledge check", "#quiz"),
             ("A–E", "Appendices: source coverage, completion record, glossary, review notes", "#app-a")]
    for items in (left, right):
        out.append("<div>")
        for n, t, href in items:
            out.append('<p style="margin:0 0 9px;display:flex;gap:12px;align-items:baseline">'
                       '<b style="color:var(--blue);min-width:34px;font-variant-numeric:tabular-nums">%s</b>'
                       '<a href="%s" style="color:var(--ink);font-weight:600">%s</a></p>' % (e(n), href, e(t)))
        out.append("</div>")
    out.append("</div>")
    out.append(h3("Figures"))
    out.append(table(["#", "Figure", "Section"],
                     [["1", '<a href="#fig-d1-lifecycle">End-to-end SAP-to-AWS migration lifecycle</a>', "3"],
                      ["2", '<a href="#fig-d2-responsibility">Responsibility split across the migration lifecycle</a>', "5.4"],
                      ["3", '<a href="#fig-d3-aws-architecture">Target AWS reference architecture</a>', "5.1"],
                      ["4", '<a href="#fig-d4-hana-mdc">HANA MDC architecture, S3 backup backend and recovery flow</a>', "6"],
                      ["5", '<a href="#fig-d5-oracle-dataguard">Oracle Data Guard switchover, SCN synchronisation and rollback</a>', "9"],
                      ["6", '<a href="#fig-d6-cutover">Cutover execution sequence with Go/No-Go and rollback</a>', "10"],
                      ["7", '<a href="#fig-d7-performance">Performance monitoring, memory escalation and troubleshooting path</a>', "8"],
                      ["8", '<a href="#fig-d8-evidence">Evidence lifecycle</a>', "13"]],
                     caption="Figure index", widths=["6%", "74%", "20%"], cls="plain"))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s1_overview():
    out = [section("overview", "1", "Executive training overview", kick="Section 1",
                   lead="The consolidated training focused on the practical execution of SAP migration activities, with emphasis "
                        "on moving SAP workloads to AWS and validating the target environment. Sessions covered discovery, source "
                        "baselining, sizing, architecture, AWS infrastructure readiness, SAP/HANA and Oracle considerations, "
                        "post-migration validation, monitoring, troubleshooting, cutover, rollback, go-live and hypercare.")]
    out.append(kpis([("10", "lifecycle stages", "Scope through to hypercare, each with entry and exit criteria"),
                     ("8", "vector figures", "Architecture, flows, decision gates and troubleshooting paths"),
                     ("5", "live checklists", "OS, SAP, database, performance and cutover readiness"),
                     ("15", "days of hypercare", "Stated post-go-live support period in the source training")]))
    out.append(box("key", "Core operating principle",
                   para("A migration is not simply a technical copy. The process begins with scope, discovery, inventory and "
                        "dependency analysis, followed by sizing, architecture, build, validation, migration and controlled handover. "
                        "Every stage produces evidence that the next stage consumes.")))
    out.append(box("ok", "Baseline principle",
                   para("<b>Working before migration should work after migration.</b> If something was already failing before "
                        "migration, it is documented as a pre-existing condition — not absorbed as a migration defect, and not "
                        "quietly fixed without a record.")))
    out.append(h3("1.1", "Training coverage at a glance"))
    out.append(table(["Area", "Training focus", "Where it is covered"],
                     [["Preparation", "Scope, access, CMDB, IP analysis, source parameters", "Module 1 (Section 4)"],
                      ["Discovery", "Sizing, workload, interfaces, external agents, NFS, AL11", "Module 1 (Section 4)"],
                      ["Target readiness", "AWS account, VPC, subnets, DNS, S3, build sheet", "Module 2 (Section 5)"],
                      ["SAP / HANA", "MDC, SystemDB/TenantDB, backup, recovery, HA", "Module 3 (Section 6)"],
                      ["SAP validation", "OS, services, STMS, RFC, Gateway, SNC, certificates", "Module 4 (Section 7)"],
                      ["Performance", "ST02, ST03/ST03N, STAD, response-time analysis", "Module 5 (Section 8)"],
                      ["Oracle", "Data Guard, SCN, snapshots, DBVERIFY, RMAN", "Module 6 (Section 9)"],
                      ["Cutover", "Shutdown, switchover/recovery, validation, Go/No-Go", "Module 7 (Section 10)"],
                      ["After go-live", "Hypercare, evidence, issue classification and support", "Module 7 (Section 10)"]],
                     caption="Coverage map", widths=["18%", "52%", "30%"]))
    out.append(h3("1.2", "What good looks like at the end of a migration"))
    out.append(cards([
        ("Technically identical where it matters", "OS, SAP and database parameters, UIDs/GIDs, directories, interfaces and "
         "certificates match the approved target design — and every difference from source is explained, not discovered later."),
        ("Provably working", "Auto-start has been proven through a real reboot, backup and recovery have been tested, and RFC, "
         "Gateway, STMS, spool and SNC connectivity have each been exercised, not assumed."),
        ("Evidence at every gate", "Source and target evidence is captured, compared and attached to the change record before "
         "the next gate opens."),
        ("Clear accountability", "One owner per system, one guide per owner, and no uncoordinated parallel changes to the same SID."),
        ("Controlled handover", "Users unlocked, jobs and Control-M resumed with the owning teams, hypercare running, and issues "
         "classified against the pre-migration baseline."),
        ("Rollback still possible", "Until the migration is declared safe, the snapshot, source system and DNS rollback path remain "
         "available and tested.")], cols=3, accent=True))
    out.append("</section>")
    return "".join(out)


def s2_objectives():
    out = [section("objectives", "2", "Training objectives and learning outcomes", kick="Section 2",
                   lead="Ten objectives define what a trained engineer must be able to do. Each one maps to a module and to the "
                        "evidence that proves the skill in practice.")]
    objs = [
        ("Understand the end-to-end migration lifecycle and the dependency between phases.", "3", "Can explain why sizing precedes build, and why validation precedes cutover."),
        ("Build a reliable source baseline before migration so target validation is evidence-based.", "4", "Produces a source evidence pack with interfaces, directories and known failures recorded."),
        ("Understand the role of the approved build sheet and CMDB in target provisioning.", "5", "Reviews a build sheet, completes peer review, and validates the build against it."),
        ("Validate AWS infrastructure delivered by the automation team against approved requirements.", "5", "Checks VPC, subnets, IPs, DNS, S3 and permissions rather than accepting the automation output."),
        ("Understand HANA SystemDB/TenantDB architecture and the backup/recovery sequence.", "6", "Explains the container model, configures the backup destination and tests recovery."),
        ("Perform SAP Basis post-migration validation across OS, SAP, database, interfaces and security.", "7", "Completes all four validation domains and records deviations with owners."),
        ("Use core SAP transactions for structured validation and troubleshooting.", "8, 11", "Navigates ST02, ST03N, STAD, SM51, SM59, SMGW, SMICM, STMS, DB02, AL11, SPAD, RZ10/RZ11."),
        ("Understand Oracle Data Guard switchover, SCN synchronization, snapshot and rollback concepts.", "9", "Verifies synchronisation, confirms the rollback point, validates the new primary."),
        ("Execute a controlled cutover with evidence, approvals and Go/No-Go gates.", "10", "Runs the lane sequence, presents evidence at the gate, respects the decision."),
        ("Support post-go-live hypercare and distinguish migration-related issues from pre-existing issues.", "10, 13", "Classifies each ticket against the baseline and routes it to the owning team."),
    ]
    out.append(table(["#", "Learning objective", "Module", "Observable evidence of competence"],
                     [[str(i + 1), o, m, ev] for i, (o, m, ev) in enumerate(objs)],
                     caption="Training objectives", widths=["5%", "46%", "9%", "40%"]))
    out.append(box("key", "Expected capability after training",
                   para("A trained migration/Basis engineer should be able to take an approved migration package, understand the "
                        "source baseline, validate the target build, execute the defined technical checks, capture evidence, "
                        "identify deviations, coordinate with specialist teams, and support cutover and hypercare — without "
                        "bypassing the approved change and ownership model.")))
    out.append(h3("2.1", "Prerequisites assumed by this training"))
    out.append(bullets([
        "Working knowledge of SAP Basis administration in at least one landscape (start/stop, profiles, transports, monitoring).",
        "Basic Linux/Unix administration: file systems, permissions, services, users and groups, log inspection.",
        "Basic relational database concepts and, for Module 6, exposure to Oracle administration.",
        "Familiarity with cloud infrastructure concepts: accounts, networks, subnets, DNS, object and file storage.",
        "Ability to read a change record and work inside an approval and evidence process."]))
    out.append(h3("2.2", "How the modules build on each other"))
    out.append(flow(["Module 1 baseline", "Module 2 target build", "Module 3 HANA data",
                     "Module 4 SAP validation", "Module 5 performance", "Module 6 Oracle switchover",
                     "Module 7 cutover + hypercare"]))
    out.append(para("Modules 1 and 2 create the conditions for everything else: without a source baseline and a validated target, "
                    "the validation modules have nothing to compare against. Modules 3 to 6 are the technical depth, and Module 7 "
                    "is where that depth is exercised under time pressure with a decision gate at the end."))
    out.append("</section>")
    return "".join(out)


def s3_lifecycle():
    out = [section("lifecycle", "3", "End-to-end SAP-to-AWS migration lifecycle", kick="Section 3",
                   lead="Ten stages, three formal gates. The lifecycle is sequential by design: each stage consumes the evidence "
                        "produced by the one before it, and skipping a stage converts a planned risk into an unplanned incident.")]
    out.append(figure("d1-lifecycle", FIG["d1-lifecycle"],
                      "<b>Figure 1.</b> The migration lifecycle from scope to hypercare. Amber and red stages are decision gates — "
                      "stage 7 (pre-cutover validation), stage 9 (Go/No-Go) and stage 10 (release to hypercare). A gate does not open "
                      "on assertion; it opens on evidence and named approval."))
    out.append(h3("3.1", "Stage table with entry and exit criteria"))
    rows = [
        ["1", "Scope &amp; Preparation", "Confirm scope, systems, access, AWS account and customer expectations.",
         "Customer request and system list", "Signed scope, named systems, access granted, AWS account verified"],
        ["2", "Discovery &amp; Baseline", "Collect source configuration, interfaces, workload, dependencies, inventory and evidence.",
         "Scope and access", "Source baseline pack: parameters, interfaces, NFS, AL11, known failures"],
        ["3", "Sizing &amp; Architecture", "Consume approved sizing; confirm target AWS architecture, HA/DR and connectivity.",
         "Source baseline", "Approved sizing report and target architecture agreed with the customer"],
        ["4", "Build Sheet", "Finalise the technical input used for provisioning and customer review.",
         "Architecture agreement", "Peer-reviewed build sheet finalised with the customer"],
        ["5", "AWS Build", "Provision infrastructure through automation; validate VPC, subnets, DNS, storage and resources.",
         "Approved build sheet", "Validated infrastructure, CMDB CIs deployed and matching the inventory"],
        ["6", "SAP / DB Build", "Install and configure SAP and database components; validate target readiness.",
         "Validated infrastructure", "SAP and database installed, configured and reachable; pre-checks passed"],
        ["7", "Pre-Cutover Validation " + pill("GATE 1", "a"), "Complete source/target comparisons, backup/recovery testing and readiness checks.",
         "Target build complete", "All checklist items closed or formally deferred with an owner and a date"],
        ["8", "Cutover", "Execute shutdown, database migration/switchover or recovery, network updates and technical validation.",
         "Gate 1 approval and a booked window", "Target system technically validated; R3TRANS -d returns 0000; SAP started"],
        ["9", "Go / No-Go " + pill("GATE 2", "r"), "Review evidence, approvals, functional results and rollback readiness.",
         "Technical and functional evidence", "Recorded Go or No-Go decision with named approvers"],
        ["10", "Go-Live &amp; Hypercare " + pill("GATE 3", "g"), "Unlock users, resume jobs, monitor the system and resolve migration-related issues.",
         "Go decision", "System released, jobs resumed, hypercare running for 15 days, handover complete"],
    ]
    out.append(table(["#", "Stage", "Purpose", "Entry criteria", "Exit criteria / evidence"], rows,
                     caption="Lifecycle stage table", widths=["4%", "18%", "30%", "20%", "28%"]))
    out.append(box("warn", "The three gates",
                   bullets([
                       "<b>Gate 1 — Pre-cutover validation.</b> Nothing enters a cutover window with an untested backup/recovery path or an open critical checklist item.",
                       "<b>Gate 2 — Go/No-Go.</b> Technical, functional and system-owner sign-off plus confirmed rollback readiness. A No-Go is a successful outcome of this gate when the evidence does not support release.",
                       "<b>Gate 3 — Release to hypercare.</b> Users unlocked and jobs resumed only after the Go decision is recorded, with the hypercare roster and escalation path live."])))
    out.append(h3("3.2", "Sequence to remember"))
    out.append(flow(["Scope", "Discovery", "Inventory", "Dependencies", "Sizing", "Architecture",
                     "Build", "Validation", "Migration", "Handover"]))
    out.append(para("If a project is in trouble, it is almost always because one of these was skipped or compressed: discovery "
                    "(unknown interfaces and agents surface at cutover), dependencies (third-party credentials arrive late), or "
                    "validation (the target is assumed correct because automation produced it)."))
    out.append(h3("3.3", "Where each team enters the lifecycle"))
    out.append(figure("d2-responsibility", FIG["d2-responsibility"],
                      "<b>Figure 2.</b> Responsibility split. Read the matrix by row when you need to know what your team owns, and "
                      "by column when you need to know who to call at a given stage. Two teams can share work (A · R), but only one "
                      "can be accountable."))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s4_m1():
    out = [section("m1", "4", "Module 1 — Preparation, discovery and source baseline", cls="mod",
                   kick="Module 1 · Section 4",
                   lead="Everything validated later is validated against what is recorded here. A weak baseline produces a "
                        "cutover full of unanswerable questions; a strong baseline turns every deviation into a five-minute lookup.")]
    out.append(h3("4.1", "Preparation and discovery"))
    out.append(steps([
        "Finalise the migration scope with the customer, in writing.",
        "Identify the systems included in the migration (SIDs, landscape role, environment).",
        "Verify AWS account availability and the target region.",
        "Create or validate ServiceNow CMDB configuration items for each system.",
        "Perform IP address analysis: current addressing, subnets, overlaps, static entries, host-file records.",
        "Confirm SAP, OS/DB and AWS access for every engineer who will execute work — including privileged and third-party access.",
        "Collect source system and database parameters."]))
    out.append(box("warn", "Access is the most common silent delay",
                   para("Access requests that are raised in the cutover week arrive after the window. Raise SAP, OS, database, "
                        "AWS, middleware and third-party interface credentials during preparation, and confirm each one by "
                        "actually logging in — not by receiving a ticket closure.")))
    out.append(h3("4.2", "Source sizing and workload"))
    out.append(bullets([
        "Sizing considers CPU, memory, server configuration, instance type and source-to-target mapping.",
        "The migration team <b>consumes</b> the approved sizing report for target planning and validation — it does not create or re-derive it.",
        "<code>ST03</code> / <code>ST03N</code> is used for workload analysis, particularly for production systems.",
        "Workload information provides the context for post-migration performance comparison: without it, “the system feels slower” cannot be resolved."]))
    out.append(table(["Sizing input", "What to capture", "Why it matters later"],
                     [["CPU and memory", "Current configuration, peak and average utilisation", "Confirms the target instance type is not undersized"],
                      ["Server configuration", "Host type, physical or virtual, cluster membership", "Drives HA design and licensing implications"],
                      ["Instance type mapping", "Source host → target EC2/instance type", "Becomes the build sheet and the validation reference"],
                      ["Database size and growth", "Data, log, archive, backup volumes and growth rate", "Sizes storage, snapshots and backup windows"],
                      ["Workload (ST03N)", "Dialog, batch and interface load by hour/day", "Sets the performance baseline for comparison after migration"],
                      ["Peak patterns", "Month-end, batch windows, integration peaks", "Determines when cutover is safe and what to re-measure"]],
                     caption="Sizing inputs consumed by the migration team", widths=["22%", "40%", "38%"]))
    out.append(h3("4.3", "Inventory and external dependencies"))
    out.append(table(["Inventory item", "Detail to record"],
                     [["Identity", "Hostname, IP address, CMDB CI number, SID, environment"],
                      ["Software", "Kernel version and patch level, database type and version, NetWeaver / SAP_BASIS release, SP level"],
                      ["External agents", "Control-M, NetBackup, OEM/OBM and any other monitoring, scheduling or backup agent installed on the host"],
                      ["Credentials", "OS, database, Oracle and Oracle Wallet credentials identified through approved processes (never shared by email or chat)"],
                      ["NFS dependencies", "Every NFS mount: export host, path, purpose, consumer. Decide per share whether it is maintained/copied or migrated to AWS EFS"],
                      ["AL11 directories", "Directory state before migration — which SAP directories exist, what they contain, which are custom"],
                      ["Certificates and keys", "SNC, SSL/TLS, PSE files, keystores, wallet locations and expiry dates"],
                      ["Jobs and scheduling", "Background jobs, job schedulers, batch windows, and which are controlled externally"]],
                     caption="Source inventory content", widths=["22%", "78%"]))
    out.append(box("key", "External agents are the classic cutover surprise",
                   para("Agents installed by other teams (backup, scheduling, monitoring, security) are frequently missing from the "
                        "source inventory because no one on the migration team installed them. Enumerate them from the host, not from "
                        "memory: compare installed packages, running services and cron entries on source and target.")))
    out.append(h3("4.4", "Interface and connectivity baseline"))
    out.append(bullets([
        "Identify SAP-to-SAP interfaces, external applications, middleware, RFCs and network dependencies.",
        "Validate SSO dependencies and the authentication path for each user group.",
        "Use <code>SM59</code> to identify RFC destinations and connection types; record each destination, its target and its status.",
        "Record whether each interface is <b>working before migration</b> — success or failure, with a timestamp.",
        "Treat pre-existing failures as baseline conditions rather than migration defects."]))
    out.append(table(["Interface category", "How to enumerate", "Baseline evidence"],
                     [["SAP ↔ SAP (RFC)", "<code>SM59</code> destinations by type; connection test per destination", "Destination list + test result, with failures annotated"],
                      ["Middleware / ESB", "webMethods, MuleSoft, MBox and other documented integrations " + pill("source term", "a"), "Interface inventory with owning team and credentials status"],
                      ["External applications", "Interface documentation, port and firewall rules, partner contacts", "Connectivity matrix: source host/port → target host/port"],
                      ["File-based interfaces", "<code>AL11</code> directories, NFS mounts, scheduled transfers", "Directory listing before migration and the transfer schedule"],
                      ["Authentication / SSO", "SNC configuration, certificates, SSO provider dependencies", "Certificate validity, SNC users, SSO test result"],
                      ["Gateway traffic", "<code>SMGW</code> connections and gateway parameters", "Connection list and gateway status"],
                      ["HTTP(S) traffic", "<code>SMICM</code> ICM services and endpoints", "Service list, ports, certificate binding"]],
                     caption="Interface baseline", widths=["22%", "42%", "36%"]))
    out.append(box("risk", "Practical rule",
                   para("If an interface or directory was not working before migration, capture the evidence. The migration team "
                        "should not silently convert a pre-existing issue into a migration defect — and equally should not silently "
                        "fix one without recording it, because an unrecorded fix becomes an unapproved change.")))
    out.append(h3("4.5", "Building the source baseline pack"))
    out.append(para("The output of this module is a single, indexed evidence pack per system. It is the reference used at every "
                    "later gate and during hypercare triage."))
    out.append(table(["Baseline artefact", "Typical source", "Used again at"],
                     [["OS parameter sheet", "<code>uname</code>, <code>/etc/os-release</code>, kernel, swap, file systems, UID/GID", "Section 7.2 OS validation"],
                      ["SAP parameter sheet", "Profile parameters (<code>RZ10</code>/<code>RZ11</code>), instance list (<code>SM51</code>)", "Section 7.3 SAP validation"],
                      ["Database parameter sheet", "<code>DB02</code>, DB parameters, tablespace list and sizes", "Section 7.4 database validation"],
                      ["Interface list", "<code>SM59</code>, <code>SMGW</code>, <code>SMICM</code>, middleware inventory", "Section 10.3 functional validation"],
                      ["Directory list", "<code>AL11</code>, NFS mounts, custom directories and permissions", "Section 10.2 post-processing"],
                      ["Workload snapshot", "<code>ST03</code>/<code>ST03N</code> daily/weekly/monthly, <code>STAD</code> samples", "Module 5 performance comparison"],
                      ["Memory and buffer snapshot", "<code>ST02</code>", "Module 5 performance comparison"],
                      ["Backup status", "Last successful backup, backup history, log/archive status", "Section 6.4, Section 9.4"],
                      ["Known issues", "Open tickets, failing interfaces, failing jobs, missing directories", "Hypercare triage (Section 10.6)"],
                      ["Transport landscape", "<code>STMS</code> domain, systems, routes, transport directory", "Section 7.3, Section 10.3"]],
                     caption="Contents of the source baseline pack", widths=["24%", "42%", "34%"]))
    out.append(h3("4.6", "Module 1 readiness checklist"))
    out.append(checklist("m1", ["Done", "Check", "Status", "Evidence / remarks"], [
        "Migration scope finalised and documented with the customer",
        "Systems in scope identified (SID, environment, landscape role)",
        "AWS account availability verified; target region confirmed",
        "ServiceNow CMDB CIs created or validated for each system",
        "IP address analysis completed (addressing, overlaps, static entries)",
        "SAP, OS/DB and AWS access confirmed by successful login for every engineer",
        "Third-party and middleware credentials requested through approved processes",
        "Source system and database parameters collected",
        "Approved sizing report received and consumed (not re-derived)",
        "ST03/ST03N workload snapshot captured for production systems",
        "Host inventory complete: hostname, IP, CI, kernel, DB, NetWeaver release",
        "External agents identified (Control-M, NetBackup, OEM/OBM, others)",
        "NFS dependencies listed with a decision per share (maintain/copy vs EFS)",
        "AL11 directory state captured before migration",
        "SAP-to-SAP, external, middleware and RFC interfaces identified",
        "SSO and SNC dependencies validated",
        "SM59 destinations exported with connection test results",
        "SMGW and SMICM connection/service baseline captured",
        "Working vs failing state recorded for every interface",
        "Pre-existing failures documented as baseline conditions with evidence",
        "Baseline evidence pack indexed and stored per retention rules",
    ]))
    out.append("</section>")
    return "".join(out)


def s5_m2():
    out = [section("m2", "5", "Module 2 — Target architecture, AWS readiness and build", cls="mod",
                   kick="Module 2 · Section 5",
                   lead="The automation team builds the target; the migration team proves it is right. Validating someone else's "
                        "output is not a lack of trust — it is the control that keeps an infrastructure defect out of a production "
                        "cutover.")]
    out.append(h3("5.1", "Target architecture"))
    out.append(bullets([
        "Confirm customer agreement with the proposed AWS target configuration and instance type.",
        "Architecture diagrams should show AWS Region, Availability Zones, SAP servers, database servers, ASCS/ERS where "
        "applicable, major infrastructure components and high-level connectivity.",
        "HA/DR discussions may include ASCS, ERS/CRS, Oracle, secondary/standby systems and failover architecture.",
        "Record the agreed RPO/RTO and the failover mechanism — an HA design nobody can describe under pressure is not an HA design."]))
    out.append(figure("d3-aws-architecture", FIG["d3-aws-architecture"],
                      "<b>Figure 3.</b> Target AWS reference architecture used for training. It shows the shape of a typical SAP-on-AWS "
                      "landing zone — two AZs, application and database subnets, an HA partner, and the shared services the migration "
                      "depends on (S3, EFS, Route 53, snapshots, KMS). Instance types, AZ count and HA mechanism always come from the "
                      "approved sizing report and build sheet."))
    out.append(table(["Architecture element", "What must be agreed and recorded"],
                     [["Region and AZs", "Target region, number of AZs, and which component sits in which AZ"],
                      ["SAP servers", "ASCS/ERS (or CRS), PAS, AAS count and sizing per instance"],
                      ["Database servers", "HANA or Oracle, instance/storage class, HA mechanism (HSR, Data Guard, cluster)"],
                      ["Network", "VPC, subnets and their purpose, route tables, security groups / NACLs, inter-AZ latency"],
                      ["Connectivity", "On-premises connectivity method, SAProuter, jump/bastion access, DNS resolution path"],
                      ["Storage", "Root, SAP data/log volumes, shared file systems, backup targets, snapshot policy"],
                      ["Security", "Encryption at rest and in transit, key management, privileged access path, audit logging"],
                      ["Observability", "Monitoring agents, log forwarding, alerting ownership"]],
                     caption="Architecture content that must be explicit", widths=["24%", "76%"]))
    out.append(h3("5.2", "Build sheet"))
    out.append(steps([
        "Prepare the build sheet from the approved sizing report and architecture.",
        "Perform peer review — a second engineer checks every field against the source documents.",
        "Finalise the information with the customer and obtain their confirmation.",
        "Use only the approved information for target provisioning.",
        "Validate the provisioned environment against the build sheet, field by field."]))
    out.append(table(["Build sheet field group", "Examples", "Validation method after build"],
                     [["Identity", "Hostname, SID, instance number, domain, environment", "Compare with <code>hostname</code>, SAP profile, CMDB CI"],
                      ["Compute", "Instance type, vCPU, RAM, AZ, placement", "AWS console/CLI describe-instance versus build sheet"],
                      ["Network", "VPC, subnet, private/public IP, security groups, routes", "Interface attachment, IP, and reachability tests"],
                      ["Storage", "Volume types and sizes, mount points, shared file systems", "<code>df -h</code>, <code>lsblk</code>, <code>/etc/fstab</code>"],
                      ["OS", "Distribution, version, kernel, packages, tuning parameters", "<code>/etc/os-release</code>, <code>uname -r</code>, package list"],
                      ["Users and groups", "UID/GID for <code>sapadm</code>, <code>&lt;sid&gt;adm</code>, DB users, groups", "<code>id</code>, <code>getent passwd/group</code>"],
                      ["Database", "Engine, version, SID, memory allocation, parameters", "DB status, parameter export"],
                      ["SAP", "Kernel/patch level, instance profile parameters, services", "<code>SM51</code>, <code>RZ10</code>, service status"],
                      ["Backup", "Backup tool, target bucket/path, retention", "Test backup job and verify the object exists"],
                      ["Access and agents", "Bastion/SAProuter, monitoring, backup and scheduling agents", "Agent status and version check"]],
                     caption="Build sheet content and how each group is validated", widths=["20%", "38%", "42%"]))
    out.append(box("key", "Peer review is the cheapest control in the programme",
                   para("Most provisioning defects found after build (wrong subnet, missing mount, UID mismatch, absent security-group "
                        "rule) would have been caught by a second pair of eyes reading the build sheet against the sizing report. "
                        "Build the review into the schedule; do not treat it as optional when the timeline tightens.")))
    out.append(h3("5.3", "AWS bootstrapping and infrastructure validation"))
    out.append(bullets([
        "Validate VPC, Availability Zones, subnets and available IP addresses.",
        "Validate the required AWS resources (compute, storage, network, security, backup).",
        "Validate DNS configuration and Route 53 where applicable — forward, reverse, and the private-zone resolution path used by SAP.",
        "Validate S3 bucket and folder requirements for Oracle backup and package use cases.",
        "Validate required read/write permissions and backend connectivity from the servers that will use them.",
        "Confirm tagging, inventory and CMDB automation produced correct records."]))
    out.append(table(["Validation", "What a pass looks like", "Common failure"],
                     [["VPC and subnets", "CIDRs, AZ placement and route tables match the build sheet", "Subnet in the wrong AZ; free-IP exhaustion"],
                      ["IP address availability", "Enough free addresses for all planned interfaces, including HA and future growth", "Overlap with source addressing; static entries missed"],
                      ["DNS / Route 53", "Forward and reverse resolution correct from every subnet; private zones associated", "Resolver rule missing; reverse lookup absent"],
                      ["S3 bucket and folders", "Bucket exists, folder structure correct, versioning/encryption as designed", "Folder path differs from the backup configuration"],
                      ["S3 permissions", "The instance role/user can read and write the intended prefix, and nothing broader", "Policy too narrow (backup fails) or too broad (audit finding)"],
                      ["Backend connectivity", "Backup agent or HANA reaches the endpoint over the intended path", "Endpoint or proxy not permitted in the security group"],
                      ["EFS / shared storage", "Mounted, correct permissions, and reachable from every consumer", "Mount missing on the secondary node; wrong UID/GID owner"],
                      ["Snapshots and backup policy", "Policy attached, retention correct, restore path tested at least once", "Policy attached to the wrong volume set"],
                      ["Tagging and CMDB", "Tags present, CI created, relationships and status correct", "CI created with source details, or left in “planned”"]],
                     caption="Infrastructure validation matrix", widths=["20%", "42%", "38%"]))
    out.append(h3("5.4", "Responsibility split"))
    out.append(table(["Role", "Primary responsibilities"],
                     [["Automation team", "AWS provisioning, server creation, automated build, DNS provisioning, tagging, Chef/configuration management, inventory and CMDB automation."],
                      ["Basis / migration team", "Build-sheet input, target validation, SAP-specific activities, SAP/database configuration validation, migration checks and handover."],
                      ["Specialist teams", "DBA, Linux, network, security, application, interface and DR teams support their respective specialist areas."]],
                     caption="Responsibility split (summary — full matrix in Figure 2)", widths=["24%", "76%"]))
    out.append(box("warn", "Where the split breaks in practice",
                   bullets([
                       "<b>DNS.</b> Automation provisions records; Basis validates resolution from the SAP host. If neither owns the private-zone association, name resolution fails at cutover.",
                       "<b>File systems.</b> Linux mounts the file systems; Basis validates that SAP directories and permissions are correct. Ownership of the mount options must be explicit.",
                       "<b>Credentials.</b> Security/AD issues them; Basis and DBA consume them. Requests must be raised early and tracked, not escalated on cutover day.",
                       "<b>Agents.</b> Automation installs platform agents; the owning team installs application agents (backup, scheduling, monitoring). Both lists must be reconciled against the source."])))
    out.append(h3("5.5", "CMDB validation after build"))
    out.append(checklist("cmdb", ["Done", "Check", "Status", "Evidence / remarks"], [
        "CI exists for every new server in ServiceNow",
        "CI relationship is correct (host → application → database)",
        "Application / DB relationship is correct for each SID",
        "CI status is deployed / operational (not planned or in build)",
        "Target server details match the inventory and the build sheet",
        "Hostname, IP, environment and owning team are correct on the CI",
        "Old source CIs flagged for retirement at the correct date",
        "Tags on AWS resources match the CMDB and cost-allocation standard",
    ]))
    out.append(h3("5.6", "Module 2 readiness checklist"))
    out.append(checklist("m2", ["Done", "Check", "Status", "Evidence / remarks"], [
        "Customer agreement recorded for target configuration and instance type",
        "Architecture diagram covers region, AZs, SAP, DB, ASCS/ERS and connectivity",
        "HA/DR design documented (ASCS, ERS/CRS, standby database, failover)",
        "RPO/RTO and failover mechanism agreed with the customer",
        "Build sheet prepared from approved sizing and architecture",
        "Build sheet peer-reviewed by a second engineer",
        "Build sheet finalised and confirmed with the customer",
        "Provisioning used only approved build-sheet information",
        "VPC, AZs, subnets and free IP availability validated",
        "Required AWS resources validated against the build sheet",
        "DNS and Route 53 configuration validated (forward and reverse)",
        "S3 buckets and folders validated for backup and package use cases",
        "S3 read/write permissions and backend connectivity validated",
        "EFS / shared file systems mounted with correct ownership and permissions",
        "Snapshot and backup policies attached and a restore path tested",
        "Provisioned environment validated field-by-field against the build sheet",
        "Deviations logged with an owner and a resolution date",
    ]))
    out.append("</section>")
    return "".join(out)


def s6_m3():
    out = [section("m3", "6", "Module 3 — SAP HANA MDC, backup and recovery", cls="mod",
                   kick="Module 3 · Section 6",
                   lead="HANA migration succeeds or fails on the backup and recovery path. Understand the container model, prove the "
                        "backend works, and never stop the source before the final backup is validated.")]
    out.append(figure("d4-hana-mdc", FIG["d4-hana-mdc"],
                      "<b>Figure 4.</b> HANA MDC containers inside one HANA system, the S3 backup backend, and the six-step recovery "
                      "sequence. Note the separation on the left: the three tiers are validated bottom-up — the database is recovered "
                      "first, then the application servers are started against it."))
    out.append(h3("6.1", "HANA MDC architecture"))
    out.append(bullets([
        "<b>SystemDB</b> provides central management and monitoring capabilities for the whole HANA system.",
        "<b>TenantDB</b> contains the application and data workload for a specific SAP system.",
        "SystemDB and TenantDB have separate login contexts and credentials — connecting to the wrong context is a common operator error.",
        "SystemDB/TenantDB should not be confused with HA server architecture.",
        "SystemDB and TenantDB can reside within the same HANA server/VM; HA is a separate infrastructure/system-level design."]))
    out.append(table(["Aspect", "SystemDB", "TenantDB"],
                     [["Purpose", "Central management and monitoring of the HANA system", "Hosts the application and data workload"],
                      ["Contains", "System-wide configuration, nameserver, backup catalogue", "Application tables, tenant services, tenant configuration"],
                      ["Login context", "Own context and credentials (for example the SYSTEM user)", "Own context and credentials, separate from SystemDB"],
                      ["Backup", "Holds the backup catalogue for the system", "Has its own backup configuration and data volume"],
                      ["Recovery", "Recovered/restored first so tenants can be recovered", "Recovered after the system context is available"],
                      ["HA relationship", "Not an HA component — a database container", "Not an HA component — a database container"]],
                     caption="SystemDB versus TenantDB", widths=["16%", "42%", "42%"]))
    out.append(box("risk", "The most common HANA conceptual error",
                   para("Treating SystemDB/TenantDB as a primary/standby pair. They are containers within one HANA system. High "
                        "availability is achieved by a different mechanism (system replication plus clustering or failover tooling, "
                        "with storage and network design), and it is decided at infrastructure level.")))
    out.append(h3("6.2", "HANA pre-checks"))
    out.append(checklist("hana-pre", ["Done", "Check", "Status", "Evidence / remarks"], [
        "Database / EC2 sizing confirmed against the approved sizing report",
        "Shared file system sizing confirmed",
        "Required INI files and HANA configuration present and consistent",
        "S3 bucket and backend configuration validated",
        "HANA DB server status checked (services running, no failed units)",
        "Transparent Huge Pages (THP) configuration checked against the SAP requirement",
        "Kernel and HANA version confirmed against the target design",
        "Global INI and relevant service configuration reviewed",
        "Index server and name server configuration reviewed",
        "OS prerequisites verified: hugepages, shared memory, limits, scheduler tuning",
        "Evidence for every pre-check captured and stored",
    ]))
    out.append(para("Pre-check output should be retained even when everything passes. A clean pre-check record is what allows you to "
                    "say later that a problem was introduced by the migration rather than carried into it."))
    out.append(h3("6.3", "AWS S3 backup backend"))
    out.append(checklist("s3", ["Done", "Check", "Status", "Evidence / remarks"], [
        "S3 bucket availability confirmed in the correct region",
        "Required bucket and folder structure created",
        "Read/write policies and permissions validated for the backup identity",
        "Backup path configuration validated in HANA",
        "Backend connectivity from the HANA host validated (endpoint, DNS, proxy, security group)",
        "Encryption and key management confirmed",
        "Required configuration / INI files available and consistent with the backup setup",
        "A real backup has been written to the backend and the objects verified",
        "Retention and lifecycle rules match the project standard",
    ]))
    out.append(box("warn", "Backint versus file-based backup",
                   para("The source training refers to an S3 backup backend without naming the mechanism. In practice this is either a "
                        "certified Backint agent for S3 or a file-based backup to a mounted/S3-synced target. Confirm which one the "
                        "project uses, because the configuration files, permissions, log locations and restore syntax differ. "
                        + pill("Validate", "r"))))
    out.append(h3("6.4", "Backup and recovery sequence"))
    out.append(steps([
        "Configure the backup destination on the source.",
        "Validate S3/backend connectivity end to end (write and read).",
        "Test backup and recovery <b>before</b> cutover, on a target that mirrors production.",
        "Verify recovered data consistency (row counts, key tables, application logon, no failed recovery steps in the log).",
        "Capture evidence of the successful test: backup log, recovery log, timestamps, verification output.",
        "During cutover, execute the final backup.",
        "Complete final backup validation <b>before</b> source shutdown.",
        "Stop the source system only after the required backup activity has succeeded.",
        "Configure the target and initiate recovery.",
        "Validate database and application connectivity after recovery."]))
    out.append(flow(["Source backup", "Configuration file", "S3 backend", "Target configuration", "Recovery", "Validation"]))
    out.append(box("risk", "Sequencing rule that protects the programme",
                   para("Keep the source available until the required final backup activity is successfully completed. Stopping the "
                        "source first removes the rollback option and turns a routine recovery into an incident.")))
    out.append(h3("6.5", "Three-tier application validation"))
    out.append(table(["Layer", "What is validated", "Order"],
                     [["UI / presentation layer", "SAP GUI or Fiori connectivity, login, transaction rendering, timeout behaviour", "3rd"],
                      ["Application layer", "Work processes, instance start, RFC and Gateway connectivity, spool, ICM services", "2nd"],
                      ["Database layer", "HANA services, tenant status, connectivity from the application, data retrieval and updates", "1st"]],
                     caption="Three-tier validation order", widths=["22%", "60%", "18%"], align=[None, None, "c"]))
    out.append(para("Database recovery is completed first; application servers are then started and validated against the recovered "
                    "HANA database. Validate application processing, data retrieval, updates and database connectivity — not just "
                    "“the instance is green”."))
    out.append(h3("6.6", "Module 3 readiness checklist"))
    out.append(checklist("m3", ["Done", "Check", "Status", "Evidence / remarks"], [
        "SystemDB and TenantDB roles understood and documented for this system",
        "SystemDB/TenantDB not confused with the HA design in project documentation",
        "HANA pre-checks executed with all output retained",
        "S3 backup backend configured and connectivity proven",
        "Backup tested successfully to the S3 backend",
        "Recovery tested successfully on a non-production target",
        "Recovered data consistency verified",
        "Backup/recovery evidence pack complete",
        "Cutover backup window and duration estimated from the test",
        "Rollback anchor defined (final backup plus snapshot)",
        "Three-tier validation performed in the correct order after recovery",
    ]))
    out.append("</section>")
    return "".join(out)
