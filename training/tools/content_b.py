"""Handbook content, part 2: sections 7-10 (modules 4-7)."""

from htmlkit import (box, bullets, cards, checklist, cmd, e, figure, flow, h3, kpis,
                     para, pill, qa, section, steps, table)

FIG = {}


# --------------------------------------------------------------------------- #
def s7_m4():
    out = [section("m4", "7", "Module 4 — SAP post-migration validation", cls="mod",
                   kick="Module 4 · Section 7",
                   lead="Validation is comparison, not inspection. Every check in this module answers one question: does the target "
                        "match the approved design and the source baseline, and if not, is the difference explained?")]
    out.append(h3("7.1", "Auto-start validation"))
    out.append(steps([
        "Check the configured SAP service (the init/systemd unit that starts SAP at boot).",
        "Verify the service status is <b>Active</b>.",
        "Verify the service return code.",
        "Stop the required SAP instances cleanly.",
        "Coordinate the server reboot with the Linux team (and with any cluster or HA manager).",
        "After reboot, verify automatic SAP startup without manual intervention.",
        "Confirm SAP availability: instances registered, work processes running, logon possible.",
        "Capture evidence: service status, return code, instance list before and after, timestamps."]))
    out.append(box("risk", "Never assume auto-start works. Test it through an actual reboot.",
                   para("A service that is enabled and active can still fail at boot because of ordering: a file system that mounts "
                        "late, a network interface that is not yet up, a cluster resource that owns the virtual IP, or a dependency "
                        "on the database host. Only a real reboot proves the sequence.")))
    out.append(table(["Return code", "Interpretation", "First actions"],
                     [["<code>0</code>", "Success. The expected result after reboot.", "Confirm instances are actually registered in <code>SM51</code> — a zero exit code is not proof that SAP is usable."],
                      ["<code>127</code>", "Command or shared library not found: missing executable, wrong path, or an unresolved library dependency.", "Check the service <code>ExecStart</code> path, the <code>&lt;sid&gt;adm</code> environment, <code>LD_LIBRARY_PATH</code>, and that the kernel and shared libraries were migrated with correct permissions."],
                      ["<code>255</code>", "Generic/unknown failure returned by the start script or SAP program.", "Read the actual logs: service journal, <code>startsap</code>/SAPControl output, <code>dev_w0</code>, <code>dev_disp</code>, <code>dev_ms</code>, and the database connection trace."],
                      ["Other non-zero", "Script- or component-specific failure.", "Map the code against the start script and SAP component logs; do not retry until the cause is known."]],
                     caption="Service return codes discussed in the training", widths=["12%", "38%", "50%"],
                     note="Codes 127 and 255 were cited in the source training as indicators requiring troubleshooting. Treat the mapping above as a diagnostic starting point and confirm against the platform and SAP start mechanism used in the project."))
    out.append(cmd(["<span class='c'># Service state and exit code (example — adapt to the project's unit naming)</span>",
                    "<span class='p'>systemctl status</span> SAP&lt;SID&gt;_&lt;NR&gt;.service   <span class='c'># expect: Active: active (exited/running)</span>",
                    "<span class='p'>systemctl show</span> -p ExecMainStatus,ExecMainCode,Result SAP&lt;SID&gt;_&lt;NR&gt;.service",
                    "<span class='c'># expect: ExecMainStatus=0  Result=success</span>",
                    "",
                    "<span class='c'># Instance state without the SAP GUI</span>",
                    "<span class='p'>sapcontrol</span> -nr &lt;instance-number&gt; -function GetSystemInstanceList",
                    "<span class='p'>sapcontrol</span> -nr &lt;instance-number&gt; -function GetProcessList",
                    "<span class='c'># then confirm in SM51 that every instance is active and registered</span>"]))
    out.append(h3("7.2", "OS validation"))
    out.append(table(["Check", "What to compare", "Typical commands / sources"],
                     [["File systems and mount points", "Every mount present, correct size, type, options and owner", "<code>df -h</code>, <code>mount</code>, <code>/etc/fstab</code>, <code>lsblk</code>"],
                      ["CPU", "Core count and architecture match the approved sizing", "<code>lscpu</code>, <code>nproc</code>"],
                      ["RAM", "Total memory matches the build sheet; HANA/DB allocation as designed", "<code>free -g</code>, <code>/proc/meminfo</code>"],
                      ["Swap", "Swap size and swappiness per the SAP/DB requirement", "<code>swapon -s</code>, <code>sysctl vm.swappiness</code>"],
                      ["OS and kernel versions", "Distribution, release and kernel match the target design", "<code>/etc/os-release</code>, <code>uname -r</code>"],
                      ["UID/GID", "<code>sapadm</code>, <code>&lt;sid&gt;adm</code>, DB users and groups identical to source/design", "<code>id</code>, <code>getent passwd</code>, <code>getent group</code>"],
                      ["Libraries", "Required shared libraries present at the expected versions", "<code>ldd</code> on key binaries, package list comparison"],
                      ["FTP users and OS groups", "Service accounts and group memberships migrated correctly", "<code>getent passwd</code>, <code>getent group</code>, FTP/SFTP config"],
                      ["Physical and virtual IPs", "Both present, bound to the right interfaces, correct netmask/gateway", "<code>ip a</code>, <code>ip r</code>"],
                      ["Physical and virtual hostnames", "Hostname, FQDN and virtual hostname resolve as designed", "<code>hostname</code>, <code>hostname -f</code>, <code>getent hosts</code>"],
                      ["<code>/etc/services</code> and <code>/etc/hosts</code>", "SAP service ports (sapdp/sapgw), sapdbhost entries, no stale source IPs", "<code>grep sap /etc/services</code>, <code>/etc/hosts</code>"],
                      ["SAP directories and permissions", "Kernel, profile, work, log, transport, interface directories present with correct ownership", "<code>ls -ld</code> per directory, compare with the source listing"],
                      ["OS tuning", "Hugepages, THP, semaphores, shared memory, file limits, scheduler", "<code>sysctl -a</code> subset, <code>/proc/meminfo</code>, <code>ulimit -a</code>"]],
                     caption="OS validation detail", widths=["22%", "40%", "38%"]))
    out.append(box("warn", "UID/GID mismatches are quiet and expensive",
                   para("A different UID for <code>&lt;sid&gt;adm</code> on the target makes files look correctly named but wrongly owned. "
                        "The symptoms appear later and elsewhere: SAP start failures, permission denied on the transport or interface "
                        "directory, NFS squash problems, or inter-server communication failures. Compare numeric IDs, not just names.")))
    out.append(h3("7.3", "SAP application validation"))
    out.append(table(["Area", "Transaction / tool", "What a pass looks like"],
                     [["SAP services and processes", "OS service, <code>sapcontrol</code>", "Service active, return code 0, all processes green"],
                      ["Application servers", "<code>SM51</code>", "Every planned instance listed, active, with the expected work process configuration"],
                      ["Gateway", "<code>SMGW</code>", "Gateway running, expected connections present, no unexplained external registrations"],
                      ["RFC destinations", "<code>SM59</code>", "Each destination from the baseline exists and its connection test succeeds (or matches a documented pre-existing failure)"],
                      ["RFC connectivity report", "<code>SA38</code> / project report", "Bulk test result matches the baseline interface list"],
                      ["Transport landscape", "<code>STMS</code>", "Domain, systems, routes and transport directory correct; import works end to end"],
                      ["Directories", "<code>AL11</code>", "All baseline directories present with correct permissions and content"],
                      ["Printers and spool", "<code>SPAD</code>, <code>SP01</code>", "Device types and output devices correct; test page prints; spool processes run"],
                      ["ICM / HTTP(S)", "<code>SMICM</code>", "ICM services active on the expected ports; HTTPS endpoints answer with the right certificate"],
                      ["SNC and secure communication", "<code>SNC</code> configuration, PSE/keystore", "SNC enabled where designed, correct users, valid PSE, no handshake errors"],
                      ["Certificates", "<code>STRUST</code>", "Certificates valid, correct hostname/domain, chain complete, expiry dates acceptable"],
                      ["SAP license", "<code>SLICENSE</code>", "Correct license installed for the new hardware key; temporary license not left to expire"]],
                     caption="SAP application validation", widths=["22%", "20%", "58%"]))
    out.append(box("key", "Hardware key and license",
                   para("A migration normally changes the hardware key, which invalidates the permanent SAP license. Install the "
                        "correct license (or a valid temporary one) during cutover and record the expiry date so it is replaced "
                        "before it lapses. This is a go-live blocker that is easy to overlook because the system works without it "
                        "for a while.")))
    out.append(h3("7.4", "Database validation"))
    out.append(table(["Check", "Detail to record", "Tool"],
                     [["DB status", "Instance up, services/processes running, no failed components", "<code>DB02</code>, DB-specific console"],
                      ["Space utilisation", "Data, log, archive, backup area; percent used and absolute free", "<code>DB02</code>"],
                      ["Tablespaces", "Each tablespace size, free space, autoextend setting, largest objects", "<code>DB02</code>"],
                      ["Growth", "Growth rate compared with the source baseline and the sizing assumption", "<code>DB02</code>, historical reports"],
                      ["Latest successful backup", "Timestamp, type, duration, size, and that it is on the intended target", "Backup tool / <code>DB02</code>"],
                      ["Backup history", "Sequence complete, no gaps, retention as designed", "Backup catalogue"],
                      ["Redo / archive log status", "Archive destination reachable, no log-switch stalls, archiver running", "DB log mode and archive status"],
                      ["Recovery considerations", "Point-in-time recovery possible; restore path and required files verified", "Recovery test record"]],
                     caption="Database validation", widths=["22%", "52%", "26%"]))
    out.append(box("warn", "A green database is not a validated database",
                   para("Compare sizes and object counts with the source baseline. A recovery that completes but silently misses a "
                        "tablespace, or a log archive destination that is full, will not show up as an error at start-up — it shows "
                        "up as an incident two weeks into hypercare.")))
    out.append(h3("7.5", "Handling deviations found during validation"))
    out.append(steps([
        "Record the deviation immediately: what was expected, what was found, and the evidence for both.",
        "Classify it: configuration drift, migration defect, pre-existing condition, or an intentional approved difference.",
        "Assign it to the responsible team and owner — do not carry an unowned deviation into the cutover gate.",
        "Correct it through the approved change route.",
        "Retest the specific check, not just the fix.",
        "Re-capture the evidence and close the item with a reference to the change record."]))
    out.append("</section>")
    return "".join(out)


