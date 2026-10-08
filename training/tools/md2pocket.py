#!/usr/bin/env python3
"""Build the condensed field companion: SAP-Migration-Pocket-Reference-v1.0.docx

A short, print-friendly run-card extracted from the full handbook: cutover
sequence, the five validation checklists, quick references, return codes,
Oracle/HANA cards, evidence naming and escalation. Reuses the handbook's DOCX
emitters so formatting stays identical.

Usage:  <venv>/bin/python training/tools/md2pocket.py
"""

from __future__ import annotations

import os
import sys

from lxml import html as LH

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import htmlkit as K  # noqa: E402
import md2docx as M  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, "..", "handbook",
                                    "SAP-Migration-Pocket-Reference-v1.0.docx"))


def cover():
    out = [K.section("pcover", None, "SAP Migration — Field Pocket Reference",
                     kick="Condensed companion · v1.0 · Sept–Oct 2026",
                     lead="The one document to carry into a cutover bridge: the sequence, the checks, the "
                          "return codes and the decision gates. Full rationale, theory and evidence strategy "
                          "live in the SAP Migration Training Handbook v1.0 — this card deck does not replace it.")]
    out.append(K.table(["Field", "Value"],
                       [["Document ID", "SAP-MIG-TRN-PR-001"],
                        ["Companion to", "SAP-MIG-TRN-HB-001 v1.0 (Training Handbook)"],
                        ["Owner", "Amit Prajapati — primary trainer"],
                        ["Use", "Cutover bridge, validation desks, hypercare desk"],
                        ["Status", "Issued with handbook v1.0"]],
                       widths=[26, 74], cls="plain"))
    out.append(K.box("risk", "Three rules that override everything else on these pages",
                     K.para("1. Nothing advances past a gate without evidence and a named approval.",
                            "2. The source stays available until the required final backup activity succeeds.",
                            "3. If <code>R3trans -d</code> is not <code>0000</code>, SAP does not start.")))
    out.append(K.endsec())
    return "".join(out)


def s1_runcard():
    out = [K.section("pr-run", "1", "Cutover run-card", kick="Pocket reference · Section 1",
                     lead="Four lanes, one direction of travel. Each handover is announced on the bridge and "
                          "recorded in the change log with a timestamp.")]
    out.append(K.table(["APPLICATION", "DBA", "BASIS / MIGRATION", "FUNCTIONAL + PMO"],
                       [["1 Cooldown / ramp-up complete\n2 Application + web services stopped\n3 Handover to DBA confirmed",
                         "4 Final backup + AWS snapshot\n5 Switchover or HANA recovery\n6 DBVERIFY, RMAN, DB validation",
                         "7 rsync global directory; clean host/IPAM\n8 Profile parameters, kernel permissions, root scripts\n9 R3trans -d must return 0000\n10 Start SAP; validate SNC/SSO, Gateway, RFC",
                         "11 Business transaction tests, interfaces, printers, evidence"]],
                       widths=[25, 25, 30, 20], caption="Lane sequence"))
    out.append(K.cmd(["<span class='c'># the gate before SAP start</span>",
                      "su - &lt;sid&gt;adm",
                      "<span class='p'>R3trans -d</span>        <span class='c'># expect: R3trans finished (0000)</span>",
                      "<span class='p'>cat</span> trans.log     <span class='c'># first place to look if not 0000</span>",
                      "",
                      "<span class='c'># instance state without the GUI</span>",
                      "<span class='p'>sapcontrol</span> -nr &lt;nn&gt; -function GetProcessList",
                      "<span class='p'>sapcontrol</span> -nr &lt;nn&gt; -function GetSystemInstanceList"]))
    out.append(K.table(["Go/No-Go input", "Must be true to vote Go"],
                       [["Technical validation", "Module 4 + Module 6 checks complete, or formally deferred with owner, impact, date"],
                        ["Functional validation", "Named business transactions passed by the functional team"],
                        ["Evidence", "Source and target captured, compared, attached to the change record"],
                        ["Rollback readiness", "Snapshot / final backup verified; DNS rollback path defined; owner on the bridge"],
                        ["Approvals", "Basis, application, functional, system owner, PMO — recorded by name"],
                        ["Open risks", "Every item classified; no unexplained critical"],
                        ["Support readiness", "Hypercare roster, escalation path, ticket routing live"]],
                       widths=[26, 74], caption="Go/No-Go gate inputs"))
    out.append(K.box("warn", "Rollback path (executed on No-Go or an unsafe cutover)",
                     K.bullets([
                         "Restore the snapshot or recover the source; revert DNS/CNAME to the source.",
                         "Restart source database and SAP; re-validate connectivity (<code>R3trans -d</code>).",
                         "Announce decision, time and reason on the bridge; record evidence of the attempt.",
                         "Confirm with the business what data (if any) was created on the target."])))
    out.append(K.figure("d6-cutover", "", "<b>Figure 6.</b> Cutover execution sequence with the Go/No-Go decision "
                                          "and rollback path (from the handbook)."))
    out.append(K.endsec())
    return "".join(out)


