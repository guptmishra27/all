"""Handbook content, part 3: sections 11-17 and appendices."""

from htmlkit import (box, bullets, cards, checklist, cmd, e, figure, flow, h3, kpis,
                     para, pill, qa, section, steps, table)

FIG = {}
STATS = {"figures": 8, "tables": 70, "checklists": 15, "items": 209, "quiz": 16,
         "glossary": 53, "words": 24000, "callouts": 49, "sections": 25}


# --------------------------------------------------------------------------- #
def s11_tcode():
    out = [section("tcode", "11", "SAP transaction and technology quick reference",
                   kick="Section 11 · Reference",
                   lead="The working vocabulary of a migration. Learn what each item proves — a transaction you cannot interpret "
                        "produces a screenshot, not evidence.")]
    out.append(h3("11.1", "SAP transactions"))
    out.append(table(["Transaction", "Purpose in this training", "What you check", "Module"],
                     [["<code>ST03</code> / <code>ST03N</code>", "Workload and performance analysis", "Response, DB, CPU and wait time; steps and users; daily/weekly/monthly trend", "5"],
                      ["<code>STAD</code>", "Detailed transaction and user-level performance analysis", "Individual statistical records behind the aggregates: the slow steps and where the time went", "5"],
                      ["<code>ST02</code>", "SAP memory and buffer monitoring", "Extended, heap/private, roll, paging; buffer utilisation and hit ratio", "5"],
                      ["<code>AL11</code>", "SAP directory analysis and interface/custom directory validation", "Directory presence, content, permissions and changes versus the baseline", "1, 4"],
                      ["<code>SM59</code>", "RFC destination and connectivity validation", "Destinations by type, connection test result, logon and authentication", "1, 4, 7"],
                      ["<code>SMGW</code>", "SAP Gateway monitoring and troubleshooting", "Gateway status, active connections, unexpected or missing registrations", "4, 7"],
                      ["<code>SMICM</code>", "HTTP/HTTPS and ICM communication monitoring", "ICM services and ports, URL handling, certificate binding, errors", "4, 7"],
                      ["<code>SM51</code>", "Application server status and availability", "All planned instances active and registered; work process configuration", "4, 7"],
                      ["<code>STMS</code> / TMS", "Transport landscape, domain, routes and transport directory", "Domain controller, systems, routes, transport directory path, import test", "4, 7"],
                      ["<code>RZ10</code>", "Persistent profile parameter maintenance", "Profile versions, imports, activation and the restart requirement per parameter", "5, 7"],
                      ["<code>RZ11</code>", "Dynamic/temporary parameter changes where supported", "Current runtime value versus the profile value", "5"],
                      ["<code>DB02</code>", "Database status, storage and tablespace information", "Space, tablespaces, growth, backup status (database-dependent views)", "4"],
                      ["<code>SPAD</code>", "Printer configuration and spool validation", "Output devices, device types, host printers, test page", "4, 7"],
                      ["<code>SP01</code>", "Spool requests", "Spool output present, no stuck or failed requests", "4, 7"],
                      ["<code>STRUST</code>", "Certificate and PSE management", "Certificate validity, chain, hostname/domain match, expiry", "4, 7"],
                      ["<code>SLICENSE</code>", "SAP license administration", "Hardware key after migration, installed license, temporary-license expiry", "4"],
                      ["<code>SA38</code>", "ABAP report execution (used for RFC connectivity reports)", "Running the project's RFC/interface test report", "1, 4"],
                      ["<code>ST22</code>", "ABAP runtime error analysis", "New or rising dumps after go-live", "7"],
                      ["<code>SM37</code>", "Background job overview", "Job status after cutover: released, running, cancelled", "7"],
                      ["<code>SM13</code>", "Update errors", "Stuck or failed update records — business-visible data issues", "7"],
                      ["<code>SM12</code>", "Lock entries", "Stale or growing locks after go-live", "7"],
                      ["<code>WE02</code> / <code>BD87</code>", "IDoc monitoring and processing", "Failed or stuck IDocs on interfaces", "7"],
                      ["Solution Manager / EarlyWatch", "Central monitoring and SAP health information", "Landscape health, configuration and performance reporting where available", "5"]],
                     caption="SAP transaction reference", widths=["15%", "27%", "46%", "12%"]))
    out.append(h3("11.2", "Database, platform and tooling reference"))
    out.append(table(["Technology", "Purpose in this training", "Module"],
                     [["Oracle Data Guard", "Database replication and planned switchover mechanism in the discussed Oracle scenario", "6"],
                      ["Oracle <code>DBVERIFY</code> (<code>dbv</code>)", "Block-level integrity check for database corruption after switchover", "6"],
                      ["Oracle <code>RMAN</code>", "Backup and recovery of the new primary after successful validation", "6"],
                      ["Oracle OEM agent", "Monitoring coverage restored on the new primary in production", "6"],
                      ["Oracle listener / SQL*Net", "Database connectivity path validated from the SAP application hosts", "6"],
                      ["Data Guard Broker + observer node", "Configuration management and independent monitoring for HA designs", "6"],
                      ["<code>R3trans -d</code>", "SAP-to-database connectivity check; training expects return code <code>0000</code>", "7"],
                      ["<code>sapcontrol</code> / <code>sapstart</code>", "Instance control and status from the OS, without the GUI", "4, 7"],
                      ["AWS Route 53", "DNS management: hosted zones, records and the cutover CNAME/IP change", "2, 6"],
                      ["AWS S3", "Object storage used as the backup backend (HANA, Oracle) and for packages", "2, 3"],
                      ["AWS EFS", "Managed file service — an option when migrating NFS shares", "1, 2"],
                      ["EC2 snapshots", "Disk-level rollback recovery point before risky cutover activities", "6, 7"],
                      ["AWS KMS", "Encryption keys for storage, backups and snapshots", "2"],
                      ["Chef", "OS and configuration management used by the automation team", "2"],
                      ["CMDB / ServiceNow", "Configuration inventory, CIs, relationships and lifecycle status", "1, 2"],
                      ["Control-M", "External job scheduling — resumed with the owning team after go-live", "1, 7"],
                      ["NetBackup", "Backup agent that must be inventoried and re-pointed on the target", "1, 2"],
                      ["rsync", "Synchronization of SAP global directories during post-processing", "7"],
                      ["<code>systemd</code> / SAP service", "Service that must start SAP automatically after a reboot", "4"]],
                     caption="Technology reference", widths=["22%", "62%", "16%"]))
    out.append(h3("11.3", "OS commands used during validation"))
    out.append(table(["Command", "Validates", "Section"],
                     [["<code>df -h</code>, <code>mount</code>, <code>lsblk</code>", "File systems, mount points, sizes and options", "7.2"],
                      ["<code>lscpu</code>, <code>nproc</code>, <code>free -g</code>", "CPU and memory versus the build sheet", "7.2"],
                      ["<code>uname -r</code>, <code>/etc/os-release</code>", "Kernel and OS version", "7.2"],
                      ["<code>id</code>, <code>getent passwd</code>, <code>getent group</code>", "UID/GID and group membership consistency", "7.2"],
                      ["<code>ip a</code>, <code>ip r</code>", "Physical and virtual IPs, routes", "7.2"],
                      ["<code>hostname -f</code>, <code>getent hosts</code>, <code>nslookup</code>", "Hostname and DNS resolution", "7.2, 9.5"],
                      ["<code>swapon -s</code>, <code>sysctl vm.swappiness</code>", "Swap configuration", "7.2"],
                      ["<code>grep -E 'sapdp|sapgw' /etc/services</code>", "SAP service port definitions", "7.2"],
                      ["<code>ldd</code> on key binaries", "Shared library dependencies", "7.2"],
                      ["<code>systemctl status / show</code>", "Service state, result and exit code", "7.1"],
                      ["<code>sapcontrol -nr &lt;nn&gt; -function GetProcessList</code>", "Instance process state from the OS", "7.1"],
                      ["<code>R3trans -d</code>", "SAP-to-database connectivity (expect <code>0000</code>)", "10.2"],
                      ["<code>rsync -avn</code> (dry run first)", "Global directory synchronization", "10.2"]],
                     caption="Command quick reference", widths=["34%", "48%", "18%"],
                     note="Command names and syntax differ by distribution, SAP release and project standard. These are the checks to perform, not copy-paste production commands."))
    out.append(h3("11.4", "Key files and locations"))
    out.append(table(["File / location", "Relevance"],
                     [["<code>/etc/hosts</code>", "Hostname and virtual-hostname resolution; stale entries silently override DNS"],
                      ["<code>/etc/services</code>", "<code>sapdp&lt;nn&gt;</code> and <code>sapgw&lt;nn&gt;</code> port definitions used by SAP and the gateway"],
                      ["<code>/etc/fstab</code>", "Mount definitions — a missing or misordered entry breaks SAP at boot"],
                      ["SAP profile directory", "Instance and default profiles maintained via <code>RZ10</code>"],
                      ["SAP work / log directories", "<code>dev_w*</code>, <code>dev_disp</code>, <code>dev_ms</code> traces used to diagnose start failures"],
                      ["SAP global directories", "Transport, interface and shared directories synchronized with <code>rsync</code>"],
                      ["HANA INI files", "<code>global.ini</code>, <code>nameserver.ini</code> and service configuration used in recovery"],
                      ["Oracle network files", "<code>listener.ora</code>, <code>tnsnames.ora</code>, <code>sqlnet.ora</code>"],
                      ["Oracle wallet / PSE / keystore locations", "Credentials and certificates for SNC, SSL and database authentication"],
                      ["<code>R3trans</code> trace (<code>trans.log</code>)", "First place to look when <code>R3trans -d</code> does not return <code>0000</code>"]],
                     caption="Files that decide whether a cutover works", widths=["30%", "70%"]))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s12_checklists():
    out = [section("checklists", "12", "Consolidated validation checklists",
                   kick="Section 12 · Reference",
                   lead="Five checklists covering the whole validation surface. They are interactive: tick a check, set a status, "
                        "add the evidence reference. Progress persists in your browser and is printed as a static record.")]
    out.append(box("key", "How to use these checklists in anger",
                   bullets([
                       "Run them twice per system: once at pre-cutover validation (Gate 1) and once during the cutover window.",
                       "Every item needs either a tick with evidence, or a recorded deferral with an owner, an impact statement and a date.",
                       "“Not applicable” is a valid status — but write why. An unexplained N/A is an audit finding waiting to happen.",
                       "Transfer the results into the project's validation workbook or change record before sign-off; the browser copy is a working aid, not the system of record."])))
    tools = ('<div class="ck-tools no-print"><button class="btn" data-reset="#list-os">Reset OS list</button>'
             '<button class="btn" data-reset="#list-sap">Reset SAP list</button>'
             '<button class="btn" data-reset="#list-db">Reset database list</button>'
             '<button class="btn" data-reset="#list-perf">Reset performance list</button>'
             '<button class="btn" data-reset="#list-cut">Reset cutover list</button></div>')
    out.append(tools)

    out.append(h3("12.1", "OS validation"))
    out.append('<div id="list-os"></div>')
    out.append(checklist("os", ["Done", "Check", "Status", "Evidence / remarks"], [
        "File systems / mount points", "CPU", "RAM", "Swap", "OS version", "Kernel version",
        "UID/GID", "Libraries", "FTP users", "OS groups", "IP addresses", "Hostnames",
        "/etc/hosts", "/etc/services", "SAP directories", "Permissions",
    ]))

    out.append(h3("12.2", "SAP validation"))
    out.append('<div id="list-sap"></div>')
    out.append(checklist("sap", ["Done", "Check", "Status", "Evidence / remarks"], [
        "SAP services active", "Auto-start tested (real reboot)", "SAP processes green",
        "Application servers available", "SM51", "SMGW", "SM59", "RFC report",
        "SNC", "STMS", "Transport directory", "AL11", "Printers", "Spool", "SMICM",
        "SSL/TLS certificates", "SAP license",
    ]))

    out.append(h3("12.3", "Database validation"))
    out.append('<div id="list-db"></div>')
    out.append(checklist("db", ["Done", "Check", "Status", "Evidence / remarks"], [
        "DB status", "DB02", "Storage utilization", "Tablespaces", "Database growth",
        "Latest backup", "Backup status", "Redo/archive logs", "Recovery requirements",
    ]))

    out.append(h3("12.4", "Performance validation"))
    out.append('<div id="list-perf"></div>')
    out.append(checklist("perf", ["Done", "Check", "Status", "Evidence / remarks"], [
        "ST02 memory", "Extended memory", "Heap/private memory", "Buffer utilization",
        "ST03N workload", "Response time", "Wait time", "DB request time", "CPU time",
        "Performance trends",
    ]))

    out.append(h3("12.5", "Cutover readiness"))
    out.append('<div id="list-cut"></div>')
    out.append(checklist("cut", ["Done", "Check", "Status", "Evidence / remarks"], [
        "Application shutdown confirmed", "DBA handover confirmed",
        "Source/target synchronization confirmed", "Snapshot/backup confirmed",
        "DNS/IPAM plan confirmed", "Evidence captured", "Technical validation complete",
        "Functional validation complete", "Approvals complete", "Rollback ready",
        "Go/No-Go decision recorded",
    ]))
    out.append(h3("12.6", "Sign-off"))
    out.append(table(["Validation domain", "Validated by", "Date", "Deviations / deferrals", "Reviewed by"],
                     [["OS validation", "", "", "", ""],
                      ["SAP validation", "", "", "", ""],
                      ["Database validation", "", "", "", ""],
                      ["Performance validation", "", "", "", ""],
                      ["Cutover readiness", "", "", "", ""],
                      ["Functional validation", "", "", "", ""],
                      ["Go/No-Go decision", "", "", "", ""]],
                     caption="Validation sign-off record", widths=["22%", "18%", "12%", "32%", "16%"], cls="plain"))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s13_evidence():
    out = [section("evidence", "13", "Evidence and documentation strategy",
                   kick="Section 13 · Reference",
                   lead="Evidence is the difference between “it works” and “it is proven to work, by these checks, at this time, "
                        "compared with this baseline”. It is also the only defence against absorbing a pre-existing fault as a "
                        "migration defect.")]
    out.append(figure("d8-evidence", FIG["d8-evidence"],
                      "<b>Figure 8.</b> The evidence lifecycle. The loop from retest back to comparison is deliberate: a correction is "
                        "not complete until the comparison has been re-run and re-recorded."))
    out.append(h3("13.1", "Evidence lifecycle"))
    out.append(steps([
        "Capture source evidence before migration.",
        "Execute migration/cutover activities.",
        "Capture equivalent target evidence.",
        "Compare source and target.",
        "Identify deviations.",
        "Correct issues with the responsible team.",
        "Retest.",
        "Capture final evidence.",
        "Complete handover."]))
    out.append(box("warn", "Equivalent means equivalent",
                   para("A target screenshot of a different transaction, a different time window or a filtered view is not comparable "
                        "evidence. Same check, same scope, same tooling, and — for performance — the same period type and load profile.")))
    out.append(h3("13.2", "Evidence categories"))
    cats = ["OS configuration and file systems", "CPU and memory", "UID/GID", "IP / hostname",
            "SAP status and application servers", "RFC and Gateway status", "STMS",
            "Database status and backup", "Printers and AL11", "SNC and certificates",
            "Performance indicators", "Backup/recovery evidence",
            "Database synchronization/switchover evidence", "Functional transaction evidence",
            "Approvals and Go/No-Go decision"]
    out.append('<div class="grid g3">' + "".join(
        '<div class="card"><h4 style="font-size:13px">%s</h4></div>' % e(c) for c in cats) + "</div>")
    out.append(h3("13.3", "Recommended evidence record"))
    out.append(table(["ID", "Validation area", "Source evidence", "Target evidence", "Result / action"],
                     [[str(i), "", "", "", ""] for i in range(1, 9)],
                     caption="Evidence register template", widths=["6%", "24%", "24%", "24%", "22%"], cls="plain"))
    out.append(h3("13.4", "Naming and storage convention"))
    out.append(para("Adopt one convention across the programme so that evidence can be found during a 02:00 cutover call without "
                    "opening files:"))
    out.append(cmd(["&lt;SID&gt;_&lt;PHASE&gt;_&lt;CHECK&gt;_&lt;SOURCE|TARGET&gt;_&lt;YYYYMMDD-HHMM&gt;.&lt;ext&gt;",
                    "",
                    "<span class='c'># examples</span>",
                    "PRD_PRECUT_SM59_SOURCE_20261002-1015.pdf",
                    "PRD_CUTOVER_R3TRANS_TARGET_20261005-0212.log",
                    "PRD_CUTOVER_SCN_BOTH_20261005-0140.png",
                    "PRD_HYPER_ST03N_TARGET_20261007-0900.pdf"]))
    out.append(bullets([
        "Store per the project retention and data-handling rules — no production data in unapproved locations, personal drives or chat.",
        "Attach evidence to the change/Jira record at the gate it supports, not in a batch at the end.",
        "Capture full output. A cropped success line proves nothing about what else was on the screen.",
        "Where evidence contains credentials, secrets or personal data, redact before storing and note that redaction occurred.",
        "Keep the evidence pack indexed by checklist item so a reviewer can jump from “SNC” to the SNC proof in one step."]))
    out.append(h3("13.5", "Documentation set produced by a migration"))
    out.append(table(["Document", "Owner", "Purpose"],
                     [["Source baseline pack", "Basis / migration", "Reference for every comparison and for hypercare triage"],
                      ["Build sheet (approved)", "Basis + automation", "The provisioning input and the validation reference"],
                      ["Infrastructure validation record", "Basis / migration", "Proof that what was built matches what was approved"],
                      ["Backup/recovery test record", "Basis + DBA", "Proof the recovery path works before it is needed"],
                      ["Validation workbooks (Sections 12)", "Executing engineer", "Check-by-check results with evidence references"],
                      ["Cutover runbook and log", "Basis / migration + PMO", "What was planned, what was done, at what time, by whom"],
                      ["Go/No-Go pack and decision record", "PMO", "The evidence set and the named approvals behind the decision"],
                      ["Hypercare issue log", "Hypercare lead", "Issues, classification (migration vs pre-existing), owners, closure"],
                      ["Handover pack to BAU", "Basis / migration", "Final state, known issues, deferred items, contacts, evidence archive"]],
                     caption="Documentation set", widths=["28%", "20%", "52%"]))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s14_ownership():
    out = [section("ownership", "14", "Ownership and operating model",
                   kick="Section 14 · Reference",
                   lead="The training concluded with an ownership model intended to prevent conflicting changes and unclear "
                        "accountability. Technology rarely fails a migration on its own; uncoordinated people do.")]
    out.append(h3("14.1", "Ownership model"))
    out.append(steps([
        "Complete the training and review the documentation.",
        "Clear technical doubts before taking ownership — an unasked question becomes a cutover incident.",
        "Assign individual SIDs/systems to owners.",
        "Assign a guide/support person for each owner.",
        "The assigned owner remains accountable for the system.",
        "Avoid multiple people independently modifying the same assigned system.",
        "Consolidate the training documentation/MOM after completion.",
        "Circulate the finalized material after confirmation/sign-off."]))
    out.append(box("key", "Ownership principle",
                   para("One accountable owner per assigned system, with a defined guide/support path and controlled changes. "
                        "Accountability does not mean doing everything alone — it means being the person who knows the state of the "
                        "system and who authorises changes to it.")))
    out.append(h3("14.2", "System ownership register"))
    out.append(table(["SID", "System / description", "Owner (accountable)", "Guide / support", "Backup owner", "Status"],
                     [["", "", "", "", "", ""] for _ in range(6)],
                     caption="Ownership register template", widths=["10%", "26%", "18%", "18%", "16%", "12%"], cls="plain"))
    out.append(h3("14.3", "Typical collaboration model"))
    out.append(table(["Team", "Owns", "Consulted on"],
                     [["Basis / migration", "SAP validation, migration coordination and technical handover", "Everything SAP-side; chairs the technical bridge"],
                      ["DBA", "Database migration, synchronization, backup/recovery and database validation", "Storage sizing, snapshot strategy, DB parameters"],
                      ["Linux", "OS configuration, services, file systems, UID/GID and reboot coordination", "Auto-start design, kernel tuning, reboot sequencing"],
                      ["Network / IPAM / DNS", "IP changes, hostname resolution, CNAME and connectivity", "TTL reduction, resolver design, firewall and security groups"],
                      ["Application / functional", "Business transactions and application validation", "Test scripts, data readiness, user communication"],
                      ["Automation / cloud", "AWS infrastructure provisioning and configuration automation", "Build-sheet feasibility, tagging, CMDB automation"],
                      ["Security / AD", "Credentials, SSO/SNC/certificates and security dependencies", "Certificate reissue, privileged access, audit requirements"],
                      ["Project management / stakeholders", "Approvals, Go/No-Go and change governance", "Window scheduling, risk acceptance, communication"]],
                     caption="Collaboration model", widths=["20%", "44%", "36%"]))
    out.append(h3("14.4", "Escalation path"))
    out.append(table(["Severity", "Definition", "Route", "Response expectation"],
                     [["S1 — Critical", "Cutover blocked, system unavailable, data at risk, or rollback decision required", "Bridge → module owner → programme lead → stakeholders immediately", "Immediate; decision within the agreed checkpoint interval"],
                      ["S2 — High", "A gate cannot be passed; a validation item fails with no workaround", "Module owner → accountable team lead; logged in the change record", "Same day, inside the window if one is open"],
                      ["S3 — Medium", "Deviation with a workaround; deferrable to a later checkpoint", "Owning team; tracked in the deviation log", "Before the next gate"],
                      ["S4 — Low", "Cosmetic, documentation, or non-blocking observation", "Deviation log; closed during hypercare", "Hypercare window"]],
                     caption="Escalation model", widths=["14%", "38%", "30%", "18%"]))
    out.append(box("warn", "Change control does not pause for a migration",
                   para("Every change made during build, validation and cutover is still a change: it needs an owner, a record and, "
                        "where the process requires it, an approval. The cutover change record is the umbrella — but it must list what "
                        "was done, not merely that a cutover happened.")))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s15_playbook():
    out = [section("playbook", "15", "Troubleshooting playbook and common failure modes",
                   kick="Section 15 · Reference",
                   lead="The failures that recur across SAP migrations, with the first diagnostic question for each. Use this "
                        "before changing anything: most of these are resolved by finding the cause, not by adjusting a parameter.")]
    modes = [
        ("SAP does not auto-start after reboot", "Section 7.1",
         ["Service enabled but exit code non-zero (127 / 255 / other)",
          "SAP starts manually as <code>&lt;sid&gt;adm</code> but not from the service",
          "Instance starts but never registers in <code>SM51</code>"],
         ["Read the service journal and the SAP start log before retrying.",
          "Check boot ordering: file systems mounted, network up, virtual IP owned, database reachable.",
          "For 127: path, environment and shared libraries. For 255: the SAP-side trace (<code>dev_disp</code>, <code>dev_ms</code>, <code>dev_w0</code>).",
          "Confirm the cluster/HA manager is not fighting the local service for the same resource."],
         "Coordinate the reboot with the Linux team, and rehearse it before cutover — never for the first time in the window."),
        ("R3trans -d does not return 0000", "Section 10.2",
         ["Database not reachable or not open",
          "Wrong credentials, missing user, or wallet/keystore problem",
          "Library or DB client (for example the Oracle client / HANA client) mismatch",
          "<code>/etc/hosts</code> or <code>/etc/services</code> pointing at the source",
          "Database name or SID changed without updating SAP configuration"],
         ["Read <code>trans.log</code> — it names the failing step.",
          "Test the DB connection independently of SAP (listener/service check, DB client connection).",
          "Verify the DB host entry and the SAP profile's database parameters.",
          "Confirm the DB client version and library path match the target design."],
         "Do not start SAP until this returns 0000; starting it first buries the real error under hundreds of secondary messages."),
        ("Interface fails after migration but worked before", "Sections 4.4, 7.3",
         ["RFC destination points at an old hostname/IP",
          "Gateway or message-server connection blocked by a security group or firewall",
          "Certificate, SNC or credential change on either side",
          "Middleware endpoint not repointed",
          "The interface was already failing before migration (baseline)"],
         ["Check the baseline record first: was it working before?",
          "Test the destination in <code>SM59</code> and read the returned error class.",
          "Check <code>SMGW</code> for the connection and for missing registrations.",
          "Validate name resolution and the network path from the SAP host, not from your laptop."],
         "If the baseline shows it was already failing, classify it as a pre-existing condition and route it to BAU with the evidence."),
        ("Permission denied on SAP or interface directories", "Section 7.2",
         ["UID/GID mismatch between source and target",
          "Ownership not preserved by the copy or the rsync",
          "NFS export with root-squash or a different owner mapping",
          "EFS mount with different default ownership"],
         ["Compare numeric UID/GID, not just user names.",
          "Check the ownership of the parent directory and the mount options.",
          "For NFS/EFS, verify the export permission model and squashing behaviour."],
         "Fix the ID mapping rather than chmod-ing the symptom; a broad permission change creates a security finding."),
        ("HANA recovery fails or hangs", "Section 6.4",
         ["Backup backend not reachable, or permissions insufficient",
          "Configuration files missing or inconsistent with the source topology",
          "Wrong recovery context (SystemDB versus tenant)",
          "Insufficient storage or memory on the target",
          "Log or data volume path mismatch"],
         ["Read the recovery log and the nameserver/indexserver traces.",
          "Prove the S3/backend path with a manual read test before retrying.",
          "Confirm you are recovering the tenant from the correct system context.",
          "Verify the INI/topology files describe the target, not the source."],
         "This is why recovery is tested before cutover. A first-time recovery attempt during the window is a rollback decision waiting to happen."),
        ("Database sizes do not match the source baseline", "Section 7.4",
         ["Tablespace not recovered or not extended",
          "Archive/log volume difference after the migration",
          "Compression, storage class or block-size difference on the target",
          "Growth since the baseline was taken"],
         ["Compare per tablespace, not only the total.",
          "Check the recovery log for skipped or truncated datafiles.",
          "Reconcile object counts for a sample of large tables."],
         "A total that looks plausible can hide a missing tablespace; compare the composition."),
        ("Performance worse than baseline", "Section 8",
         ["Different workload mix or period compared",
          "Stale database statistics or a changed access path",
          "Memory configuration not matching the target sizing",
          "Network latency between application and database hosts",
          "Storage throughput or IOPS below the sizing assumption",
          "Instance type smaller than the sizing report specified"],
         ["Confirm you are comparing equivalent periods and load.",
          "Split the response time: DB, CPU, wait. Follow the dominant component.",
          "Measure app-to-DB latency and storage throughput against the design.",
          "Check whether database statistics were refreshed after the data move."],
         "Do not raise memory parameters first; find what is consuming the resource."),
        ("DNS still resolves to the source", "Section 9.5",
         ["CNAME or A record not updated, or updated in the wrong zone",
          "Stale <code>/etc/hosts</code> entry overriding DNS",
          "TTL still high, or a caching resolver holding the old record",
          "Private zone not associated with the target VPC"],
         ["Resolve from the affected host with <code>getent hosts</code> and <code>nslookup</code>.",
          "Check <code>/etc/hosts</code> explicitly.",
          "Verify which zone answers and whether the VPC association is correct.",
          "Prove it with a real connection test (<code>R3trans -d</code>), not by reading the record."],
         "Lower TTL ahead of cutover as designed, and clear the host-file entries as part of post-processing."),
        ("Certificate, SNC or SSO failure after migration", "Section 7.3",
         ["Certificate issued for the old hostname or domain",
          "Certificate expired during the project",
          "PSE/keystore not migrated, or migrated with wrong permissions",
          "SSO provider still pointing at the old URL",
          "SNC configuration mismatch between partners"],
         ["Check validity and the hostname/domain match in <code>STRUST</code>.",
          "Verify the PSE/keystore files exist with correct ownership.",
          "Test SNC handshake and SSO logon with a representative user, not an administrator account.",
          "Confirm the partner side is configured for the new endpoint."],
         "Certificate reissue has lead time with the issuing authority — raise it during preparation."),
        ("Transport or ChaRM problem after migration", "Sections 7.3, 10.3",
         ["Transport directory not synchronized, or permissions wrong",
          "Domain controller or route definition pointing at the old landscape",
          "TMS configuration not updated for the new hostnames",
          "ChaRM cycle state inconsistent after the move"],
         ["Validate <code>STMS</code>: domain, systems, routes, transport directory.",
          "Run a test import through the full route.",
          "Check ownership and permissions on the transport directory on every host."],
         "A transport route that only works in one direction is a common half-migrated landscape symptom."),
        ("Backup fails on the target", "Sections 6.3, 9.4",
         ["Bucket/path/policy not matching the backup configuration",
          "Agent not installed, not registered, or pointing at the old master server",
          "Credentials or IAM role missing on the new host",
          "Network path to the backup target blocked"],
         ["Check the backup log for the exact failing operation.",
          "Verify the agent inventory and registration against the source baseline.",
          "Test the backend path manually with the same identity the backup uses."],
         "The first backup on the target must succeed before the system is handed to BAU — no exceptions."),
        ("Job or Control-M scheduling gap", "Section 10.6",
         ["Jobs not released after cutover",
          "Control-M agent not reinstalled or not re-pointed",
          "Job definitions referencing old hostnames or paths",
          "Dependencies resumed out of order"],
         ["Compare the job list with the source baseline (<code>SM37</code> plus the scheduler).",
          "Confirm the agent is registered with the correct control.",
          "Resume in the agreed order with the job owners on the call."],
         "Resuming everything at once creates a self-inflicted load spike on go-live day."),
    ]
    for name, ref, syms, diags, tip in modes:
        body = "<h5>Symptoms</h5>" + bullets(syms)
        body += "<h5>First diagnostics</h5>" + bullets(diags)
        body += box("key", "Practical tip", para(tip))
        out.append("<details><summary><span class='qn'>!</span><span>%s</span>"
                   "<span style='font-weight:600;color:var(--faint);font-size:12px;padding-top:3px'>%s</span>"
                   "<span class='car'>▶</span></summary><div class='ans'>%s</div></details>"
                   % (e(name), e(ref), body))
    out.append(box("risk", "When to stop and roll back",
                   bullets([
                       "The database cannot be validated and the remaining window cannot absorb the diagnosis.",
                       "The rollback point is about to expire or be invalidated by the next step.",
                       "Data consistency cannot be proven (SCN mismatch, corruption found, missing tablespaces).",
                       "A dependency outside the project's control will not be ready before the business deadline.",
                       "The Go/No-Go gate lacks a required approval or an unexplained critical open item."])))
    out.append("</section>")
    return "".join(out)