def s8_m5():
    out = [section("m5", "8", "Module 5 — Performance monitoring and troubleshooting", cls="mod",
                   kick="Module 5 · Section 8",
                   lead="Performance work after a migration is comparison work. The pre-migration baseline turns a subjective "
                        "complaint into a measurable delta, and the triage path keeps you from changing parameters before you "
                        "understand the cause.")]
    out.append(figure("d7-performance", FIG["d7-performance"],
                      "<b>Figure 7.</b> Left: the SAP memory escalation described in the training — extended memory is consumed first, "
                      "and when it is exhausted work processes move into heap/private memory. Right: the top-down triage path from "
                      "workload statistics to a root-cause fix with the owning team."))
    out.append(h3("8.1", "ST02 — memory monitoring"))
    out.append(table(["Memory area", "What it is", "What to watch"],
                     [["Extended memory (EM)", "Shared memory used first for user context; allocated per instance", "Max, used and free; whether processes are being pushed out of EM"],
                      ["Heap / private memory", "Process-private memory used when EM is exhausted; the process mode becomes PRIVATE", "Frequency and duration of PRIVATE mode — a strong signal of under-allocation or a memory leak"],
                      ["Roll memory / roll area", "Per work process area holding rolled user context", "Roll-in/roll-out activity and whether the roll area is a bottleneck"],
                      ["Paging memory", "Paged user context (paging area / swaps)", "Swaps and paging rate; high paging means context is being thrown away and rebuilt"],
                      ["Buffer memory", "Program buffer, single record buffer, table buffer, export/import buffer", "Utilisation and hit ratio per buffer; low hit ratio with high reads means sizing or access-pattern problems"]],
                     caption="ST02 memory areas", widths=["20%", "42%", "38%"]))
    out.append(para("For each area record <b>available, used and free</b>, plus buffer utilisation and hit ratio, so the target can be "
                    "compared with the source snapshot rather than judged in isolation."))
    out.append(box("key", "Memory troubleshooting principle",
                   para("The training described the general relationship as: <b>Extended Memory → if exhausted → Heap/Private "
                        "Memory</b>. Investigate the cause rather than simply increasing memory. A parameter increase hides the "
                        "symptom and can move the failure somewhere worse — for example into OS swapping or an OOM condition.")))
    out.append(table(["Symptom", "Likely causes to investigate first", "Do not do this"],
                     [["Work processes frequently in PRIVATE mode", "EM under-sized for the workload, long-running transactions, high dialog step counts, memory-consuming custom code", "Raise <code>ztta/roll_area</code>/EM parameters before measuring actual consumption"],
                      ["High paging / swap rate", "Paging area too small for the number of users, or context held too long", "Add OS swap to “fix” an SAP memory design issue"],
                      ["Low table-buffer hit ratio", "Buffer sizing, or access patterns that bypass the buffer (non-key reads, generic selects)", "Enlarge buffers without checking whether the code can use them"],
                      ["Growing heap over days", "Memory leak in custom code, unfreed internal tables, session accumulation", "Schedule restarts as a permanent workaround"],
                      ["Slow response only at peak", "Work process saturation, DB contention, enqueue or RFC waits", "Tune a parameter that is not the constraint"]],
                     caption="Memory symptom table", widths=["26%", "44%", "30%"]))
    out.append(h3("8.2", "RZ10 versus RZ11"))
    out.append(table(["Transaction", "Nature", "Persistence", "Restart", "Use when"],
                     [["<code>RZ10</code>", "Profile parameter maintenance (instance, default and start profiles)", "Persistent — written to the profile and activated", "Required for many parameters; some take effect at the next instance start", "The change must survive a restart and be part of the configuration baseline"],
                      ["<code>RZ11</code>", "Runtime parameter display and change where the parameter is dynamically switchable", "Temporary — lost at restart unless also set in the profile", "Not required for dynamic parameters", "Testing a value, or applying a supported dynamic change within an approved window"]],
                     caption="RZ10 versus RZ11", widths=["10%", "26%", "24%", "20%", "20%"]))
    out.append(box("warn", "Profile discipline during migration",
                   bullets([
                       "Any <code>RZ11</code> change made to get through a cutover must be followed by a matching <code>RZ10</code> entry, or the fix disappears at the next restart.",
                       "Profile changes are configuration changes: they need the same approval, documentation and transport/record discipline as any other change.",
                       "Compare the source and target profile parameter sets explicitly after migration — parameters that no longer exist, or that were silently defaulted, are a frequent cause of post-migration behavioural differences."])))
    out.append(h3("8.3", "ST03 / ST03N — workload analysis"))
    out.append(table(["Metric", "Definition", "How to use it in a migration"],
                     [["Response time", "Total time from dialog step start to end, as experienced by the user", "Compare target against the source baseline for the same period type (business hours, month-end)"],
                      ["Database time", "Time spent in database requests", "The single most useful split: high DB time points to the database, network or SQL, not to ABAP"],
                      ["CPU time", "Time spent executing on the application server CPU", "High CPU time with normal DB time points to code, volume or under-sized compute"],
                      ["Wait time", "Time waiting for resources: roll, paging, enqueue, RFC, dispatcher", "High wait time is a resource or dependency problem — check memory and external systems"],
                      ["Workload / steps", "Number of dialog steps, background and RFC steps", "Confirms you are comparing equivalent load, not a quiet day against a peak day"],
                      ["User activity", "Active users and their distribution", "Explains load differences and identifies who to interview about slowness"]],
                     caption="Workload metrics", widths=["18%", "40%", "42%"]))
    out.append(bullets([
        "Analyse daily, weekly and monthly views: a single day is noise, a month shows the trend and the peaks.",
        "Compare like with like — same day type, same time window, same workload mix.",
        "Record the top transactions by response time and by total load; they become your re-test list after any change.",
        "<code>ST03N</code> is the current workload transaction; <code>ST03</code> is retained here because the source material and many runbooks still reference it."]))
    out.append(h3("8.4", "STAD — detailed statistical records"))
    out.append(para("Where ST03/ST03N gives you aggregates, <code>STAD</code> gives you the individual statistical records behind them. "
                    "Use it to answer “which specific step, for which user, at which time, and where did the time go?”"))
    out.append(table(["Analysis goal", "What to look for in STAD"],
                     [["Slow transactions", "Records with the highest response time, grouped by transaction code"],
                      ["Long response times", "Distribution of response time — a few extreme records or a general shift"],
                      ["Database-intensive activity", "High DB time relative to response time; number of DB requests per step; sequential reads"],
                      ["CPU-intensive activity", "High CPU time relative to response time, often with low DB time"],
                      ["User-specific workload", "Records by user — identifies a single heavy session, a broken client, or a report run ad hoc"],
                      ["Performance bottlenecks", "Roll/wait time, enqueue time, RFC time, and spool time as separate components"]],
                     caption="STAD analysis targets", widths=["26%", "74%"]))
    out.append(box("warn", "Threshold caution",
                   para("The source training referenced approximately <b>1200 ms</b> response time and <b>40%</b> average database "
                        "request time as discussion/reference values. These are teaching aids, not standards. Validate them against "
                        "the applicable SAP and client baseline — and against the measured source performance for the same system — "
                        "before using them as production alerting thresholds. " + pill("Validate", "r"))))
    out.append(h3("8.5", "Triage path"))
    out.append(steps([
        "Reproduce or evidence the symptom: which transaction, which user, which time window, how often.",
        "Check the aggregate view in <code>ST03</code>/<code>ST03N</code> and compare it with the pre-migration baseline for the same period type.",
        "Split the time: database, CPU, wait, roll, RFC. This decides which team owns the investigation.",
        "Drill into <code>STAD</code> for the specific slow records.",
        "If memory is implicated, check <code>ST02</code>: EM, heap/private, roll, paging, buffer hit ratios.",
        "Check the non-SAP layer when the split points there: database statistics and SQL, network latency to the DB, storage throughput, host CPU and memory pressure.",
        "Identify the root cause and agree the fix with the owning team (DBA, ABAP, Linux, network).",
        "Apply the fix through the approved change route, then re-measure against the baseline.",
        "Record before/after evidence and close the item."]))
    out.append(table(["Time component dominates", "Look at", "Usual owner"],
                     [["Database time", "SQL and access path, missing or stale statistics/indexes, DB parameters, network latency to the DB, storage throughput", "DBA (with ABAP for access paths)"],
                      ["CPU time", "Custom code, volume of data processed, loop and internal-table behaviour, under-sized instance type", "ABAP / application team"],
                      ["Wait time", "Roll and paging behaviour, EM/heap configuration, enqueue contention, slow RFC destinations", "Basis (with the interface owner)"],
                      ["Roll time", "Roll area sizing, number of dialog steps, context size", "Basis"],
                      ["RFC / external time", "Destination response, middleware, partner system, network path", "Interface owner + network"],
                      ["Spool time", "Spool server, device type, output volume, printer availability", "Basis"]],
                     caption="From symptom to owner", widths=["22%", "54%", "24%"]))
    out.append(h3("8.6", "Module 5 readiness checklist"))
    out.append(checklist("m5", ["Done", "Check", "Status", "Evidence / remarks"], [
        "ST02 captured on source and target: EM, heap/private, roll, paging",
        "Buffer utilisation and hit ratio recorded for each buffer",
        "ST03/ST03N daily, weekly and monthly views captured on source and target",
        "Response, DB, CPU and wait times compared with the baseline",
        "STAD samples captured for the slowest transactions",
        "Top transactions by response time and total load listed",
        "Bottleneck classified by dominant time component",
        "Root cause identified with the owning team (not a parameter guess)",
        "Any RZ11 runtime change mirrored in RZ10 or formally withdrawn",
        "Profile parameter sets compared between source and target",
        "Reference thresholds validated against the client baseline before alerting use",
        "Before/after evidence attached to the change record",
    ]))
    out.append("</section>")
    return "".join(out)


