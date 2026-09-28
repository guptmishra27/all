# Minutes of Meeting — Training 2

## Meeting details

| Field | Details |
|---|---|
| **Meeting title** | Training 2 MOM |
| **Date** | September 28 *(year not specified in the source transcript)* |
| **Participant listed in the request** | Gupteswar Mishra |
| **Speakers identified in the transcript** | Gupteswar Mishra, Amit Prajapati, Nikhil Mandlekar |
| **Purpose** | Training on SAP architecture, high availability, migration validation, system startup/shutdown, and infrastructure checks |

> **Transcript note:** The source was an automated Hindi/English transcript with repeated and misrecognized terms. Technical abbreviations have been normalized where the context was clear—for example, **ASCS**, **ERS**, **PAS**, **AAS**, **CMDB**, **UID/GID**, **rsync**, **SNC**, and **RFC**. Exact system-specific names, instance numbers, ports, and file paths should be confirmed against the applicable runbook.

## Executive summary

The session covered the difference between non-HA and HA SAP deployments, the role of ASCS/ERS and the message/enqueue servers, system start and stop order, CMDB and automation handoffs, and the technical validation required after a migration or new server build. Particular emphasis was placed on validating source-to-target parity, preserving UID/GID ownership, separating instance-local from shared directories, and updating host-specific configuration before bringing the target system online.

## Key discussion points

### 1. SAP architecture and HA design

- A single-server/non-HA design is generally suitable for development, testing, or sandbox environments where continuous availability is not required.
- Whether HA or DR is needed should be based on the business criticality of the data and availability requirements—not simply on whether the organization is large or small.
- **ASCS (SAP Central Services)** contains the central enqueue and message-server functions.
  - The enqueue server manages logical locks and enqueue-related processing.
  - The message server distributes users/logons across application servers using load-balancing information.
- **ERS (Enqueue Replication Server)** provides the standby/replication function for ASCS in an HA design.
- Application servers provide work processes such as dialog, update, and background processes. The message server uses the availability/load of these work processes when directing requests.
- The generic left/right diagram is not sufficient to determine the actual topology. Component placement may differ by system and availability zone; a system-specific architecture diagram is required.

### 2. Start and stop sequence

The training discussion established the following normal sequence:

**Start**

1. Database
2. ASCS/Central Services
3. PAS (Primary Application Server)
4. AAS/additional application servers

**Stop — reverse order**

1. AAS/additional application servers
2. PAS
3. ASCS/Central Services
4. Database

The exact ERS sequence and failover handling must be documented separately in the HA runbook. Application servers depend on Central Services/message-server communication; if the central or message-server layer is unavailable, an application server may not start or may not operate correctly.

### 3. HA failover and availability zones

- In an HA arrangement, the standby component continuously monitors the active component, typically through health checks or heartbeats.
- If the active component stops responding, the standby should take over according to the HA mechanism and runbook.
- The primary/standby placement is not inherently tied to the left or right side of a generic diagram. The actual placement across availability zones must be designed per system.
- The discussion stated that HA application-server layouts should use an even number of servers where pairing is required. This should be treated as a design standard to confirm for the target architecture rather than assumed for every SAP deployment.
- A system-specific diagram should show the database, ASCS/ERS, PAS, AAS, availability zones, and the expected failover path.

### 4. Automation, AWS resources, and CMDB

- The automation team provisions or updates infrastructure such as AWS resources, VPCs, instances, and database-related components.
- After the automation handoff, the Basis/technical team validates that the delivered infrastructure matches the requested design and inventory.
- **CMDB (Configuration Management Database)** was described as the central registry of configuration items. For a given SID, it records the associated servers/instances and components, such as ASCS/ERS, PAS/AAS, and the database.
- The CMDB should be used to reconcile the requested server count and the instances actually delivered.

### 5. Migration and target-system validation

The following checks were discussed as part of the migration/build validation checklist:

- **Inventory:** Confirm that the number of servers and instances delivered matches the request.
- **File systems:** Use file-system checks such as `df -h` to verify mount points, sizes, and availability. Target capacity must not be below the source or the agreed minimum requirement. Required file systems must be mounted.
- **Memory:** Compare main memory and swap memory between source and target. The target may have more capacity, but it must not be below the agreed minimum.
- **Operating system:** Verify the kernel version, OS release, and other required platform versions.
- **Users and groups:** Confirm that relevant SAP, database, administrator, and service users exist and that source and target UID/GID values match. Mismatches can cause ownership, permission, and inter-system communication problems.
- **Packages and libraries:** Confirm that required packages/libraries are present on the target and that package/version checks are consistent with the source requirement.
- **Directory/file transfer:** Use `rsync` or the approved transfer method to copy required data from source to target. Validate the source and target paths carefully.
- **File counts:** Compare the file count for each transferred path. The target count should not be lower; any difference or unexpected additional files should be investigated.
- **Path correctness:** Avoid accidentally creating a directory inside the intended destination directory. A small path error can prevent the system from starting even when the major components appear correct.
- **Evidence:** Capture command output or screenshots showing that the checks were completed and that the system is running as expected.

### 6. Local versus shared SAP directories

