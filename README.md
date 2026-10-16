# Quantum Integrators — AI SRE Copilot Dev Pilot

> **Internal Development Pilot • Google Cloud • GSK Excluded**  
> **Tier-1 Enhanced Charter — Ready for Approval**

---

## At a Glance

| Item | Detail |
|---|---|
| **Proposal** | AI SRE Copilot — Controlled, evidence-linked diagnosis with deterministic policy validation & mandatory human approval |
| **Environment** | QI internal GCP project — `us-east1` / `us-central1` |
| **Duration** | 4–6 weeks (from approval + access readiness) |
| **Budget ceiling** | **USD 250** — planning estimate, period to be confirmed (full pilot vs. monthly) |
| **Scope** | Start with **2** Cloud Run services → scale to **≤20** on cost signal |
| **Document ID** | `QI-AI-SRE-2026-001` • **v2.0 Enhanced** (supersedes v1.0 dated 16 Oct 2026) |
| **Owners** | Coordinator: **Gupteswar Mishra** • Tech Lead: **Akshay Saxena** • Sponsors: **Ken / Prithiviraj** |
| **Classification** | Confidential — QI Internal • Not for external distribution |

**Design axiom:** `AI proposes → deterministic policy validates → authorized human approves → protected workflow executes → health checks verify → audit records persist.`

**Go / No-Go rule:** Privileged remediation stays **disabled** until IAM isolation, approval-binding, and all 8 adversarial bypass tests pass (Gate 4, jointly signed).

---

## 📄 Documents

| File | Description |
|---|---|
| [`AI_SRE_Copilot_Dev_Pilot_Proposal_QI.pdf`](./AI_SRE_Copilot_Dev_Pilot_Proposal_QI.pdf) | **Original v1.0** — 7-page working draft (retained for traceability, unchanged) |
| [`docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.html`](./docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.html) | **Enhanced v2.0 — Interactive charter** (recommended). Sticky TOC, diagrams, callouts, print-to-PDF via browser. **Open this file to review.** |
| [`docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.pdf`](./docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.pdf) | **Enhanced v2.0 — Print-ready PDF** (12 pages, A4, paginated, cover + header/footer). Archive as signed record. |
| [`docs/RUNBOOK_E2E.html`](./docs/RUNBOOK_E2E.html) | **🏃 End-to-End Runbook (NEW)** — Faithful HTML poster (13 sections) + clickable runbook (1→8 flow, T1–T8, Gates 0–6, 5 scenario playbooks). **Print poster + execute.** |
| [`docs/RUNBOOK_E2E.md`](./docs/RUNBOOK_E2E.md) | **Runbook — Markdown** — Same content as HTML for git diff / CLI. |
| [`docs/REVIEW_AND_ENHANCEMENTS.md`](./docs/REVIEW_AND_ENHANCEMENTS.md) | **Review & Enhancement Report** — gap analysis vs. Tier-1, before/after, reviewer guide. |
| [`docs/generate_pdf.py`](./docs/generate_pdf.py) | Reproducible PDF generator (ReportLab). Run `python3 docs/generate_pdf.py` to rebuild. |

### How to Review (Pick Your Depth)

- **10 min — Executive:** Open the **HTML** → read **Cover** + **§0 Executive Summary** + **§12 Decisions & Next Steps**.
- **30 min — Steering:** Above + **§4 Architecture** (diagram) + **§8 Budget** (bar) + **§10 Risks** + **§11 Governance**.
- **60 min — Full Audit:** Linear read; linger on **§5 Security checklist**, **§6 Bypass matrix**, **Appendix B (schema)** and **D (scoring)**.

---

## 🛡️ Scope Boundary

> **This pilot is QI-internal only.** It does not authorize access to, deployment in, or use of credentials or data from **GSK**. Any future GSK implementation requires a separate architecture, security, access, budget, and go-live approval package. Violation = immediate pilot pause.

**Allow-listed actions only:** rollback to previous revision, redeploy approved revision, restart/scale within bounds, toggle pre-approved feature flag.  
**Prohibited:** IAM changes, DB operations, quota increases, regional failover, arbitrary commands.

---

## ✅ Decisions Requested (This Week)