def s16_lessons():
    out = [section("lessons", "16", "Key lessons and practical guidance",
                   kick="Section 16",
                   lead="Fifteen lessons carried out of the training sessions. Each one is short because the moment you need it "
                        "will not be a comfortable one.")]
    lessons = [
        ("Never assume auto-start works. Test it through an actual reboot.", "4, 7.1"),
        ("Always establish a source baseline before migration.", "4"),
        ("Use the approved build sheet as the central technical input.", "5.2"),
        ("Validate provisioned AWS infrastructure rather than assuming automation produced the expected result.", "5.3"),
        ("Keep CMDB, inventory and actual infrastructure aligned.", "5.5"),
        ("UID/GID mismatches can create permission and application issues.", "7.2"),
        ("Validate STMS, RFC, Gateway, certificates, printers and directories explicitly.", "7.3"),
        ("Obtain third-party RFC credentials before cutover when required.", "4.1, 10.3"),
        ("Test backup and recovery before the actual cutover.", "6.4"),
        ("Keep the source available until the required final backup activity is successfully completed.", "6.4"),
        ("Capture evidence at every important decision gate.", "13"),
        ("Do not classify a pre-existing source issue as a migration defect without evidence.", "4.4, 13"),
        ("Go/No-Go must be evidence-driven and supported by technical, functional and owner approvals.", "10.4"),
        ("Rollback readiness must be maintained until the migration is considered safe.", "9.3, 10.5"),
        ("During hypercare, compare actual issues with the pre-migration baseline.", "10.6"),
    ]
    out.append(table(["#", "Lesson", "Where it applies"],
                     [[str(i + 1), l, ref] for i, (l, ref) in enumerate(lessons)],
                     caption="Key lessons", widths=["5%", "76%", "19%"], cls="plain"))
    out.append(h3("16.1", "Anti-patterns the training warned against"))
    out.append(cards([
        ("Silent fixes", "Repairing something during cutover without recording it. It becomes an unapproved change nobody can explain later."),
        ("Assertion instead of evidence", "“It was working” with no timestamp, no output and no comparison to the baseline."),
        ("Automation absolution", "Assuming the automated build is correct because it completed. Completion is not correctness."),
        ("Parameter-first troubleshooting", "Raising memory, timeouts or buffer sizes before identifying what is consuming the resource."),
        ("Shared ownership", "Three engineers making independent changes to one SID during validation."),
        ("Compressed discovery", "Shortening discovery to protect the schedule, then paying for it in the cutover window."),
        ("Unrehearsed rollback", "A rollback plan that exists in a document but has never been executed or timed."),
        ("Late credential requests", "Third-party and middleware credentials requested in cutover week."),
        ("Cropped screenshots", "Evidence that shows only the success line and none of the context around it."),
        ("Hypercare amnesia", "Losing the baseline at go-live, so every pre-existing fault becomes a migration defect.")],
        cols=2, accent=True))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