- Instance-specific paths under `/usr/sap/<SID>` are local to the relevant instance/server and may contain items such as instance executables, logs, work, and security-related files.
- The shared SAP mount, commonly represented as `/sapmnt/<SID>` or SAPMNT in the discussion, is shared across the system's servers.
- A change made in a shared repository can affect all relevant servers in the SID. A change made in an instance-local directory should affect only that instance/server.
- Profiles, kernel files, gateway-related files, interface/transport files, and other shared content must be classified correctly before copying or editing them.
- Naming conventions for copied source data are acceptable for identification, but the destination path and runtime configuration must remain correct.

### 7. Profiles, hostnames, and services

- SAP services read the relevant profile during startup. The default/global profile and instance profiles must be reviewed after source-to-target copying.
- Source physical and virtual hostnames/domains must be replaced with the target values where required. Leaving the source host/domain in the target profile can prevent connectivity and system startup.
- Gateway profiles and message-server access controls must be reviewed.
- **MS ACL (Message Server Access Control List)** entries must contain the correct target host information.
- Security and registration information such as `secinfo` and `reginfo` must be reviewed; security entries should be updated for the target hosts according to the approved procedure.
- SNC (Secure Network Communication), SSL certificates, credential storage, and related security settings must be checked after migration.
- SNC configuration may be required on all application servers, depending on the system design.

### 8. Process and status checks

- The SAPControl process-list check was demonstrated as the way to confirm whether an instance is running and whether its processes are healthy. The command discussed was equivalent to:

  ```text
  sapcontrol -nr <instance_number> -function GetProcessList
  ```

- The check should include the message server, enqueue server, gateway, and relevant application-server processes.
- A stopped or unhealthy central/message-server process can block application-server startup or prevent normal system communication.
- The resulting status should be retained as validation evidence.

### 9. SID, instance numbers, ports, RFC, and SNC

- A SAP SID is three alphanumeric characters.
- Instance numbers are system-specific and may vary by component. Port numbers are derived from or assigned with the relevant instance configuration and must be verified rather than assumed.
- RFC (Remote Function Call) supports communication between systems/components. The discussion compared this concept with inter-system/business-function integrations used in other platforms.
- SNC provides secure network communication and may support authentication or single sign-on requirements.

### 10. Oracle versus HANA memory configuration

- Large memory pages/HugePages and related Linux memory-management checks are relevant to Oracle configurations discussed in the session.
- The same check may be marked not applicable for HANA where the target standard does not require it.
- The exact command, threshold, and applicability should be documented in the platform-specific checklist rather than copied between Oracle and HANA systems.

## Decisions and agreed guidance

1. Select HA/DR based on business criticality, recovery requirements, and availability needs.
2. Use a single-server architecture primarily for development, testing, or sandbox use where appropriate.
3. Start the system from the database upward through Central Services and then the application tiers; stop it in reverse order.
4. Treat CMDB as the authoritative registry for SID-related configuration items and server/instance associations.
5. Do not assume that a generic architecture diagram represents the actual availability-zone placement.
6. Do not proceed with target startup until source-to-target file systems, memory, OS, users/groups, packages, profiles, hostnames, security files, and process status have been validated.
7. Run the first end-to-end validation/execution with guidance and retain command output or screenshots as evidence.

## Action items

| # | Action | Owner | Due/status |
|---|---|---|---|
| 1 | Share a system-specific architecture diagram showing availability-zone placement, ASCS/ERS, database, PAS, AAS, and failover behavior. | Nikhil / training team | Before the next relevant training or migration review; date not specified |
| 2 | Share the additional explanation/diagram for large memory pages/HugePages and clarify Oracle versus HANA applicability. | Nikhil / training team | Pending; date not specified |
| 3 | Update the migration checklist/runbook to include inventory, `df -h`, memory/swap, OS/kernel, UID/GID, packages/libraries, rsync paths/counts, local/shared directories, profiles, hostnames, MS ACL, `secinfo`/`reginfo`, SNC, SSL, and process-list checks. | Basis/migration team | Pending |
| 4 | Confirm the exact HA start/stop and ERS failover procedure for the target architecture. | Basis/HA design team | Pending architecture confirmation |
| 5 | Validate automation-team deliverables against the requested design and CMDB inventory, including server count, instances, mounts, and resources. | Automation team and Basis/technical team | After infrastructure handoff |
| 6 | Perform the first migration validation/execution under guidance, then repeat the process independently after the workflow is understood. | Gupteswar Mishra, with Nikhil’s guidance | On the first applicable migration |
| 7 | Prepare a validation/test script and retain screenshots or command output proving that the target system and key processes are healthy. | Migration/Basis team | Before handover or sign-off |

## Open points to confirm

- Exact availability-zone placement and failover topology for the target system.
- Exact instance numbers, port assignments, and hostnames for each component.
- The approved list of shared versus instance-local directories for each SID.
- The required `secinfo`/`reginfo`, MS ACL, SNC, SSL, and credential changes for the target environment.
- The platform-specific HugePages/memory requirements for Oracle and HANA.
- The final automation/CMDB handoff format and sign-off criteria.
