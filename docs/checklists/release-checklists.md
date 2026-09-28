# Release Checklists — Printable

Companion to **DOC-RUNBOOK-001 v2.0** (Appendix D). Attach a completed copy to every change ticket.

| Field | Value |
|-------|-------|
| Service | |
| Release tag | `v` |
| Commit SHA | |
| Image digest | `sha256:` |
| Change ticket | |
| Release Manager | |
| Approver (non-author) | |
| Date / window (UTC) | |

---

## 1. Pre-Release — Release Manager (OPS-05)

- [ ] Candidate commit is on `main`; trunk is green
- [ ] OPS-02 build published; digest recorded above
- [ ] OPS-03 Dev deployment succeeded for this exact commit
- [ ] OPS-04 validation passed (V1–V8)
- [ ] Dev soak ≥ 30 min, or expedited justification: ______________________
- [ ] Image signed and provenance attested
- [ ] No unresolved High/Critical vulnerabilities
- [ ] Change ticket approved and linked
- [ ] No active freeze (OPS-14), or exception ref: ______________________
- [ ] Release notes reviewed
- [ ] New feature flags default **off** in PRD (OPS-13)
- [ ] Database changes are backward-compatible (expand/contract) — or N/A
- [ ] Rollback target recorded: revision ______  digest `sha256:____________`
- [ ] Approver identified, available and is **not** the author
- [ ] On-call notified of the release window
- [ ] Signed tag created and pushed

Signed: ____________________  Time (UTC): __________

---

## 2. Production Approval — Approver (OPS-06)

- [ ] A9 — I am **not** the author of this change (SoD-2)
- [ ] A1 — Release tag and commit match the change ticket
- [ ] A2 — Digest equality (Dev == PRD) shown in the run summary
- [ ] A3 — Signature and provenance verified
- [ ] A4 — Dev validation evidence reviewed
- [ ] A5 — Vulnerability posture acceptable
- [ ] A6 — `helm diff` reviewed; no unexpected changes to replicas, resources, probes, secrets or ingress
- [ ] A7 — Release window valid; no freeze
- [ ] A8 — Rollback target present in the summary
- [ ] Approval comment references the change ticket

Approved / Rejected (circle): ____________________  Time (UTC): __________

---

## 3. Post-Deployment — Release Manager / On-Call (OPS-08)

**T+0 to T+2**
- [ ] Rollout completed; all replicas Ready
- [ ] `/healthz`, `/readyz` return 200 on all pods
- [ ] `/version` reports the released commit
- [ ] Running image contains the approved digest

**T+2 to T+15**
- [ ] Read-only smoke suite passed
- [ ] 5xx rate < 0.5% and not above baseline + 0.2pp
- [ ] p95 latency ≤ baseline × 1.2
- [ ] Zero unexpected pod restarts
- [ ] CPU / memory < 80% of limits

**T+15 to T+45**
- [ ] No new Sev-1/Sev-2 alerts
- [ ] Business KPIs within normal band
- [ ] Change ticket updated with tag, digest, Helm revision
- [ ] Release announced; evidence archived (E1–E11)

Closed by: ____________________  Time (UTC): __________

---

## 4. Rollback — On-Call (OPS-09)

- [ ] Decision recorded against the §16.1 matrix; condition: ______________________
- [ ] Flag-disable (OPS-13) considered first — applicable? Y / N
- [ ] Forensic evidence captured **before** pods recycled
- [ ] Rollback executed via `rollback-prd.yml` (or fallback method: ______)
- [ ] Target revision: ______  Restored image digest: `sha256:____________`
- [ ] OPS-08 immediate gates re-verified
- [ ] Stakeholders notified; status page updated if customer-visible
- [ ] Service-scoped release freeze applied
- [ ] Incident raised: INC-______  Severity: ______
- [ ] Post-incident review scheduled (≤ 5 business days)
- [ ] Fix-forward (OPS-10) owner assigned: ______________________

Detected (UTC): ______  Rollback started: ______  Service restored: ______

---

## 5. Break-Glass — On-Call + Platform Lead (OPS-15)

- [ ] Incident declared; break-glass invocation announced with reason
- [ ] Dual authorisation: operator ____________  authoriser ____________
- [ ] Elevated role requested with 60-minute TTL and justification
- [ ] Minimum necessary action taken (prefer reversal over novel change)
- [ ] OPS-08 immediate gates verified
- [ ] Full terminal transcript attached to the incident
- [ ] Role expiry confirmed (`kubectl auth can-i update deploy -n app-prd` → `no`)
- [ ] Git/Helm reconciled with actual cluster state (≤ 1 business day)
- [ ] Post-incident review and security log review completed