QUIZ = [
    ("Why is a source baseline essential before migration?",
     "It provides the evidence used for target comparison and it is what allows you to distinguish migration-related failures "
     "from pre-existing issues. Without a baseline, every post-migration problem is arguable: you cannot prove whether the "
     "migration caused it, and you cannot prove that a fix is needed. The baseline covers OS, SAP, database, interfaces, "
     "directories, workload, memory, backup status and known failures — each with a timestamp."),
    ("What is the purpose of the build sheet?",
     "It is the approved system information used for target provisioning and for validating what was provisioned. It is prepared "
     "from the sizing report and architecture, peer-reviewed, finalised with the customer, and then used twice: as the input to "
     "automation, and as the reference the migration team validates the built environment against."),
    ("What is the difference between SystemDB and TenantDB?",
     "SystemDB provides central management and monitoring for the HANA system and holds the backup catalogue; TenantDB contains "
     "the application and data workload for a specific SAP system. They have separate login contexts and credentials, and both "
     "can reside on the same HANA server or VM. Neither is an HA component — high availability is a separate "
     "infrastructure-level design."),
    ("Why must backup and recovery be tested before cutover?",
     "To confirm that the backup destination, configuration, permissions and the recovery process actually work before they are "
     "needed under production pressure. The test also produces the evidence required at Gate 1 and gives you a realistic "
     "duration estimate for the cutover window."),
    ("What does SM59 validate?",
     "RFC destinations and their connectivity, including the relevant TCP/IP, HTTP and external connections. In a migration it is "
     "used twice: to enumerate the interface baseline before the move, and to prove each destination still works after it — "
     "compared against that baseline, so pre-existing failures are not mistaken for migration defects."),
    ("What is the role of STMS?",
     "Transport landscape management: the transport domain and its controller, the systems in the landscape, the routes between "
     "them, and the transport directory. After migration you validate all four and prove the route works with a test import — a "
     "landscape that only transports in one direction is a common half-migrated symptom."),
    ("Why are UID/GID checks important?",
     "Because mismatches cause permission problems, inter-server communication issues, SAP file-access problems and application "
     "failures that appear far from their cause. Compare the numeric IDs for <code>sapadm</code>, <code>&lt;sid&gt;adm</code>, "
     "the database users and their groups — not just the names, which can be identical while the numbers differ."),
    ("What is the purpose of comparing Oracle SCN values?",
     "To verify synchronization and data consistency between the source primary and the target standby before the switchover. "
     "Matching SCN values (with no apply gap) are the evidence that no committed data will be lost when the roles are swapped, "
     "and they are attached to the change ticket for approval."),
    ("Why is an AWS disk-level snapshot useful during Oracle cutover?",
     "It provides a rollback recovery point before subsequent migration activities. Taken after the standby is synchronized and "
     "before the role change, it lets you restore the target to a known consistent state if the switchover or the following "
     "validation fails."),
    ("What is the purpose of the Go/No-Go decision?",
     "To ensure the system is released only after the required technical, functional and owner approvals are in place, with "
     "evidence and confirmed rollback readiness. It is a governance control, not a formality: a No-Go with documented reasons is "
     "a successful use of the gate."),
    ("What should happen if a critical issue prevents safe cutover?",
     "Execute the agreed rollback procedure — the one prepared and rehearsed before the window. Restore the snapshot or recover "
     "the source, revert DNS/CNAME, restart the source, re-validate connectivity, then record the reason, the evidence and the "
     "path back into the incident and change process."),
    ("What is the stated hypercare period in the final training?",
     "15 days after successful go-live. During that period, users are unlocked, background jobs and Control-M activities are "
     "resumed with the owning teams, remaining EDG/SAProuter configuration is completed, and every issue is classified as "
     "migration-related or pre-existing and routed to the responsible support team."),
    ("Why must <code>R3trans -d</code> return 0000 before SAP is started?",
     "<em>Added during the review pass.</em> Because it is the definitive SAP-to-database connectivity check. Starting SAP with a "
     "failing database connection generates hundreds of secondary errors in the work process and dispatcher traces that hide the "
     "real cause and consume window time; diagnosing <code>trans.log</code> first is faster and safer."),
    ("Why is a real reboot required to validate auto-start, and what do return codes 127 and 255 indicate?",
     "<em>Added during the review pass.</em> An enabled, active service can still fail at boot because of dependency ordering — "
     "late-mounting file systems, network not yet up, a cluster-owned virtual IP, or an unreachable database. Only a reboot proves "
     "the sequence. A return code of 127 indicates a missing command or unresolved shared library (path, environment, library "
     "dependency); 255 is a generic failure from the start script or SAP program and must be diagnosed from the service journal "
     "and the SAP traces."),
    ("What is the difference between an Oracle Data Guard switchover and a failover?",
     "<em>Added during the review pass.</em> A switchover is a planned, reversible role swap in which both databases end in valid "
     "roles and you can switch back; it is the migration mechanism. A failover is a disaster-recovery action taken when the primary "
     "is lost: the standby becomes primary and the old primary typically needs rebuilding. Migration runbooks must never describe "
     "a failover when they mean a switchover."),
    ("How should a pre-existing failure be handled during validation and hypercare?",
     "<em>Added during the review pass.</em> Record it in the source baseline with evidence and a timestamp, classify it as a "
     "pre-existing condition, and route it to BAU support rather than absorbing it as a migration defect. If it is fixed during the "
     "migration, record the fix as a change — an unrecorded fix is an unapproved change that nobody can explain later."),
]