def s9_m6():
    out = [section("m6", "9", "Module 6 — Oracle database migration and switchover", cls="mod",
                   kick="Module 6 · Section 9",
                   lead="The Oracle scenario covered in the training moves the database by building a standby in AWS, synchronising "
                        "it with Data Guard, then performing a planned switchover during the cutover window.")]
    out.append(figure("d5-oracle-dataguard", FIG["d5-oracle-dataguard"],
                      "<b>Figure 5.</b> Data Guard switchover sequence. Redo flows from the source primary to the target standby "
                      "throughout the project; SCN values are compared to prove synchronisation; a snapshot creates the rollback "
                      "point; the roles are swapped only after evidence and approval; and the new primary is validated with DBVERIFY, "
                      "RMAN and the OEM agent before it is accepted."))
    out.append(h3("9.1", "Oracle Data Guard in the migration scenario"))
    out.append(bullets([
        "Source primary and target standby are synchronized using Oracle Data Guard.",
        "Log switching and synchronization are reviewed before switchover — apply lag must be zero (or within the agreed tolerance) at the moment of the change.",
        "Source and target System Change Number (SCN) values are compared to verify synchronization and data consistency.",
        "Evidence must be captured and attached to the relevant Jira/change ticket for approval.",
        "After successful validation, the source is shut down and the target standby is activated as the new primary."]))
    out.append(table(["Concept", "Meaning", "Why it matters at cutover"],
                     [["Primary", "The database that accepts writes and generates redo", "The source is primary until the switchover moment"],
                      ["Physical standby", "A copy of the primary kept current by applying shipped redo", "The migration target during the project phase"],
                      ["Redo transport", "Shipping of redo from primary to standby", "A break here silently widens the gap between source and target"],
                      ["Managed recovery (apply)", "Standby process applying received redo", "Apply lag is the number to watch before switchover"],
                      ["SCN (System Change Number)", "A logical point-in-time marker for the database", "Comparing source and target SCN proves the data is consistent"],
                      ["Log switch / archive", "Closing and archiving the current redo log", "Forcing log switches confirms the pipeline is live, not stalled"],
                      ["Switchover", "Planned, reversible role swap between primary and standby", "The migration mechanism in this scenario"],
                      ["Failover", "Unplanned promotion of the standby after a primary failure", "Not reversible in the same way — this is DR, not migration"],
                      ["Data Guard Broker", "Management layer that coordinates Data Guard configuration and operations", "Simplifies and standardises the switchover where it is used"],
                      ["Observer node", "Independent node that monitors the configuration (used with fast-start failover)", "Required for HA environments where automatic failover is designed"]],
                     caption="Data Guard vocabulary", widths=["18%", "40%", "42%"]))
    out.append(box("key", "Switchover versus failover",
                   para("A <b>switchover</b> is planned and reversible: both databases end the operation in a valid role, and you can "
                        "switch back. A <b>failover</b> is a disaster-recovery action: the standby becomes primary and the old primary "
                        "usually needs rebuilding. Migration uses switchover. Confusing the two in a runbook is how a reversible "
                        "operation becomes an unrecoverable one.")))
    out.append(h3("9.2", "Oracle configuration checks"))
    out.append(checklist("oracle-cfg", ["Done", "Check", "Status", "Evidence / remarks"], [
        "SQL*Net and listener configuration validated on source and target (tnsnames, listener.ora, service names)",
        "Listener registered services confirmed and reachable from the SAP application hosts",
        "Data Guard parameters validated (log archive destinations, transport/apply settings)",
        "SID-specific settings confirmed (SID, ORACLE_HOME, environment files, profile entries)",
        "Data Guard Broker configuration reviewed (where Broker is used)",
        "Observer-node configuration reviewed for HA environments",
        "Required source/target patch-level alignment confirmed",
        "Archive log mode and destination space validated on both sides",
        "Password files, wallets and credentials available to the DBA team",
        "Network path and latency between source and target measured and acceptable",
        "Character set, national character set and database options match",
    ]))
    out.append(h3("9.3", "Switchover sequence"))
    out.append(steps([
        "Complete pre-checks: listener, SQL*Net, Data Guard parameters, SID settings, Broker, observer node, patch alignment.",
        "Review log switching and apply status; confirm the standby is applying with no gap.",
        "Compare source and target SCN values and record both.",
        "Capture evidence and attach it to the Jira/change ticket; obtain approval.",
        "Take the AWS disk-level snapshot of the target to establish the rollback recovery point.",
        "Confirm application shutdown is complete and the DBA handover has been accepted.",
        "Shut down / close the source primary as designed.",
        "Perform the switchover and activate the target standby as the new primary.",
        "Open the new primary and validate it: services registered, listener responding, SAP can connect.",
        "Run <code>DBVERIFY</code> to check for database block corruption.",
        "Take an Oracle <code>RMAN</code> backup after successful validation.",
        "Install or verify the OEM agent in production where applicable.",
        "Hand back to Basis for the DNS/IPAM update and SAP-side validation."]))
    out.append(cmd(["<span class='c'>-- Synchronisation evidence typically captured before switchover (illustrative)</span>",
                    "<span class='p'>SELECT</span> database_role, open_mode, current_scn <span class='p'>FROM</span> v$database;",
                    "<span class='c'>-- run on BOTH source and target; compare current_scn</span>",
                    "",
                    "<span class='p'>SELECT</span> process, status, thread#, sequence#, block# <span class='p'>FROM</span> v$managed_standby;",
                    "<span class='c'>-- confirm MRP0 is APPLYING_LOG and no gap remains</span>",
                    "",
                    "<span class='c'>-- On the target after switchover: block integrity and backup</span>",
                    "<span class='p'>dbv</span> file=&lt;datafile&gt; blocksize=&lt;size&gt;      <span class='c'># expect: no corrupt blocks listed</span>",
                    "<span class='p'>rman</span> target /  <span class='c'>→</span> BACKUP DATABASE PLUS ARCHIVELOG;",
                    "",
                    "<span class='c'>-- Exact syntax (DGMGRL SWITCHOVER, ALTER DATABASE commands, Broker config)</span>",
                    "<span class='c'>-- comes from the project runbook and the Oracle version in use.</span>"]))
    out.append(box("warn", "Snapshot timing",
                   para("The snapshot must be taken <b>after</b> the standby is fully synchronised and <b>before</b> the role change. "
                        "Taken too early it is not a consistent recovery point; taken after the switchover it protects nothing. "
                        "Also confirm whether the project requires an application-consistent snapshot (quiesced database) or accepts "
                        "a crash-consistent one for this purpose — that decision belongs to the DBA lead and must be recorded. "
                        + pill("Validate", "r"))))
    out.append(h3("9.4", "Backup and rollback protection"))
    out.append(table(["Step", "Purpose", "Evidence"],
                     [["AWS disk-level snapshot before subsequent activities", "Establishes the rollback recovery point", "Snapshot ID, timestamp, volume list"],
                      ["Validate the new primary after switchover", "Confirms the database is open, services are registered and SAP can connect", "Listener/services output, connection test"],
                      ["Run Oracle <code>DBVERIFY</code>", "Checks for database block corruption in datafiles", "DBVERIFY output with no corrupted blocks"],
                      ["Take an Oracle <code>RMAN</code> backup", "Creates the first backup of the new primary and a fresh recovery baseline", "RMAN log, backup piece list, completion status"],
                      ["Install / verify the OEM agent in production", "Restores monitoring and alerting coverage on the new primary", "Agent status, target visible in the monitoring console"]],
                     caption="Post-switchover protection sequence", widths=["30%", "38%", "32%"]))
    out.append(h3("9.5", "DNS and IPAM after database switchover"))
    out.append(bullets([
        "The <b>virtual hostname remains unchanged</b> according to the migration design — SAP continues to address the database by the same name.",
        "The <b>target IP is updated</b> in DNS/IPAM.",
        "<b>CNAME entries are updated</b> to point to the correct target environment.",
        "Verify hostname and IP resolution from every consumer: SAP application hosts, interfaces, backup and monitoring systems.",
        "Clean obsolete host-file entries — a stale <code>/etc/hosts</code> line overrides DNS and silently reconnects you to the source."]))
    out.append(cmd(["<span class='c'># Resolution checks from an SAP application host</span>",
                    "<span class='p'>getent hosts</span> &lt;virtual-db-hostname&gt;      <span class='c'># must return the NEW target IP</span>",
                    "<span class='p'>nslookup</span> &lt;virtual-db-hostname&gt;         <span class='c'># confirm the CNAME chain</span>",
                    "<span class='p'>grep -n</span> &lt;virtual-db-hostname&gt; /etc/hosts  <span class='c'># must be empty or correct</span>",
                    "<span class='c'># then prove the SAP side sees the same database</span>",
                    "<span class='p'>R3trans -d</span>                             <span class='c'># expect return code 0000</span>"]))
    out.append(box("risk", "Cache and connection pooling",
                   para("DNS TTL, name-service caching and pooled database connections can keep a system talking to the old IP after "
                        "the record changes. Reduce TTL ahead of cutover as designed, restart the affected services, and verify with "
                        "an actual connection test (<code>R3trans -d</code>) rather than by reading the DNS record.")))
    out.append(h3("9.6", "Module 6 readiness checklist"))
    out.append(checklist("m6", ["Done", "Check", "Status", "Evidence / remarks"], [
        "Data Guard configured and applying with zero gap",
        "Listener, SQL*Net and service names validated on both sides",
        "Data Guard parameters and Broker configuration reviewed",
        "Observer node configured for HA environments",
        "Source and target patch levels aligned as required",
        "Log switching tested and reviewed before switchover",
        "Source and target SCN compared and recorded",
        "Evidence attached to the Jira/change ticket",
        "Approval obtained before production changes",
        "AWS disk-level snapshot taken at the correct point",
        "Application shutdown and DBA handover confirmed",
        "Switchover executed and new primary validated",
        "DBVERIFY completed with no corruption found",
        "RMAN backup of the new primary completed successfully",
        "OEM agent installed/verified in production where applicable",
        "Virtual hostname unchanged; target IP and CNAME updated",
        "Resolution verified from every consumer host",
        "Obsolete host-file entries cleaned",
        "R3trans -d returns 0000 from the application host",
        "Rollback path tested or rehearsed and still available",
    ]))
    out.append("</section>")
    return "".join(out)