def s2_checklists():
    out = [K.section("pr-checks", "2", "Validation checklists — field copy", kick="Pocket reference · Section 2",
                     lead="Tick, status, evidence reference. Transfer results into the change record before "
                          "sign-off; an unexplained N/A is an audit finding.")]
    out.append(K.h3("2.1", "OS"))
    out.append(K.checklist("pos", ["Done", "Check", "Status", "Evidence / remarks"],
                           ["File systems / mount points", "CPU", "RAM", "Swap", "OS version", "Kernel version",
                            "UID/GID", "Libraries", "FTP users", "OS groups", "IP addresses", "Hostnames",
                            "/etc/hosts", "/etc/services", "SAP directories", "Permissions"]))
    out.append(K.h3("2.2", "SAP"))
    out.append(K.checklist("psap", ["Done", "Check", "Status", "Evidence / remarks"],
                           ["SAP services active", "Auto-start tested (real reboot)", "SAP processes green",
                            "Application servers available", "SM51", "SMGW", "SM59", "RFC report", "SNC", "STMS",
                            "Transport directory", "AL11", "Printers", "Spool", "SMICM", "SSL/TLS certificates",
                            "SAP license"]))
    out.append(K.h3("2.3", "Database"))
    out.append(K.checklist("pdb", ["Done", "Check", "Status", "Evidence / remarks"],
                           ["DB status", "DB02", "Storage utilization", "Tablespaces", "Database growth",
                            "Latest backup", "Backup status", "Redo/archive logs", "Recovery requirements"]))
    out.append(K.h3("2.4", "Performance"))
    out.append(K.checklist("pperf", ["Done", "Check", "Status", "Evidence / remarks"],
                           ["ST02 memory", "Extended memory", "Heap/private memory", "Buffer utilization",
                            "ST03N workload", "Response time", "Wait time", "DB request time", "CPU time",
                            "Performance trends"]))
    out.append(K.h3("2.5", "Cutover readiness"))
    out.append(K.checklist("pcut", ["Done", "Check", "Status", "Evidence / remarks"],
                           ["Application shutdown confirmed", "DBA handover confirmed",
                            "Source/target synchronization confirmed", "Snapshot/backup confirmed",
                            "DNS/IPAM plan confirmed", "Evidence captured", "Technical validation complete",
                            "Functional validation complete", "Approvals complete", "Rollback ready",
                            "Go/No-Go decision recorded"]))
    out.append(K.endsec())
    return "".join(out)