def s17_quiz():
    out = [section("quiz", "17", "Final knowledge check",
                   kick="Section 17",
                   lead="Sixteen questions. The first twelve are from the source training; the last four were added during the "
                        "professional review to cover points the modules rely on. Answers are hidden until opened — this is a "
                        "self-test, not a reading exercise.")]
    out.append('<div class="ck-tools no-print">'
               '<button class="btn" data-expand="1" data-scope="#quiz">Reveal all answers</button>'
               '<button class="btn" data-expand="0" data-scope="#quiz">Hide all answers</button></div>')
    out.append(qa([(q, para(a)) for q, a in QUIZ], "quiz"))
    out.append(h3("17.1", "Scoring guidance for trainers"))
    out.append(table(["Score", "Interpretation", "Recommended action"],
                     [["14–16", "Ready to take ownership of a system in a migration wave.", "Assign a SID and a guide; proceed to supervised execution."],
                      ["11–13", "Sound understanding with gaps.", "Re-read the modules behind the missed questions; re-test before assignment."],
                      ["8–10", "Partial readiness.", "Paired execution only, with the guide performing the validation and the trainee observing."],
                      ["Below 8", "Not yet ready for independent migration work.", "Repeat the training; focus on Modules 1, 4 and 7 and the evidence model."]],
                     caption="Scoring bands", widths=["12%", "40%", "48%"], cls="plain"))
    out.append(box("key", "Practical assessment suggestion",
                   para("A written check tests recall; migration work tests judgement. Pair this quiz with a practical exercise: "
                        "give the trainee a source baseline pack and a target system, and ask them to complete one Section 12 "
                        "checklist, produce the evidence, classify three seeded deviations correctly, and present the result as if "
                        "at a Go/No-Go gate.")))
    out.append("</section>")
    return "".join(out)