| # | Decision | Owner | Gate |
|---|---|---|---|
| D1 | Approve QI-only scope; explicitly exclude GSK | Ken / Prithiviraj | Before Gate 0 |
| D2 | Confirm USD 250 period (full pilot vs. monthly) | Sponsors + Finance | Before Gate 0 |
| D3 | Confirm named owners, approvers & escalation contacts | Coordinator | Kickoff |
| D4 | Confirm GitHub plan supports required approval controls | CI/CD Owner | Gate 0 |
| D5 | Approve synthetic / QI-approved data + redaction | Security + Sponsors | Gate 0 |
| D6 | Authorize provisioning only after readiness gate | Sponsors | Gate 0 sign-off |
| D7 | Require final review before any extension / prod / GSK | Sponsors | Standing |

**Next 5 days:** Day 1–2 Decision log + RACI → Day 3 Gate 0 preflight → Day 4 Security review → Day 5 Gate 0 sign-off → Week 1 starts.

---

## 🗓️ Stage-Gated Delivery (4–6 Weeks)

| Phase | Timing | Exit Gate |
|---|---|---|
| **0 — Approval & Readiness** | Before Week 1 | All readiness checks green; no provisioning before |
| **1 — Foundation & Security** | Week 1 | IAM isolation demonstrated; cost alerts live |
| **2 — Monitoring & Intake** | Week 2 | Alert → incident → evidence bundle traceable |
| **3 — AI Diagnosis** | Week 3 | ≥5 dry-runs scored; allowlist rejects verified |
| **4 — CI/CD & Approval** | Week 4 | **All 8 bypass tests pass — remediation enabled only now** |
| **5 — Scenario Evaluation** | Week 5 | 5 scenarios + ≥10 scored runs complete |
| **6 — Review & Clean-up** | Week 6 | Proceed / Extend / Stop recommendation + GSK-separation attestation |

---

## 💰 Budget & Success Criteria

**Ceiling: USD 250** — Cloud Run $45 + Grafana $40 + Vertex AI $55 + Logs $30 + Artifacts $20 + Contingency $60 (coordinator-gated).  
Alerts at 50/75/90/100% are **notify, not hard caps** — operational stop procedure tested separately.

**Pilot acceptance (zero-tolerance bold):**

- ≥90% correct primary diagnosis (≥10 runs, labelled live vs. simulated) — *pilot signal, not statistical proof*
- All 5 scenarios exercised • **Zero** infra changes outside approved workflows
- **100%** privileged remediations have pre-execution approval • **Zero** automated IAM/DB/failover
- Full trace per run (evidence → recommendation → decision → outcome) • Duplicate protection
- Median alert→approved-fix vs. manual baseline • Spend within envelope • **No GSK touch**

---

## 🏛️ Governance

| Role | Owner |
|---|---|
| Business Sponsors | Ken / Prithiviraj — budget & pilot authorization |
| Pilot Coordinator | Gupteswar Mishra — scope, dependencies, final recommendation |
| Technical Lead | Akshay Saxena — blueprint, build, integration, testing |
| Cloud / Platform | Assigned Engineer — GCP, billing, IAM, quotas |
| CI/CD Owner | Assigned Engineer — workflows, approval gates |
| Security Reviewer | Assigned Reviewer — data handling, guardrails, bypass review |
| Approvers | Named Engineers (≥2) — per-proposal decision |

Cadence: daily stand-up during build/test, weekly steering, gate sign-offs 0–6 (written, not verbal).

---

## 🔍 Original vs. Enhanced

See [`docs/REVIEW_AND_ENHANCEMENTS.md`](./docs/REVIEW_AND_ENHANCEMENTS.md) for full gap analysis and before/after.

**In short:** Substance preserved, structure elevated to Tier-1 — pyramid summary, zero-trust detail, stage gates with exit criteria, unit-economics + sensitivity, RAID with owners, RACI, 8-row adversarial matrix, and Appendix pack (schemas, workflow spec, cost assumptions, scoring protocol, document control). No numbers or commitments altered.

---

## 🚀 Local Preview

```bash
# Interactive HTML (recommended)
open docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.html
# or: python3 -m http.server 8000  # then http://localhost:8000/docs/...

# Rebuild PDF
pip install --break-system-packages reportlab
python3 docs/generate_pdf.py
# → docs/AI_SRE_Copilot_Dev_Pilot_Proposal_QI_Enhanced.pdf (12 pages)
```

---

*Quantum Integrators — Confidential • QI Internal • GSK Excluded • 16 Oct 2026 • QI-AI-SRE-2026-001 v2.0 Enhanced*