def s3_quickref():
    out = [K.section("pr-quick", "3", "Transactions, commands and files", kick="Pocket reference · Section 3",
                     lead="What each item proves. A screenshot you cannot interpret is not evidence.")]
    out.append(K.table(["T-code", "Proves", "T-code", "Proves"],
                       [["SM51", "All planned instances active and registered", "ST02", "EM, heap/private, roll, paging, buffer hit ratio"],
                        ["SM59", "RFC destinations exist and connect", "ST03/ST03N", "Response/DB/CPU/wait time and workload trend"],
                        ["SMGW", "Gateway status and connections", "STAD", "The individual slow records behind the aggregates"],
                        ["SMICM", "ICM HTTP/HTTPS services and ports", "RZ10 / RZ11", "Persistent profile change / dynamic runtime change"],
                        ["STMS", "Domain, systems, routes, transport directory", "DB02", "Space, tablespaces, growth, backup status"],
                        ["AL11", "SAP directories, content, permissions", "SPAD / SP01", "Output devices and spool requests"],
                        ["STRUST", "Certificates: validity, chain, hostname", "SLICENSE", "License valid for the new hardware key"],
                        ["ST22 / SM37", "New dumps / job status after go-live", "SM13 / SM12", "Update errors / lock entries"]],
                       widths=[12, 38, 12, 38], caption="SAP transaction quick reference"))
    out.append(K.table(["Command", "Validates"],
                       [["<code>df -h</code>, <code>mount</code>, <code>lsblk</code>", "File systems, mounts, sizes, options"],
                        ["<code>lscpu</code>, <code>free -g</code>, <code>swapon -s</code>", "CPU, RAM, swap versus build sheet"],
                        ["<code>id</code>, <code>getent passwd</code>, <code>getent group</code>", "Numeric UID/GID consistency"],
                        ["<code>ip a</code>, <code>ip r</code>, <code>hostname -f</code>", "IPs, routes, hostname/FQDN"],
                        ["<code>getent hosts</code>, <code>nslookup</code>", "Resolution — run from the SAP host, not a laptop"],
                        ["<code>uname -r</code>, <code>/etc/os-release</code>", "Kernel and OS version"],
                        ["<code>systemctl status / show</code>", "Service state, Result and exit code"],
                        ["<code>sapcontrol -nr &lt;nn&gt; -function GetProcessList</code>", "Instance process state from the OS"],
                        ["<code>R3trans -d</code>", "SAP-to-database connectivity (expect 0000)"],
                        ["<code>rsync -avn</code> (dry run first)", "Global directory synchronisation"]],
                       widths=[44, 56], caption="OS command quick reference"))
    out.append(K.table(["File / location", "Why it decides the cutover"],
                       [["<code>/etc/hosts</code>", "A stale entry silently overrides DNS and reconnects you to the source"],
                        ["<code>/etc/services</code>", "<code>sapdp&lt;nn&gt;</code> / <code>sapgw&lt;nn&gt;</code> port definitions"],
                        ["<code>/etc/fstab</code>", "A missing or misordered mount breaks SAP at boot"],
                        ["SAP work/log dirs", "<code>dev_w*</code>, <code>dev_disp</code>, <code>dev_ms</code> explain start failures"],
                        ["<code>trans.log</code>", "First place to look when <code>R3trans -d</code> ≠ 0000"],
                        ["HANA INI files", "<code>global.ini</code>, <code>nameserver.ini</code> drive recovery"],
                        ["Oracle network files", "<code>listener.ora</code>, <code>tnsnames.ora</code>, <code>sqlnet.ora</code>"]],
                       widths=[28, 72], caption="Files that decide whether a cutover works"))
    out.append(K.endsec())
    return "".join(out)


def s4_codes():
    out = [K.section("pr-codes", "4", "Return codes and first diagnostics", kick="Pocket reference · Section 4",
                     lead="Diagnose before you retry, and never raise a memory parameter before finding what "
                          "consumes the memory.")]
    out.append(K.table(["Code", "Meaning", "First actions"],
                       [["Service <code>0</code>", "Success", "Still confirm instances in <code>SM51</code> — zero exit ≠ usable SAP"],
                        ["Service <code>127</code>", "Command or shared library not found", "ExecStart path, <code>&lt;sid&gt;adm</code> environment, <code>LD_LIBRARY_PATH</code>, migrated libraries"],
                        ["Service <code>255</code>", "Generic start-script/SAP failure", "Service journal, <code>dev_disp</code>, <code>dev_ms</code>, <code>dev_w0</code>, DB connect trace"],
                        ["<code>R3trans 0000</code>", "SAP ↔ database connectivity OK", "Proceed to SAP start"],
                        ["<code>R3trans 0012</code>", "Database connect failed", "DB open? listener? DB host entry in profile and <code>/etc/hosts</code>?"],
                        ["<code>R3trans 0018</code>", "DB authorisation / credentials", "User, password, wallet/keystore, credentials handover"]],
                       widths=[16, 30, 54], caption="Codes you will actually see",
                       note="Confirm code meanings against the release and platform in use; treat as a starting point."))
    out.append(K.table(["Symptom", "Investigate first", "Owner"],
                       [["Processes in PRIVATE mode", "EM under-sized, long transactions, memory-heavy custom code", "Basis + ABAP"],
                      ["High paging / swaps", "Paging area too small, context held too long", "Basis"],
                      ["Low buffer hit ratio", "Buffer sizing or access patterns bypassing buffers", "Basis + DBA"],
                      ["High DB time", "Access path, statistics, SQL, app-to-DB latency, storage throughput", "DBA"],
                      ["High CPU time", "Custom code, data volume, under-sized instance type", "ABAP"],
                      ["High wait time", "Memory, enqueue, RFC destinations, dispatcher", "Basis + interface owner"],
                      ["Slow only at peak", "Work process saturation, DB contention", "Basis + DBA"]],
                       widths=[24, 52, 24], caption="Memory and performance symptom map"))
    out.append(K.box("warn", "Threshold caution",
                     K.para("≈1200 ms response time and ≈40% average DB request time are discussion values from the "
                            "training. Validate against the client baseline and the measured source performance "
                            "before using them as alerting thresholds.")))
    out.append(K.endsec())
    return "".join(out)