# --------------------------------------------------------------------------- #
def s_app_a():
    out = [section("app-a", "A", "Appendix A — Source training coverage",
                   kick="Appendix A", cls="nobreak",
                   lead="The supplied consolidated material included multiple training/MOM sections. This handbook reorganises "
                        "them into a reusable training format; the mapping below preserves traceability to the source.")]
    out.append(table(["Source training / MOM section", "Content covered", "Mapped to"],
                     [["Final checklist session", "Consolidated end-of-project checklist review and open items", "Sections 10, 12"],
                      ["SAP-to-AWS migration checklist", "Preparation, discovery, sizing, architecture, build and validation steps", "Sections 3, 4, 5, 7"],
                      ["HANA MDC and recovery", "SystemDB/TenantDB, pre-checks, S3 backup backend, recovery sequence", "Section 6"],
                      ["SAP validation / monitoring / troubleshooting", "OS, SAP and database validation; ST02, ST03/ST03N, STAD, RZ10/RZ11", "Sections 7, 8"],
                      ["Oracle migration and switchover", "Data Guard, SCN, snapshot, DBVERIFY, RMAN, DNS/IPAM", "Section 9"],
                      ["Cutover and go-live", "Shutdown, post-processing, functional validation, Go/No-Go, rollback", "Section 10"],
                      ["Ownership and evidence model", "System ownership, guides, evidence lifecycle and categories", "Sections 13, 14"]],
                     caption="Source coverage map", widths=["30%", "46%", "24%"]))
    out.append(box("key", "What changed during consolidation",
                   bullets([
                       "Material was re-sequenced to follow the migration lifecycle rather than the order in which sessions were delivered.",
                       "Repeated content across MOM sections was merged, keeping the most complete version of each instruction.",
                       "Implicit knowledge (why a step matters, what a failure looks like) was made explicit for a training audience.",
                       "Source terminology was preserved verbatim, including client-specific terms, which are tagged " + pill("source term", "a") + " throughout.",
                       "No technical value from the source was silently altered. Corrections and clarifications are listed in Appendix D."])))
    out.append("</section>")
    return "".join(out)