def s10_m7():
    out = [section("m7", "10", "Module 7 — Cutover, Go/No-Go, rollback and hypercare", cls="mod",
                   kick="Module 7 · Section 10",
                   lead="Cutover is the execution of everything the previous modules prepared. It succeeds when the sequence is "
                        "boring: no surprises, no improvisation, evidence at each handover, and a decision gate that is allowed to "
                        "say no.")]
    out.append(figure("d6-cutover", FIG["d6-cutover"],
                      "<b>Figure 6.</b> Cutover lane sequence. Application stops and hands over to the DBA; the DBA completes backup, "
                      "snapshot, switchover or recovery and validation; Basis performs post-processing and starts SAP only after "
                      "<code>R3trans -d</code> returns 0000; the functional team tests; and the Go/No-Go gate decides release or rollback."))
    out.append(h3("10.1", "Cooldown and cutover preparation"))
    out.append(bullets([
        "Complete cooldown/ramp-up activities as defined by the project (for example reduced load, frozen changes, batch blackout).",
        "Shut down the application and associated web services as required.",
        "Hand over database-related activities to the DBA team <b>after</b> application shutdown, and get that handover acknowledged.",
        "Confirm all required evidence and approvals are ready <b>before</b> the window opens, not during it.",
        "Confirm the rollback point exists and the rollback owner is on the bridge.",
        "Confirm the window, the checkpoint times and the latest safe point-of-no-return."]))
    out.append(box("warn", "Define the point of no return",
                   para("Every cutover has a moment after which rollback becomes expensive or impossible — typically after the source "
                        "has been changed, decommissioned, or after new business data has been created on the target. Agree that point "
                        "in advance, announce it on the bridge when you pass it, and make sure the Go/No-Go decision happens before it.")))
    out.append(h3("10.2", "SAP Basis post-processing"))
    out.append(table(["#", "Activity", "Detail and acceptance"],
                     [["1", "Synchronize the SAP global directory using <code>rsync</code>", "Global directories (for example transport, interface and shared directories) copied and compared; permissions and ownership preserved"],
                      ["2", "Clean and validate host-file / IPAM entries", "No stale source IPs; virtual hostname resolves to the new target; <code>/etc/hosts</code> and <code>/etc/services</code> correct"],
                      ["3", "Validate SAP profile parameters", "Instance and default profiles match the target design; hostname, DB host, instance numbers and migration-specific parameters correct"],
                      ["4", "Validate webMethods / RFC connections", "Each documented integration reachable and authenticated; middleware endpoints repointed where required"],
                      ["5", "Verify SAP kernel permissions and required SAP/Oracle root scripts", "Kernel executable permissions correct; <code>saproot.sh</code> / Oracle root scripts executed as designed " + pill("source term", "a")],
                      ["6", "Run <code>R3trans -d</code> and confirm return code <code>0000</code> before starting SAP", "The definitive SAP-to-database connectivity check. Any other code must be diagnosed before SAP is started"],
                      ["7", "Start SAP using the appropriate SAP utilities", "<code>sapstart</code>/<code>sapcontrol</code> or the project's start mechanism; instances registered and work processes green"],
                      ["8", "Validate SNC / SSO and certificates", "SNC handshake succeeds, SSO logon works, certificates valid for the new hostnames and domains"],
                      ["9", "Validate Gateway and external connectivity", "<code>SMGW</code> connections as expected; external partners can reach the gateway as designed"],
                      ["10", "Import OS profiles through <code>RZ10</code> where applicable", "Profiles imported and activated; activation and restart behaviour understood"]],
                     caption="Basis post-processing sequence", widths=["5%", "38%", "57%"]))
    out.append(cmd(["<span class='c'># The check that gates SAP start</span>",
                    "su - &lt;sid&gt;adm",
                    "<span class='p'>R3trans -d</span>          <span class='c'># expect: \"R3trans finished (0000)\"</span>",
                    "",
                    "<span class='c'># If it does not return 0000, read the trace before retrying:</span>",
                    "<span class='p'>cat</span> trans.log        <span class='c'># look for DB connect, auth or library errors</span>",
                    "",
                    "<span class='c'># Common non-zero codes to recognise (confirm against your release):</span>",
                    "<span class='c'>#   0000 success · 0004 general error · 0012 database connect failed</span>",
                    "<span class='c'>#   0018 no database authorization / wrong credentials</span>"]))
    out.append(box("risk", "Order matters",
                   para("Starting SAP before <code>R3trans -d</code> returns <code>0000</code> produces a wall of secondary errors in "
                        "the work process traces that hides the real cause, wastes window time, and can leave the system in a state "
                        "that needs a clean restart. Diagnose the database connection first, every time.")))
    out.append(h3("10.3", "Application and functional validation"))
    out.append(bullets([
        "Validate RFC, webMethods, MuleSoft, MBox and other documented integrations " + pill("source term", "a") + ".",
        "Verify inbound and outbound interfaces and application directories.",
        "Validate printers through <code>SPAD</code> (device type, output device, host printer, test page).",
        "The functional team executes business transaction tests and captures evidence — this is their call, not Basis's.",
        "Update Type 3 RFC passwords where required " + pill("source term", "a") + ".",
        "Validate the ChaRM test cycle and transport-management functionality as applicable."]))
    out.append(table(["Validation area", "Owner", "Typical evidence"],
                     [["RFC and middleware interfaces", "Basis + interface owner", "<code>SM59</code> test results, middleware logs, message flow screenshots"],
                      ["Inbound / outbound file interfaces", "Application + Basis", "<code>AL11</code> listings, transferred file counts, timestamps"],
                      ["Printers and spool", "Basis", "<code>SPAD</code> configuration, test page output, <code>SP01</code> spool requests"],
                      ["Business transactions", "Functional team", "Named test scripts with pass/fail per transaction and screenshot evidence"],
                      ["Transports / ChaRM", "Basis + release manager", "Successful test import, ChaRM cycle status, route validation"],
                      ["Authorisations and SSO", "Security + Basis", "Representative user logons per role, SSO success, SNC status"],
                      ["Background jobs", "Basis + job owner", "Job list with release status; a sample job run successfully"],
                      ["Interfaces to external partners", "Interface owner", "Partner confirmation or successful test exchange"]],
                     caption="Functional validation ownership", widths=["26%", "22%", "52%"]))
    out.append(h3("10.4", "Go/No-Go gate"))
    out.append(steps([
        "Collect technical and functional evidence into one pack, indexed by checklist item.",
        "Complete ADPU and relevant quality-assurance sign-offs " + pill("source term", "a") + ".",
        "Obtain confirmation from Basis, application, functional and system-owner teams — by name, not by silence.",
        "Project management and stakeholders review the checklist, the open items and the rollback readiness.",
        "Release the system only after the required approvals and an explicit Go decision."]))
    out.append(table(["Gate input", "What must be true to vote Go"],
                     [["Technical validation", "All Module 4 and Module 6 checks complete or formally deferred with an owner, impact and date"],
                      ["Functional validation", "Named business transactions tested and passed by the functional team"],
                      ["Evidence", "Source and target evidence captured, compared, and attached to the change record"],
                      ["Rollback readiness", "Snapshot and/or final backup verified, DNS rollback path defined, rollback owner present"],
                      ["Approvals", "Basis, application, functional, system owner, PMO — all recorded"],
                      ["Open risks", "Every open item classified by severity with an agreed mitigation; no unexplained critical item"],
                      ["Support readiness", "Hypercare roster, escalation path and ticket routing configured"]],
                     caption="Go/No-Go inputs", widths=["24%", "76%"]))
    out.append(box("ok", "A No-Go is a success when the evidence supports it",
                   para("The gate exists to protect the business, not to approve the project's schedule. Presenting a clean No-Go with "
                        "documented reasons is professional execution. Presenting a Go with open critical items is how migrations "
                        "become incidents.")))
    out.append(h3("10.5", "Rollback"))
    out.append(bullets([
        "If a No-Go decision is made, or a critical issue prevents safe cutover, execute the <b>agreed</b> rollback procedure — the one rehearsed before the window.",
        "Typical technical path: restore the snapshot or recover the source, revert DNS/CNAME to the source, restart the source database and SAP, re-validate connectivity, then re-open the incident path.",
        "Announce the decision, the time and the reason on the bridge and in the change record.",
        "Preserve all evidence from the failed attempt — it is the input to the next attempt.",
        "Confirm with the business which data (if any) was created on the target and how it will be handled."]))
    out.append(h3("10.6", "Go-live and hypercare"))
    out.append(steps([
        "Following Go, unlock users as required (and only the intended user population).",
        "Resume background jobs and Control-M activities with the relevant teams — in the agreed order, not all at once.",
        "Complete remaining EDG / SAProuter configuration as applicable " + pill("source term", "a") + ".",
        "Provide <b>15 days</b> of hypercare, with a named roster and an escalation path.",
        "Classify each issue as migration-related or pre-existing and route it to the responsible support team.",
        "Monitor the leading indicators daily: short dumps, failed jobs, failed interfaces, response time versus baseline, memory, database growth, backup success.",
        "Hold a daily hypercare call, track issues to closure, and report trend rather than incident count alone.",
        "Close hypercare formally: exit criteria met, open items transferred to BAU support with owners, evidence archived."]))
    out.append(table(["Hypercare indicator", "Source", "What a bad trend looks like"],
                     [["Short dumps and runtime errors", "<code>ST22</code>", "New dump types appearing after go-live, or a rising count for a known dump"],
                      ["Failed background jobs", "<code>SM37</code>, Control-M", "Jobs cancelled that previously succeeded; jobs not scheduled at all"],
                      ["Failed interfaces / IDocs", "<code>SM59</code>, <code>WE02</code>/<code>BD87</code>, middleware", "Rising error status, retries not clearing, partner timeouts"],
                      ["Response time", "<code>ST03</code>/<code>ST03N</code>", "Sustained increase over the pre-migration baseline for the same period type"],
                      ["Memory behaviour", "<code>ST02</code>", "Processes moving to PRIVATE mode, rising paging or swap counts"],
                      ["Database health", "<code>DB02</code>, DB alert log", "Tablespace growth beyond forecast, archive destination filling, backup failures"],
                      ["Update errors", "<code>SM13</code>", "Update records stuck or failed — a business-visible data problem"],
                      ["Locks and enqueue", "<code>SM12</code>", "Stale or growing lock entries after go-live"],
                      ["Security and certificates", "<code>STRUST</code>, SNC", "Certificate expiring soon, SNC handshake failures, SSO fallbacks"],
                      ["Backup success", "Backup tool, <code>DB02</code>", "First backup on the target failing or running far longer than the test"]],
                     caption="Daily hypercare monitoring set", widths=["24%", "26%", "50%"]))
    out.append(box("key", "Issue classification during hypercare",
                   para("Compare each issue against the pre-migration baseline before assigning it. “Was this working before?” is "
                        "answerable only if Module 1 recorded the answer. Migration-related issues go to the migration/owning team "
                        "under the project process; pre-existing issues go to BAU support with the baseline evidence attached.")))
    out.append(h3("10.7", "Cutover readiness checklist"))
    out.append(para("This is the short list used on the bridge. The full consolidated version is in <a href='#checklists'>Section 12.5</a>."))
    out.append(checklist("m7", ["Done", "Check", "Status", "Evidence / remarks"], [
        "Cooldown / ramp-up activities complete",
        "Application and web services shut down",
        "DBA handover acknowledged after application shutdown",
        "Final backup and snapshot completed and verified",
        "Source/target synchronization confirmed (SCN or equivalent)",
        "Switchover or recovery executed successfully",
        "DBVERIFY and RMAN completed (Oracle scenario)",
        "SAP global directory synchronized with rsync",
        "Host-file and IPAM entries cleaned and validated",
        "Profile parameters validated",
        "Kernel permissions and root scripts verified",
        "R3trans -d returns 0000",
        "SAP started; instances registered and processes green",
        "SNC / SSO and certificates validated",
        "Gateway and external connectivity validated",
        "RFC, webMethods, MuleSoft, MBox interfaces validated",
        "Printers validated through SPAD",
        "Functional business transaction tests passed with evidence",
        "Type 3 RFC passwords updated where required",
        "ChaRM / transport management validated",
        "Go/No-Go inputs complete; decision recorded with named approvers",
        "Users unlocked after Go",
        "Background jobs and Control-M resumed with the owning teams",
        "EDG / SAProuter configuration completed",
        "Hypercare roster, escalation path and daily monitoring live",
        "Rollback path available until the migration is declared safe",
    ]))
    out.append("</section>")
    return "".join(out)
