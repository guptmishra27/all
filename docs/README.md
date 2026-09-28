# Documentation Index

## CICD Dev-PRD Delivery Platform

| Document | ID | Version | Description |
|----------|----|---------|-------------|
| [Production Operations Runbook](./DOC-RUNBOOK-001-production-operations-runbook.md) | DOC-RUNBOOK-001 | 2.0 | Trunk-based operational procedures: CI, Dev deployment, exact-image promotion to PRD, approval gates, rollback, troubleshooting, audit |
| [Release Checklists](./checklists/release-checklists.md) | — | 2.0 | Printable pre-release, approval, post-deployment, rollback and break-glass checklists |

## Reference Artifacts

Held under `docs/reference/` as reviewable documentation. To activate, copy the workflows into
`.github/workflows/` and substitute `<org>`, `<app>` and cluster identity placeholders.

| File | Implements |
|------|------------|
| [`reference/workflows/ci-pull-request.yml`](./reference/workflows/ci-pull-request.yml) | OPS-01 — PR quality gate (G1–G11) |
| [`reference/workflows/cd-trunk-dev.yml`](./reference/workflows/cd-trunk-dev.yml) | OPS-02/03/04 — build once, publish by digest, deploy and validate Dev |
| [`reference/workflows/cd-release-prd.yml`](./reference/workflows/cd-release-prd.yml) | OPS-06/07/08 — approval gate, exact-image promotion, PRD validation |
| [`reference/workflows/rollback-prd.yml`](./reference/workflows/rollback-prd.yml) | OPS-09 — audited production rollback |
| [`reference/branch-protection.json`](./reference/branch-protection.json) | Appendix B — `main` trunk protection |

## Quick Navigation

| I need to… | Go to |
|------------|-------|
| Ship a change | OPS-01 → OPS-02 → OPS-03 → OPS-04 |
| Release to production | OPS-05 → OPS-06 → OPS-07 → OPS-08 |
| Recover from a bad release | OPS-09, then OPS-10 |
| Fix production urgently | OPS-10 (fix-forward on trunk) |
| Change config or scale | OPS-11 |
| Rotate a secret | OPS-12 |
| Turn a feature on/off | OPS-13 |
| Freeze releases | OPS-14 |
| Act when the pipeline is down | OPS-15 |
| Diagnose a failing deployment | Runbook §24 Troubleshooting |