def s_app_b():
    out = [section("app-b", "B", "Appendix B — Training completion record",
                   kick="Appendix B", cls="nobreak",
                   lead="One row per module per attendee. Sign-off means the attendee has completed the material and can answer "
                        "the associated knowledge-check questions.")]
    mods = ["Preparation &amp; Discovery", "AWS Build &amp; Architecture", "HANA Backup &amp; Recovery",
            "SAP Validation &amp; Monitoring", "Performance &amp; Troubleshooting", "Oracle &amp; Cutover",
            "Go-Live &amp; Hypercare", "Evidence &amp; Ownership model"]
    rows = [[m, "", "", "", ""] for m in mods]
    out.append(table(["Module", "Completed by", "Date", "Trainer sign-off", "Knowledge check score"], rows,
                     caption="Completion record — attendee copy", widths=["30%", "20%", "14%", "18%", "18%"], cls="plain"))
    out.append(h3("B.1", "Session register"))
    out.append(table(["Session", "Date", "Duration", "Trainer", "Attendees", "Topics covered", "Actions from the session"],
                     [["" for _ in range(7)] for _ in range(6)],
                     caption="Session register (MOM consolidation source)", widths=["12%", "10%", "10%", "14%", "16%", "20%", "18%"], cls="plain"))
    out.append(h3("B.2", "Competency confirmation"))
    out.append(table(["Competency", "Assessed by", "Result", "Date"],
                     [["Can build and use a source baseline pack", "", "", ""],
                      ["Can validate a provisioned AWS target against a build sheet", "", "", ""],
                      ["Can perform SAP Basis post-migration validation end to end", "", "", ""],
                      ["Can execute and interpret the HANA backup/recovery test", "", "", ""],
                      ["Can support an Oracle Data Guard switchover and validate the new primary", "", "", ""],
                      ["Can perform cutover post-processing and interpret R3trans -d", "", "", ""],
                      ["Can triage a performance issue to the correct owning team", "", "", ""],
                      ["Can present evidence at a Go/No-Go gate", "", "", ""],
                      ["Can classify a hypercare issue against the baseline", "", "", ""]],
                     caption="Practical competency confirmation", widths=["48%", "20%", "16%", "16%"], cls="plain"))
    out.append("</section>")
    return "".join(out)