def s5_dbcards():
    out = [K.section("pr-db", "5", "Oracle switchover and HANA recovery cards", kick="Pocket reference · Section 5",
                     lead="Planned switchover only — a failover is disaster recovery and is not reversible in "
                          "the same way.")]
    out.append(K.table(["#", "Step", "Evidence to capture"],
                       [["1", "Pre-checks: listener, SQL*Net, DG parameters, SID, Broker, observer, patch alignment", "Config outputs"],
                        ["2", "Review log switching and apply lag (zero gap)", "<code>v$managed_standby</code>"],
                        ["3", "Compare source and target SCN", "<code>v$database.current_scn</code> both sides"],
                        ["4", "Attach evidence to Jira/change; obtain approval", "Ticket reference"],
                        ["5", "AWS disk-level snapshot of the target (rollback point)", "Snapshot ID + timestamp"],
                        ["6", "Application shutdown confirmed; DBA handover accepted", "Bridge log"],
                        ["7", "Close source primary; switchover; open new primary", "Command output"],
                        ["8", "Validate new primary; <code>DBVERIFY</code>; <code>RMAN</code> backup; OEM agent", "DBVERIFY + RMAN logs"]],
                       widths=[5, 55, 40], caption="Oracle Data Guard switchover sequence"))
    out.append(K.table(["DNS / IPAM after switchover", "Rule"],
                       [["Virtual hostname", "Unchanged — SAP keeps addressing the same name"],
                        ["Target IP", "Updated in DNS/IPAM"],
                        ["CNAME", "Repointed to the target environment"],
                        ["Resolution", "Verified from every consumer with <code>getent hosts</code> + a real <code>R3trans -d</code>"],
                        ["Host files", "Obsolete entries cleaned — they override DNS"]],
                       widths=[30, 70], caption="Name resolution after the role change"))
    out.append(K.flow(["Source backup", "Configuration file", "S3 backend", "Target configuration", "Recovery", "Validation"]))
    out.append(K.box("key", "HANA container model in one line",
                     K.para("SystemDB = central management, monitoring and the backup catalogue; TenantDB = the "
                            "application workload. Separate logins; both can live on one host; neither is HA — "
                            "HA is HSR plus cluster/storage design.")))
    out.append(K.box("risk", "Cutover rule",
                     K.para("Test backup and recovery before cutover. During cutover: final backup → validate it → "
                            "only then stop the source. The source stays available until that backup succeeds; it "
                            "is also your rollback anchor.")))
    out.append(K.endsec())
    return "".join(out)