GLOSSARY = [
    ("AAS", "Additional Application Server. Extra SAP dialog instance added for capacity."),
    ("ADPU", "Sign-off/quality-assurance step referenced in the source training. " + "Client-specific — confirm the exact meaning in the project glossary."),
    ("AL11", "SAP transaction for browsing SAP directories; used to validate directory presence, content and permissions."),
    ("Application-consistent snapshot", "A snapshot taken with the application/database quiesced, giving a transactionally consistent recovery point."),
    ("ASCS", "ABAP SAP Central Services: message server and enqueue service. A single point of failure unless made highly available."),
    ("Backint", "SAP's backup interface standard; a certified Backint agent lets SAP/HANA back up directly to a target such as S3."),
    ("BAU", "Business As Usual — the permanent support organisation that receives the system after hypercare."),
    ("Broker (Data Guard)", "Oracle Data Guard Broker: a management layer that automates and standardises Data Guard configuration and role changes."),
    ("Build sheet", "The approved technical specification used to provision the target and to validate what was built."),
    ("CNAME", "DNS record type that aliases one name to another; repointed during cutover to aim a hostname at the new target."),
    ("CMDB / CI", "Configuration Management Database and Configuration Item: the inventory record of a system and its relationships (ServiceNow in this training)."),
    ("Cooldown", "Pre-cutover period of reduced activity or frozen changes, used to stabilise the source before the move."),
    ("Crash-consistent snapshot", "A snapshot of the volumes as they are at a point in time, without application quiescing."),
    ("DB02", "SAP transaction for database space, tablespace and (database-dependent) backup information."),
    ("DBVERIFY / dbv", "Oracle utility that checks datafiles for physical block corruption."),
    ("EDG", "Term used in the source training for a remaining configuration item completed after go-live. Client-specific — confirm in the project glossary."),
    ("EM / Extended memory", "SAP extended memory: shared memory used first for user context before heap/private memory."),
    ("Enqueue", "SAP's logical lock mechanism; enqueue contention appears as wait time."),
    ("ERS / CRS", "Enqueue Replicator Service (and the equivalent central-services replication component): the partner of ASCS in an HA design."),
    ("Failover", "Unplanned promotion of a standby after primary failure; a disaster-recovery action, not reversible like a switchover."),
    ("FSx for NetApp ONTAP", "AWS managed file service offering NFS with ONTAP semantics; an alternative to EFS where NFS features or performance are required."),
    ("Go/No-Go", "The formal decision gate before release, based on evidence and named approvals."),
    ("Heap / private memory", "Process-private SAP memory used when extended memory is exhausted; the work process mode becomes PRIVATE."),
    ("HSR", "HANA System Replication: the mechanism that keeps a secondary HANA database synchronized with a primary."),
    ("Hypercare", "The elevated-support period after go-live — 15 days in this training."),
    ("ICM / SMICM", "Internet Communication Manager: the SAP component handling HTTP/HTTPS; SMICM is its administration transaction."),
    ("IPAM", "IP Address Management: the system of record for address allocation and DNS-related changes."),
    ("Managed recovery", "The Oracle standby process that applies received redo to keep the standby current."),
    ("MBox", "Integration component named in the source training. Client-specific — confirm in the project glossary."),
    ("MDC", "Multiple Database Containers: the HANA architecture with one SystemDB and one or more TenantDBs."),
    ("MOM", "Minutes of Meeting — one of the source inputs to this handbook."),
    ("NetWeaver", "SAP's application platform; the release and SP level are part of the source inventory."),
    ("Observer node", "An independent node that monitors a Data Guard configuration, used for automatic failover designs."),
    ("OEM / OBM", "Monitoring/backup agents referenced in the source training (for example Oracle Enterprise Manager agent). Confirm the exact products in the project inventory."),
    ("PAS", "Primary Application Server: the first SAP dialog instance, installed with the central instance components."),
    ("PSE", "Personal Security Environment: the SAP keystore file holding certificates and keys used for SNC/SSL."),
    ("R3trans -d", "Command-line check of SAP-to-database connectivity; a return code of 0000 means success."),
    ("RMAN", "Oracle Recovery Manager: backup, restore and recovery tooling."),
    ("Roll area / roll memory", "Per-work-process SAP memory holding rolled user context; roll-in/roll-out moves context to and from it."),
    ("RPO / RTO", "Recovery Point Objective (how much data you may lose) and Recovery Time Objective (how long you may be down)."),
    ("sapadm / &lt;sid&gt;adm", "The SAP administrative OS users; their UID/GID must match across hosts in a landscape."),
    ("SAProuter", "SAP's proxy component for controlled network access to and from an SAP system."),
    ("SCN", "System Change Number: Oracle's logical point-in-time marker, compared between source and target to prove synchronisation."),
    ("SID", "SAP System ID: the three-character identifier of an SAP system."),
    ("SNC", "Secure Network Communications: SAP's authentication and encryption layer for RFC/diag connections."),
    ("SPAD / SP01", "Spool administration and spool request monitoring."),
    ("ST02 / ST03 / ST03N / STAD", "Memory and buffer monitoring, workload statistics (legacy and current), and the detailed statistical records behind them."),
    ("STMS / TMS", "Transport Management System: the transport domain, systems, routes and transport directory."),
    ("Switchover", "A planned, reversible Oracle Data Guard role swap; the migration mechanism used in this training."),
    ("SystemDB / TenantDB", "The HANA management container and the application/data container respectively."),
    ("THP", "Transparent Huge Pages: a Linux memory feature that must be configured according to the SAP requirement for HANA hosts."),
    ("Type 3 RFC", "An SAP-to-SAP (ABAP-to-ABAP) RFC connection type; the source training refers to updating its passwords after migration."),
    ("Virtual hostname / virtual IP", "A hostname and address that can move between hosts; used so SAP addressing does not change when the target changes."),
]


def s_app_c():
    out = [section("app-c", "C", "Appendix C — Glossary and acronyms",
                   kick="Appendix C", cls="nobreak",
                   lead="Terms used in this handbook. Client-specific terms carried over from the source material are marked and "
                        "should be confirmed against the project glossary before use.")]
    half = (len(GLOSSARY) + 1) // 2
    out.append('<div class="grid g2">')
    for chunk in (GLOSSARY[:half], GLOSSARY[half:]):
        out.append("<div>" + "".join(
            '<p style="margin:0 0 10px"><b style="color:var(--navy)">%s</b> — <span style="font-size:13.4px">%s</span></p>'
            % (t, d) for t, d in chunk) + "</div>")
    out.append("</div>")
    out.append("</section>")
    return "".join(out)