def s6_evidence():
    out = [K.section("pr-evid", "6", "Evidence, hypercare and escalation", kick="Pocket reference · Section 6",
                     lead="Working before migration should work after migration — evidence is what makes that "
                          "provable at 02:00 on a bridge call.")]
    out.append(K.cmd(["&lt;SID&gt;_&lt;PHASE&gt;_&lt;CHECK&gt;_&lt;SOURCE|TARGET&gt;_&lt;YYYYMMDD-HHMM&gt;.&lt;ext&gt;",
                      "",
                      "<span class='c'># examples</span>",
                      "PRD_PRECUT_SM59_SOURCE_20261002-1015.pdf",
                      "PRD_CUTOVER_R3TRANS_TARGET_20261005-0212.log",
                      "PRD_CUTOVER_SCN_BOTH_20261005-0140.png"]))
    out.append(K.table(["Before vs after", "Classification", "Route"],
                       [["Working → failing", "Migration-related", "Owning team corrects, retests, re-captures evidence"],
                        ["Failing → failing", "Pre-existing condition", "Document it; route to BAU with baseline evidence"],
                        ["Failing → working", "Improvement", "Record it so it is not rolled back later"],
                        ["No baseline", "Unclassifiable", "Escalate — you cannot prove what you did not record"]],
                       widths=[22, 26, 52], caption="Classifying a failure in hypercare"))
    out.append(K.table(["Watch daily", "Source", "Bad trend looks like"],
                       [["Short dumps", "<code>ST22</code>", "New dump types or a rising count"],
                        ["Failed jobs", "<code>SM37</code> / Control-M", "Jobs cancelled that previously succeeded"],
                        ["Interfaces / IDocs", "<code>SM59</code>, <code>WE02</code>", "Rising error status, retries not clearing"],
                        ["Response time", "<code>ST03N</code>", "Sustained rise over baseline, same period type"],
                        ["Memory", "<code>ST02</code>", "PRIVATE mode, rising paging or swaps"],
                        ["Database", "<code>DB02</code>, alert log", "Growth beyond forecast, archive filling, backup failures"],
                        ["Updates / locks", "<code>SM13</code>, <code>SM12</code>", "Stuck updates, growing lock entries"],
                        ["Certificates", "<code>STRUST</code>", "Expiry approaching, SNC handshake failures"]],
                       widths=[20, 26, 54], caption="Hypercare monitoring set (15 days)"))
    out.append(K.table(["Severity", "Definition", "Route"],
                       [["S1 Critical", "Cutover blocked, system down, data at risk, rollback decision", "Bridge → module owner → programme lead → stakeholders now"],
                        ["S2 High", "Gate cannot pass; validation failure without workaround", "Module owner → team lead; in the change record"],
                        ["S3 Medium", "Deviation with workaround; deferrable", "Owning team; deviation log; before next gate"],
                        ["S4 Low", "Cosmetic / documentation", "Deviation log; closed in hypercare"]],
                       widths=[14, 40, 46], caption="Escalation model"))
    out.append(K.box("key", "Ownership principle",
                     K.para("One accountable owner per assigned SID, one named guide per owner, controlled change. "
                            "Multiple engineers must not independently modify the same system.")))
    out.append(K.endsec())
    return "".join(out)


def build():
    html = "<html><body><main class='paper'><div class='wrap'>" + "".join([
        cover(), s1_runcard(), s2_checklists(), s3_quickref(), s4_codes(), s5_dbcards(), s6_evidence(),
    ]) + "</div></main></body></html>"
    tree = LH.fromstring(html)

    doc = M.new_doc()
    core = doc.core_properties
    core.title = "SAP Migration — Field Pocket Reference"
    core.subject = "Condensed cutover and validation companion to SAP-MIG-TRN-HB-001 v1.0"
    core.author = "Amit Prajapati"
    core.category = "Field reference card"
    core.comments = ("Condensed companion to the SAP Migration Training Handbook v1.0. Internal training "
                     "and cutover use; does not replace approved project runbooks.")
    core.keywords = "SAP, AWS, migration, cutover, checklist, Oracle, HANA, hypercare"
    M.enable_update_fields(doc)
    M.header_footer(doc, "SAP Migration Pocket Reference · v1.0 · Internal")

    first = True
    for sec in tree.xpath("//main//section"):
        M.emit_section(doc, sec, first=first)
        first = False
    doc.save(OUT)
    print("built %s (%.1f KB, %d paragraphs, %d tables)"
          % (OUT, os.path.getsize(OUT) / 1024, len(doc.paragraphs), len(doc.tables)))
    return 0


if __name__ == "__main__":
    sys.exit(build())