def s_app_d():
    out = [section("app-d", "D", "Appendix D — Technical review and vetting notes",
                   kick="Appendix D", cls="nobreak",
                   lead="This handbook was reviewed for technical accuracy and professional consistency. Every editorial change "
                        "and every flagged ambiguity is recorded here so a reviewer can see exactly what was preserved from the "
                        "source and what was clarified.")]
    out.append(h3("D.1", "Vetting summary"))
    out.append(kpis([(str(STATS["tables"]), "tables reviewed", "Every table, checklist and statement checked for technical accuracy"),
                     ("12", "corrections", "Technical clarifications added where the source was imprecise"),
                     ("9", "terms flagged", "Client-specific or unverifiable terms retained but marked"),
                     ("4", "quiz questions added", "Review-pass questions covering points the modules rely on")]))
    out.append(h3("D.2", "Technical corrections and clarifications"))
    out.append(table(["#", "Source statement", "Review finding", "Action taken"],
                     [["1", "“Run R3TRANS -d and confirm return code 0000.”",
                       "Correct, but the source did not say what to do when the code is not 0000, nor which codes appear in practice.",
                       "Retained the 0000 requirement; added the diagnostic sequence (read <code>trans.log</code>, test the DB connection independently) and common non-zero codes with a note to confirm them against the release in use. Section 10.2."],
                      ["2", "“Service status Active, return code 0 … return codes such as 127 or 255 were discussed.”",
                       "Accurate but incomplete: 127 and 255 are shell/service-level codes whose meaning depends on the start mechanism.",
                       "Presented as a diagnostic table (0 = success, 127 = command/library not found, 255 = generic failure) with the explicit caveat that the mapping is a starting point. Section 7.1."],
                      ["3", "“STAD detailed analysis” listed alongside ST03/ST03N without distinction.",
                       "ST03/ST03N are aggregate workload statistics; STAD shows the individual statistical records behind them. Conflating them leads to wrong triage.",
                       "Added the aggregate-versus-record distinction and the drill-down path. Sections 8.3, 8.4."],
                      ["4", "“ST03 is used for workload analysis.”",
                       "ST03N is the current workload transaction in modern releases; ST03 is legacy but still referenced in runbooks.",
                       "Both retained, with a footnote explaining the relationship so the source terminology stays recognisable. Sections 8.3, 11.1."],
                      ["5", "“SystemDB and TenantDB … should not be confused with HA server architecture.”",
                       "Correct and important, but the source did not name the actual HA mechanism.",
                       "Added HANA System Replication (HSR) as the HA mechanism, clearly separated from the container model. Sections 6.1, Figure 4."],
                      ["6", "S3 as the HANA backup backend, mechanism unnamed.",
                       "The mechanism (certified Backint agent versus file-based backup) changes the configuration, permissions, logs and restore syntax.",
                       "Flagged for confirmation with the project HANA standard; both options described. Section 6.3."],
                      ["7", "“The target standby is activated as the new primary.”",
                       "Correct for the scenario, but the source used switchover and activation language interchangeably, and did not distinguish it from failover.",
                       "Added the switchover-versus-failover distinction and a vocabulary table; noted that command syntax belongs to the project runbook. Section 9.1, Figure 5."],
                      ["8", "“Take the required AWS disk-level snapshot before subsequent activities.”",
                       "Correct, but timing and consistency type matter: a snapshot taken before synchronisation completes, or a crash-consistent snapshot where an application-consistent one is required, is not a reliable recovery point.",
                       "Specified the timing (after synchronisation, before role change) and flagged the consistency decision as a DBA-lead call. Section 9.3."],
                      ["9", "“Extended Memory → if exhausted → Heap/Private Memory.”",
                       "Correct as a general relationship, but incomplete without roll area and paging, which is where the user-visible symptom often appears.",
                       "Extended the model to roll, EM, heap/private and paging, and added the “find the cause, don't raise the parameter” rule. Section 8.1, Figure 7."],
                      ["10", "“Approximately 1200 ms response time and 40% average database request time.”",
                       "These are discussion values, not standards. Quoting them without qualification risks them being configured as production thresholds.",
                       "Retained verbatim with a prominent caution to validate against the applicable SAP and client baseline. Section 8.4."],
                      ["11", "“Identify NFS dependencies and determine whether the share is maintained/copied or migrated to AWS EFS.”",
                       "Correct, but EFS is not always the right target for SAP NFS workloads; performance characteristics and NFS feature requirements may point elsewhere.",
                       "Added FSx for NetApp ONTAP as an alternative in the glossary and a note to confirm performance requirements per share. Sections 4.3, Appendix C."],
                      ["12", "“Provide 15 days of hypercare.”",
                       "Client/programme-specific commitment rather than an industry standard.",
                       "Retained as stated, and labelled explicitly as the period stated in the source training. Sections 10.6, 17 (Q12)."]],
                     caption="Corrections and clarifications", widths=["4%", "24%", "34%", "38%"]))
    out.append(h3("D.3", "Terms preserved but flagged for confirmation"))
    out.append(table(["Term", "Where used", "Why it is flagged"],
                     [["ADPU", "Section 10.4", "Sign-off step named in the source training; the exact expansion and scope are client-specific."],
                      ["MBox", "Section 10.3", "Integration component named in the source; not a generally documented product name in this context."],
                      ["OEM / OBM", "Sections 4.3, 9.3", "Used together in the source for external agents; OEM is most likely Oracle Enterprise Manager, OBM is unclear."],
                      ["EDG", "Section 10.6", "Post-go-live configuration item named in the source; expansion is client-specific."],
                      ["Type 3 RFC passwords", "Section 10.3", "Type 3 is the ABAP-to-ABAP RFC connection type; the password-update requirement depends on the project's credential handling."],
                      ["saproot.sh / Oracle root scripts", "Section 10.2", "Correct in principle; exact script names vary by database, platform and SAP release."],
                      ["webMethods / MuleSoft", "Sections 10.3, 13", "Named middleware in the source landscape; the applicable set is project-specific."],
                      ["Chef", "Sections 5.4, 11.2", "Configuration-management tool named in the source; the automation standard may differ by programme."],
                      ["≈1200 ms / ≈40% DB time", "Section 8.4", "Discussion values from the source training, not validated production thresholds."]],
                     caption="Flagged terms", widths=["18%", "18%", "64%"]))
    out.append(box("warn", "Open items for the programme to close",
                   bullets([
                       "Confirm the exact meaning of ADPU, MBox, EDG and OBM in the project glossary, then remove the flags.",
                       "Confirm the HANA backup mechanism (Backint agent versus file-based) and record the configuration file set.",
                       "Confirm whether the pre-switchover snapshot must be application-consistent, and record the decision.",
                       "Validate the performance thresholds against the client baseline before they are used for alerting.",
                       "Confirm the NFS target per share (EFS, FSx for NetApp ONTAP, or copy/maintain) against performance requirements.",
                       "Confirm the SAP license reissue path and hardware-key change procedure for each migrated system.",
                       "Replace the placeholder reviewer and approver names in Section 0.5 before the document is issued externally."])))
    out.append(h3("D.4", "Review method"))
    out.append(steps([
        "Structural review: re-sequenced the source material to follow the migration lifecycle and removed duplication across MOM sections.",
        "Technical review: verified each transaction, command, concept and sequence against standard SAP Basis, HANA, Oracle and AWS practice; recorded findings in D.2.",
        "Terminology review: preserved source wording, tagged client-specific terms, and added a glossary (Appendix C).",
        "Consistency review: cross-checked every cross-reference, checklist item, figure and quiz question against the module text.",
        "Usability review: added entry/exit criteria, role reading paths, expected outputs, a troubleshooting playbook and an escalation model.",
        "Diagram review: each figure was generated programmatically and checked geometrically for text overflow and container fit before publication."]))
    out.append(h3("D.5", "Quality-control results"))
    out.append(table(["Control", "Method", "Result for v1.0"],
                     [["Diagram geometry", "Every SVG text node measured against its container and the viewBox (<code>training/tools/svg_qa.py</code>)", "0 overflow issues across %d figures" % STATS["figures"]],
                      ["Markup integrity", "HTML parsed and tag balance, duplicate ids and anchors verified at build time (<code>build_handbook.py</code> QC pass)", "Clean: 0 broken anchors, 0 duplicate ids"],
                      ["Figure and table cross-references", "All internal <code>#</code> anchors resolved programmatically", "All resolve"],
                      ["Checklist integrity", "Unique persisted ids, status capture and progress metering verified in the generated HTML", "%d checklists, %d items" % (STATS["checklists"], STATS["items"])],
                      ["Source traceability", "Every source training section mapped to a handbook section (Appendix A)", "7 of 7 mapped"],
                      ["Terminology consistency", "Glossary coverage of the acronyms and terms used in the body (Appendix C)", "%d terms" % STATS["glossary"]],
                      ["Knowledge check", "Questions verified against the module text; four review-pass questions added", "%d questions" % STATS["quiz"]],
                      ["Word version parity", "DOCX rendered from the same HTML source; headings, tables, figures and checklists verified present", "26 top-level sections, 91 tables"]],
                     caption="QC results for this release", widths=["24%", "48%", "28%"]))
    out.append("</section>")
    return "".join(out)


def s_app_e():
    out = [section("app-e", "E", "Appendix E — Version control and change requests",
                   kick="Appendix E", cls="nobreak",
                   lead="This handbook is a controlled document. Raise corrections and additions through the change-request "
                        "record below so the next version reflects what the field actually learned.")]
    out.append(table(["CR #", "Raised by", "Date", "Section affected", "Description of the requested change", "Disposition", "Closed in version"],
                     [["" for _ in range(7)] for _ in range(6)],
                     caption="Change-request log", widths=["7%", "13%", "9%", "14%", "35%", "13%", "9%"], cls="plain"))
    out.append(h3("E.1", "Review cycle"))
    out.append(bullets([
        "Review this handbook after every migration wave, and at minimum every six months.",
        "Update it when a project runbook, SAP release, AWS service behaviour or client standard changes the guidance.",
        "Re-run the technical review (Appendix D method) whenever a module is materially changed.",
        "Retire superseded versions to the archive with their evidence packs; do not leave multiple live copies in circulation.",
        "Circulate the finalized material only after confirmation and sign-off, as required by the ownership model in Section 14."]))
    out.append(box("ok", "End of handbook",
                   para("Consolidated Training Material · 2026 · SAP Migration Training Handbook · Version 1.0 · "
                        "Internal — training use. Prepared from the consolidated training/MOM source document; primary trainer "
                        "Amit Prajapati.")))
    out.append("</section>")
    return "".join(out)
