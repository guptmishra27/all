# CICD Dev-PRD Delivery Platform — Production Operations Runbook

**Document ID:** DOC-RUNBOOK-001
**Version:** 2.0
**Status:** Approved for Operational Use
**Classification:** Internal
**Delivery Model:** Trunk-Based Development (TBD)
**Prepared By:** Platform Engineering Team
**Reference Architecture:** DOC-HLDD-001, Version 1.0, 25-Sep-2026
**Supersedes:** DOC-RUNBOOK-001 Version 1.0 (branch-per-environment model)
**Effective Date:** 28-Sep-2026
**Next Review:** 28-Mar-2026 (6-monthly) or on material architecture change

---

## Table of Contents

**Part A — Governance**
1. [Document Control](#1-document-control)
2. [Scope](#2-scope)
3. [Platform Overview](#3-platform-overview)
4. [Trunk-Based Delivery Model](#4-trunk-based-delivery-model)
5. [Environments and Topology](#5-environments-and-topology)
6. [Roles, Responsibilities and Access](#6-roles-responsibilities-and-access)
7. [Artifact Identity and Versioning](#7-artifact-identity-and-versioning)

**Part B — Standard Operating Procedures**
8. [OPS-01 — Pull Request Continuous Integration](#8-ops-01--pull-request-continuous-integration)
9. [OPS-02 — Trunk Merge and Artifact Publication](#9-ops-02--trunk-merge-and-artifact-publication)
10. [OPS-03 — Dev Deployment](#10-ops-03--dev-deployment)
11. [OPS-04 — Dev Validation and Smoke Test](#11-ops-04--dev-validation-and-smoke-test)
12. [OPS-05 — Release Candidate Selection and Tagging](#12-ops-05--release-candidate-selection-and-tagging)
13. [OPS-06 — Production Approval Gate](#13-ops-06--production-approval-gate)
14. [OPS-07 — Production Deployment (Exact-Image Promotion)](#14-ops-07--production-deployment-exact-image-promotion)
15. [OPS-08 — Production Validation](#15-ops-08--production-validation)
16. [OPS-09 — Rollback and Recovery](#16-ops-09--rollback-and-recovery)
17. [OPS-10 — Hotfix (Fix-Forward on Trunk)](#17-ops-10--hotfix-fix-forward-on-trunk)
18. [OPS-11 — Configuration-Only Change](#18-ops-11--configuration-only-change)
19. [OPS-12 — Secret Management and Rotation](#19-ops-12--secret-management-and-rotation)
20. [OPS-13 — Feature Flag Operations](#20-ops-13--feature-flag-operations)
21. [OPS-14 — Deployment Freeze and Release Windows](#21-ops-14--deployment-freeze-and-release-windows)
22. [OPS-15 — Break-Glass Emergency Deployment](#22-ops-15--break-glass-emergency-deployment)

**Part C — Operations**
23. [Monitoring, Alerting and Service Levels](#23-monitoring-alerting-and-service-levels)
24. [Troubleshooting Guide](#24-troubleshooting-guide)
25. [Incident Management](#25-incident-management)
26. [Audit, Evidence and Compliance](#26-audit-evidence-and-compliance)
27. [Delivery Performance Metrics](#27-delivery-performance-metrics)

**Part D — Appendices**
- [Appendix A — Command Reference](#appendix-a--command-reference)
- [Appendix B — Branch Protection and Repository Configuration](#appendix-b--branch-protection-and-repository-configuration)
- [Appendix C — Reference Workflow Implementations](#appendix-c--reference-workflow-implementations)
- [Appendix D — Operational Checklists](#appendix-d--operational-checklists)
- [Appendix E — RACI Matrix](#appendix-e--raci-matrix)
- [Appendix F — Glossary](#appendix-f--glossary)
- [Appendix G — Document History and Approval](#appendix-g--document-history-and-approval)

---

# Part A — Governance

## 1. Document Control

### 1.1 Purpose

This Runbook provides standardized, repeatable operational procedures for building, deploying, validating, promoting, monitoring and recovering the **CICD Dev-PRD Delivery Platform** under a **trunk-based development** model.

It translates the approved High-Level Design (DOC-HLDD-001) into executable operational procedure for:

- Continuous Integration on every change
- Continuous delivery to the Dev environment from trunk
- Exact-image promotion from Dev to Production
- Explicit, auditable Production approval
- Deployment verification through probes and smoke tests
- Rollback, recovery and fix-forward
- Troubleshooting and failure handling
- Secret management and rotation
- Operational audit and evidence retention

### 1.2 Design Principles Inherited from DOC-HLDD-001

| # | Principle | Operational Consequence |
|---|-----------|-------------------------|
| P1 | Git is the single declarative control plane | No change reaches any environment except through a commit on trunk. Console edits are prohibited. |
| P2 | Helm is the single deployment mechanism | `kubectl apply` of ad-hoc manifests is prohibited in Dev and PRD. |
| P3 | Application artifacts are immutable | Images are addressed by digest. Tags are never re-pointed. Rebuilds for promotion are prohibited. |
| P4 | Production is gated explicitly | PRD deployment requires a GitHub Environment approval by an authorised approver who is not the change author. |
| P5 | Least privilege | No human holds standing write credentials to the PRD namespace. Pipelines use short-lived OIDC-federated identities. |
| P6 | Deployment is verified, not assumed | A release is complete only after readiness, rollout completion and smoke tests pass. |
| P7 | Every change is reversible | Every PRD release has a known-good predecessor digest and a rehearsed rollback path. |

### 1.3 Change from Version 1.0

Version 1.0 assumed a branch-per-environment model (`develop` → `release/*` → `main`). Version 2.0 adopts **trunk-based development**: one long-lived branch (`main`), short-lived change branches, release by immutable tag, and fix-forward as the default remediation. Sections 4, 12, 17 and Appendix B are new or substantially rewritten; all OPS procedures have been renumbered and re-baselined.

### 1.4 Intended Audience

Platform Engineers, Application Developers, Release Managers, Production Approvers, Site Reliability Engineers, On-Call Responders, Internal Audit.

### 1.5 Conventions

| Convention | Meaning |
|------------|---------|
| `<org>` | GitHub organisation name |
| `<app>` | Application / service name |
| `MUST` / `MUST NOT` | Mandatory control. Deviation is an audit finding. |
| `SHOULD` | Strong recommendation. Deviation requires a recorded reason. |
| `MAY` | Discretionary. |
| ⚠️ | Destructive or production-impacting step. Requires confirmation. |

All shell examples assume `kubectl`, `helm` (v3.12+), `gh` (GitHub CLI), `jq` and `cosign` are installed and authenticated.

---

## 2. Scope

### 2.1 In Scope

1. GitHub repository, trunk-based branching and merge workflow.
2. GitHub Actions CI and CD workflows.
3. GitHub Container Registry (GHCR) artifact publication and retention.
4. Kubernetes Dev (`<app>-dev`) and Production (`<app>-prd`) namespaces.
5. Helm-based application deployment and configuration.
6. Application health, readiness and smoke-test validation.
7. Production approval and release execution.
8. Exact-image (digest-pinned) promotion from Dev to PRD.
9. Automatic and manual rollback, and fix-forward remediation.
10. Failure handling and troubleshooting.
11. Secret provisioning, rotation and revocation.
12. Deployment audit trail and operational evidence.

### 2.2 Out of Scope

The following are not covered by this runbook unless separately documented and referenced here:

1. Kubernetes cluster lifecycle (provisioning, upgrade, node pool management) — see DOC-RUNBOOK-010.
2. Network, ingress controller, DNS and certificate authority administration — see DOC-RUNBOOK-011.
3. Database schema migration strategy and data lifecycle — see DOC-RUNBOOK-020.
4. Stateful backup and disaster-recovery of persistent data — see DOC-DRP-001.
5. Application source-code design, unit test authorship and functional test strategy.
6. Corporate identity provider, SSO and joiner/mover/leaver processes.
7. Cost management, capacity planning and licence administration.
8. Non-Kubernetes workloads, third-party SaaS integrations and vendor-managed services.

### 2.3 Assumptions

- A single Kubernetes cluster hosts both namespaces, isolated by RBAC, NetworkPolicy and ResourceQuota. Multi-cluster variants follow identical procedure with a different `--kube-context`.
- The application is stateless at the pod level; session and persistence are externalised.
- GHCR is reachable from the cluster via an image pull secret or workload identity.
- Observability stack (metrics, logs, alerting) is operational and independent of the delivery pipeline.

---

## 3. Platform Overview

### 3.1 Delivery Flow

```
            ┌─────────────────────────── TRUNK-BASED FLOW ───────────────────────────┐

  Developer          GitHub (main = trunk)              GHCR                Kubernetes
  ─────────          ────────────────────               ────                ──────────

  short-lived
  branch  ──PR──▶  [ OPS-01 CI Gate ]
                    lint · unit · SAST
                    build · scan · IaC
                        │ all green + 1 review
                        ▼
                   [ merge queue ]
                        │
                        ▼
                    main (trunk) ──▶ [ OPS-02 Build & Publish ]
                                        image: sha-<commit>
                                        digest: sha256:… ──────▶ GHCR
                                                                   │
                                                                   ▼
                                     [ OPS-03 Deploy Dev ] ─────────────▶ <app>-dev
                                                                             │
                                                     [ OPS-04 Validate Dev ] │
                                                                             ▼
                                     [ OPS-05 Tag RC: vX.Y.Z ]           PASS/FAIL
                                                │
                                                ▼
                                     [ OPS-06 Approval Gate ] ⚠ human, non-author
                                                │
                                                ▼
                                     [ OPS-07 Deploy PRD ] ──same digest──▶ <app>-prd
                                                │
                                     [ OPS-08 Validate PRD ]
                                                │
                                      pass ─────┴───── fail ──▶ [ OPS-09 Rollback ]
                                                                 └▶ [ OPS-10 Fix-Forward ]
```

### 3.2 Component Inventory

| Component | Identifier | Owner | Purpose |
|-----------|------------|-------|---------|
| Source repository | `github.com/<org>/<app>` | Application Team | Application source, Helm chart, workflows |
| Trunk branch | `main` | Platform Engineering | Single integration branch; always releasable |
| CI workflow | `.github/workflows/ci-pull-request.yml` | Platform Engineering | PR quality gate |
| CD Dev workflow | `.github/workflows/cd-trunk-dev.yml` | Platform Engineering | Build, publish, deploy Dev |
| CD PRD workflow | `.github/workflows/cd-release-prd.yml` | Platform Engineering | Gated promotion to PRD |
| Rollback workflow | `.github/workflows/rollback-prd.yml` | Platform Engineering | Operator-triggered PRD rollback |
| Container registry | `ghcr.io/<org>/<app>` | Platform Engineering | Immutable image storage |
| Helm chart | `charts/<app>` (in-repo) | Application Team | Kubernetes manifests |
| Dev namespace | `<app>-dev` | Application Team | Continuous deployment target |
| PRD namespace | `<app>-prd` | Platform Engineering | Gated production target |
| GitHub Environment `dev` | repo setting | Platform Engineering | Dev secrets/vars, no reviewers |
| GitHub Environment `prd` | repo setting | Platform Engineering | PRD secrets/vars, required reviewers |

### 3.3 Repository Layout (reference)

```
.
├── .github/
│   └── workflows/
│       ├── ci-pull-request.yml      # OPS-01
│       ├── cd-trunk-dev.yml         # OPS-02, OPS-03, OPS-04
│       ├── cd-release-prd.yml       # OPS-06, OPS-07, OPS-08
│       └── rollback-prd.yml         # OPS-09
├── charts/<app>/
│   ├── Chart.yaml
│   ├── values.yaml                  # chart defaults only
│   ├── values-dev.yaml              # Dev overlay
│   ├── values-prd.yaml              # PRD overlay
│   └── templates/
├── docs/
│   ├── DOC-RUNBOOK-001-production-operations-runbook.md
│   ├── checklists/
│   └── reference/
├── src/
└── tests/
    └── smoke/                       # environment-agnostic smoke suite
```

---

## 4. Trunk-Based Delivery Model

> This section is normative. Any deviation requires a documented exception approved by the Platform Engineering Lead.

### 4.1 Model Definition

The platform operates **one long-lived branch: `main` (the trunk)**. `main` is permanently releasable: every commit on it has passed the full CI gate and is a legitimate release candidate.

There are **no** `develop`, `release/*`, `hotfix/*` or environment branches. Environments are distinguished by *which immutable artifact is deployed*, not by *which branch exists*.

### 4.2 Branch Rules

| Rule | Requirement |
|------|-------------|
| TBD-1 | `main` is the only long-lived branch and is protected (Appendix B). |
| TBD-2 | All work occurs on short-lived branches named `<type>/<ticket>-<slug>`, e.g. `feat/PLT-482-retry-policy`, `fix/PLT-501-null-header`, `chore/PLT-512-bump-helm`. |
| TBD-3 | A change branch MUST live **no longer than 48 hours** and SHOULD be merged within 24 hours. Branches older than 72 hours are reported by the Branch Age report and MUST be merged, split or deleted. |
| TBD-4 | A pull request SHOULD change **fewer than 400 lines**. Larger changes MUST be decomposed into incremental, independently releasable commits. |
| TBD-5 | Change branches MUST be rebased/updated onto `main` before merge. The merge queue enforces this. |
| TBD-6 | Merge strategy is **squash merge** only. One PR = one commit on trunk = one deployable artifact. |
| TBD-7 | The source branch is deleted automatically on merge. |
| TBD-8 | Direct pushes to `main` are prohibited for all principals, including administrators. No exceptions; break-glass is OPS-15. |
| TBD-9 | Force-push and branch deletion on `main` are blocked at the repository level. |
| TBD-10 | Incomplete functionality is merged **dark** behind a feature flag (OPS-13), never held on a branch. |

### 4.3 Why Trunk-Based for This Platform

| Concern | Trunk-based control |
|---------|---------------------|
| Merge conflict and integration risk | Eliminated by continuous integration into a single trunk at least daily. |
| Environment drift | Impossible: Dev and PRD run artifacts from the same linear commit history. |
| "Which branch is in production?" | Never asked. Production runs a tagged commit of `main`, identified by digest. |
| Hotfix divergence | No parallel maintenance branch; hotfix is a normal PR to trunk, fast-tracked (OPS-10). |
| Release traceability | `vX.Y.Z` tag → commit SHA → image digest → PRD ReplicaSet. One unbroken chain. |
| Unfinished work blocking release | Prevented by feature flags and incremental delivery, not by branch isolation. |

### 4.4 Release Model

- **Release from trunk by tag.** A release is an annotated, signed Git tag `vX.Y.Z` applied to a commit on `main` that has already been validated in Dev.
- **No release branch is created.** If a released commit needs a correction, the correction is a new commit on trunk and a new tag (`vX.Y.Z+1`).
- **Release cadence:** on-demand, up to multiple times per day. There is no batching requirement.
- **Roll-forward is the default remediation**; rollback (OPS-09) is the containment action used to restore service while the fix-forward is prepared.

### 4.5 Definition of "Trunk is Broken"

Trunk is broken when the post-merge workflow (OPS-02/03/04) fails on `main`. When trunk is broken:

1. The Merge Queue is paused automatically by the failing required check.
2. Fixing trunk takes **priority over all other work** for the author of the breaking commit.
3. If a fix is not identified within **15 minutes**, the breaking commit MUST be reverted (`git revert`) via an expedited PR. Reverting is never treated as failure.
4. No release tag may be cut while trunk is red.

### 4.6 Commit Convention

Conventional Commits are mandatory; they drive automated semantic versioning and the release note generator.

```
<type>(<scope>): <summary>        # type ∈ feat|fix|perf|refactor|docs|test|build|ci|chore
                                  # BREAKING CHANGE: footer ⇒ major bump
```

| Commit type | Version impact | Example |
|-------------|----------------|---------|
| `fix:` | PATCH | `fix(api): reject empty tenant header` |
| `feat:` | MINOR | `feat(api): add idempotency key support` |
| `feat!:` or `BREAKING CHANGE:` footer | MAJOR | `feat(api)!: remove v1 payload schema` |
| `chore:`, `docs:`, `ci:`, `test:` | none | `chore(deps): bump helm to 3.15.2` |

---

## 5. Environments and Topology

### 5.1 Environment Matrix

| Attribute | Dev | Production (PRD) |
|-----------|-----|------------------|
| Namespace | `<app>-dev` | `<app>-prd` |
| GitHub Environment | `dev` | `prd` |
| Trigger | Automatic on every merge to `main` | Manual: tag push + approval |
| Approval required | No | Yes — 1 approver, non-author |
| Helm release name | `<app>` | `<app>` |
| Values overlay | `values.yaml` + `values-dev.yaml` | `values.yaml` + `values-prd.yaml` |
| Image reference | `ghcr.io/<org>/<app>@sha256:…` | Identical digest, promoted unchanged |
| Replicas (baseline) | 1 | 3 (HPA 3–10) |
| Resources (baseline) | 100m / 128Mi req | 500m / 512Mi req, 1000m / 1Gi lim |
| PodDisruptionBudget | none | `minAvailable: 2` |
| Deployment strategy | RollingUpdate 25%/25% | RollingUpdate `maxUnavailable: 0`, `maxSurge: 1` |
| Data | Synthetic only | Live customer data |
| Log level | `debug` | `info` |
| Retention of Helm history | 5 revisions | 20 revisions |
| Human write access | Team-scoped, time-bound | None standing (break-glass only) |

### 5.2 Guardrails

| Guardrail | Enforcement |
|-----------|-------------|
| PRD namespace admission | Only images from `ghcr.io/<org>/*`, digest-pinned. Enforced by admission policy. |
| Resource limits mandatory | `LimitRange` + policy rejection of unbounded containers. |
| Non-root, read-only rootfs | Pod Security Admission `restricted` on `<app>-prd`. |
| Namespace quota | `ResourceQuota` per namespace prevents noisy-neighbour exhaustion. |
| Network egress | Default-deny `NetworkPolicy`; egress allowlisted per dependency. |
| Image provenance | `cosign verify` of the build attestation before PRD apply. |

---

## 6. Roles, Responsibilities and Access

### 6.1 Roles

| Role | Responsibility | GitHub permission | Kubernetes permission |
|------|----------------|-------------------|-----------------------|
| Developer | Author change, keep branch short-lived, fix broken trunk, validate Dev | `write` (no bypass) | `view` on `<app>-dev` |
| Reviewer | Review PR for correctness, security, operability | `write` | — |
| Release Manager | Cut release tag, own release window, coordinate comms | `write` + tag push | `view` on `<app>-prd` |
| Production Approver | Approve/reject the PRD gate; never approves own change | `prd` environment reviewer | — |
| Platform Engineer | Own pipelines, cluster config, rollback execution | `maintain` | `edit` on both namespaces via pipeline identity |
| On-Call Responder | Detect, triage, contain, invoke rollback/break-glass | `write` | break-glass role (OPS-15) |
| Internal Audit | Review evidence | `read` | `view` (read-only) |

### 6.2 Separation of Duties (mandatory controls)

| Control | Statement |
|---------|-----------|
| SoD-1 | The author of a change MUST NOT approve their own pull request. |
| SoD-2 | The author of a change MUST NOT approve the PRD deployment gate for that change. |
| SoD-3 | No human account holds standing `edit` rights on `<app>-prd`. Pipeline identity only. |
| SoD-4 | Registry write is restricted to the CD workflow identity; humans have `read` only. |
| SoD-5 | Break-glass access (OPS-15) is time-boxed to 60 minutes, fully logged, and reviewed within 1 business day. |

### 6.3 Pipeline Identity

- Workflows authenticate to the cluster using **OIDC workload-identity federation** with a `sub` claim bound to `repo:<org>/<app>:environment:dev` or `:environment:prd`.
- Long-lived kubeconfigs and static cloud keys MUST NOT be stored as repository secrets.
- `GITHUB_TOKEN` permissions default to `contents: read`; each job elevates only what it needs (`packages: write`, `id-token: write`, `attestations: write`).

---

## 7. Artifact Identity and Versioning

### 7.1 Identity Chain

```
commit SHA  ─▶  image tag sha-<short-sha>  ─▶  image digest sha256:…  ─▶  running ReplicaSet
     ▲                                                   │
     └──────────── release tag vX.Y.Z ──────────────────┘
```

Every deployed pod MUST be traceable to a commit in ≤ 2 lookups. The digest is the authoritative identity; tags are human conveniences.

### 7.2 Tagging Rules

| Tag | Applied when | Mutable? | Purpose |
|-----|--------------|----------|---------|
| `sha-<short-sha>` | Every trunk build | No | Canonical build identity |
| `vX.Y.Z` | Release tag pushed | No | Release identity |
| `dev` | After successful Dev deploy | Yes (pointer) | Convenience only — MUST NOT be used in any deployment |
| `prd` | After successful PRD deploy | Yes (pointer) | Convenience only — MUST NOT be used in any deployment |
| `latest` | Never | — | Prohibited |

**Rule A-1:** Deployments MUST reference images by digest (`image: ghcr.io/<org>/<app>@sha256:…`).
**Rule A-2:** An image MUST NOT be rebuilt for promotion. The Dev-validated digest is the PRD digest. The PRD workflow fails closed if they differ.
**Rule A-3:** Images referenced by any Helm revision retained in PRD history MUST be exempt from registry garbage collection.

### 7.3 Retention

| Artifact | Retention |
|----------|-----------|
| Images referenced by a `vX.Y.Z` tag | 24 months |
| Untagged / superseded trunk builds | 30 days |
| Helm release history (PRD) | 20 revisions |
| Workflow run logs and artifacts | 400 days |
| Approval and audit records | 7 years (per DOC-POL-AUDIT-002) |

---

# Part B — Standard Operating Procedures

> Each procedure states: Trigger · Actor · Pre-conditions · Steps · Verification · Failure handling · Evidence · Expected duration.

## 8. OPS-01 — Pull Request Continuous Integration

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-01 |
| **Trigger** | `pull_request` opened / synchronised targeting `main`; `merge_group` |
| **Actor** | Automated (GitHub Actions) + Reviewer |
| **Frequency** | Every change, many times per day |
| **Expected duration** | ≤ 10 minutes (hard budget; exceeding it is a pipeline defect) |

### 8.1 Pre-conditions

1. Branch created from current `main`, named per TBD-2.
2. Commit messages follow Conventional Commits (§4.6).
3. Change is < 400 changed lines (TBD-4) or a decomposition rationale is in the PR body.
4. Incomplete behaviour is flag-guarded (OPS-13).

### 8.2 Quality Gates (all required, all blocking)

| # | Gate | Tool class | Failure action |
|---|------|-----------|----------------|
| G1 | Commit message / PR title lint | commitlint | Fix message |
| G2 | Format + static lint | language linter | Fix code |
| G3 | Unit tests | test runner | Fix code |
| G4 | Coverage ≥ 80% on changed lines | coverage tool | Add tests |
| G5 | Dependency vulnerability scan (High/Critical = fail) | SCA | Upgrade / documented exception |
| G6 | Static application security testing | SAST / CodeQL | Remediate |
| G7 | Secret scanning (incl. history of the branch) | secret scanner | Rotate + purge ⚠ |
| G8 | Container image build (no push) | Buildx | Fix Dockerfile |
| G9 | Image vulnerability scan (High/Critical = fail) | Trivy/Grype | Rebase on patched base image |
| G10 | `helm lint` + `helm template` for dev and prd overlays | Helm | Fix chart |
| G11 | Manifest policy check (limits, non-root, digest pin, probes present) | policy engine | Fix chart |
| G12 | ≥ 1 approving review from CODEOWNERS, author excluded | GitHub | Obtain review |

### 8.3 Steps

1. **Developer** — create branch and push:
   ```bash
   git switch main && git pull --ff-only
   git switch -c feat/PLT-482-retry-policy
   # implement change + tests (flag-guarded if incomplete)
   git commit -m "feat(api): add configurable retry policy"
   git push -u origin feat/PLT-482-retry-policy
   ```
2. **Developer** — open PR against `main`, complete the PR template (change summary, risk, rollback note, flag name, validation evidence).
3. **Automation** — CI executes gates G1–G11 (see Appendix C.1).
4. **Reviewer** — review within 4 business hours; assess correctness, security, observability, rollback safety, flag coverage.
5. **Developer** — address feedback with additional commits; do not force-push during active review.
6. **Developer** — enqueue in the **Merge Queue** (`gh pr merge --squash --auto`). The queue re-tests the change against the current trunk head.

### 8.4 Verification

- All required checks report success on the merge-queue head, not only on the branch head.
- PR shows squash-merge mode and auto-delete of source branch.

### 8.5 Failure Handling

| Failure | Action |
|---------|--------|
| Any gate fails | PR is blocked. Fix on the branch; never bypass. |
| Flaky test | Re-run **once**. If it fails again, treat as a real failure. Raise a flake ticket; quarantining requires Platform Lead approval and an owner + due date. |
| Merge queue rejects after trunk moved | Queue rebases and re-tests automatically; if it fails, the PR is dequeued and returned to the author. |
| G7 secret detected ⚠ | Immediately rotate the exposed credential (OPS-12), then purge from history. Rotation precedes cleanup. |

### 8.6 Evidence

PR record with check results, review approval, merge-queue run, squash commit SHA.

---

## 9. OPS-02 — Trunk Merge and Artifact Publication

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-02 |
| **Trigger** | `push` to `main` (result of a merge-queue merge) |
| **Actor** | Automated |
| **Expected duration** | ≤ 8 minutes |

### 9.1 Pre-conditions

1. Commit is on `main` and produced by the merge queue.
2. Trunk is green (§4.5).

### 9.2 Steps

1. Checkout the trunk commit at full depth (tags required for versioning).
2. Derive build metadata:
   - `SHORT_SHA=$(git rev-parse --short=12 HEAD)`
   - `IMAGE=ghcr.io/<org>/<app>`
   - `TAG=sha-${SHORT_SHA}`
3. Build the container image reproducibly (pinned base image by digest, `SOURCE_DATE_EPOCH` set, no `latest`).
4. Push to GHCR with tag `sha-<short-sha>`.
5. Capture the digest emitted by the push:
   ```bash
   DIGEST=$(docker buildx imagetools inspect "$IMAGE:$TAG" --format '{{.Manifest.Digest}}')
   ```
6. Generate and attach supply-chain metadata:
   - SBOM (SPDX or CycloneDX) attached as an attestation.
   - SLSA build provenance attestation (`actions/attest-build-provenance`).
   - Keyless signature (`cosign sign` with OIDC identity).
7. Scan the **pushed** image; fail the workflow on High/Critical with an available fix.
8. Publish `digest`, `tag`, `commit`, `run_id` as job outputs and as a workflow summary table.

### 9.3 Verification

```bash
crane digest ghcr.io/<org>/<app>:sha-<short-sha>            # digest resolves
cosign verify ghcr.io/<org>/<app>@sha256:<digest> \
  --certificate-identity-regexp "https://github.com/<org>/<app>/.github/workflows/.*" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/<org>/<app>@sha256:<digest> --owner <org>
```

### 9.4 Failure Handling

| Failure | Action |
|---------|--------|
| Build fails on trunk | Trunk is broken (§4.5). Author fixes within 15 min or reverts. |
| Registry push 403 | Verify job `permissions: packages: write` and package visibility/linkage to repo. |
| Registry 5xx / timeout | Workflow retries 3× with backoff; if still failing, check GHCR status and re-run the job. |
| Scan finds new Critical in an unchanged base image | Raise expedited PR bumping the base image digest; do not suppress. |

### 9.5 Evidence

Workflow run, image digest, SBOM, provenance attestation, signature, scan report.

---

## 10. OPS-03 — Dev Deployment

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-03 |
| **Trigger** | Successful completion of OPS-02 (same workflow, dependent job) |
| **Actor** | Automated (GitHub Environment `dev`, no approval) |
| **Expected duration** | ≤ 5 minutes |

### 10.1 Pre-conditions

1. Digest published and verified (OPS-02).
2. `dev` environment is not frozen (OPS-14).
3. Cluster reachable via OIDC federation.

### 10.2 Steps

1. Authenticate to the cluster with the `dev`-scoped federated identity.
2. Confirm namespace and quota headroom:
   ```bash
   kubectl get ns <app>-dev
   kubectl -n <app>-dev get resourcequota
   ```
3. Deploy with Helm, pinning by digest:
   ```bash
   helm upgrade --install <app> ./charts/<app> \
     --namespace <app>-dev \
     --values ./charts/<app>/values.yaml \
     --values ./charts/<app>/values-dev.yaml \
     --set image.repository=ghcr.io/<org>/<app> \
     --set image.digest=sha256:${DIGEST#sha256:} \
     --set-string podAnnotations."app\.kubernetes\.io/commit"=${GITHUB_SHA} \
     --set-string podAnnotations."app\.kubernetes\.io/run-id"=${GITHUB_RUN_ID} \
     --atomic \
     --wait \
     --timeout 5m \
     --history-max 5
   ```
   `--atomic` guarantees automatic rollback of a failed upgrade; the release never remains in a partially applied state.
4. Record the deployed revision:
   ```bash
   helm -n <app>-dev history <app> --max 1 -o json
   ```

### 10.3 Verification

```bash
kubectl -n <app>-dev rollout status deploy/<app> --timeout=300s
kubectl -n <app>-dev get pods -l app.kubernetes.io/name=<app> -o wide
kubectl -n <app>-dev get deploy <app> \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'   # MUST show @sha256:<digest>
```

### 10.4 Failure Handling

| Symptom | First action | Reference |
|---------|--------------|-----------|
| `--atomic` rolled the release back | Read `kubectl -n <app>-dev describe pod` and events | §24.2 |
| `ImagePullBackOff` | Verify digest exists and pull secret validity | §24.3 |
| `CrashLoopBackOff` | `kubectl logs --previous` | §24.4 |
| Readiness never true | Probe path/port/timeout mismatch | §24.5 |
| `another operation in progress` | Release stuck in pending state | §24.8 |

### 10.5 Evidence

Helm revision number, digest, rollout status, workflow summary.

---

## 11. OPS-04 — Dev Validation and Smoke Test

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-04 |
| **Trigger** | Successful OPS-03 |
| **Actor** | Automated, with Developer confirmation for functional acceptance |
| **Expected duration** | ≤ 5 minutes automated |

### 11.1 Automated Gates

| # | Check | Pass criterion |
|---|-------|----------------|
| V1 | Rollout complete | All replicas updated, available, `Progressing=True/NewReplicaSetAvailable` |
| V2 | Liveness | All pods `Ready`, restart count stable for 60 s |
| V3 | Health endpoint | `GET /healthz` → 200 |
| V4 | Readiness endpoint | `GET /readyz` → 200 |
| V5 | Version endpoint | `GET /version` returns the expected commit SHA |
| V6 | Smoke suite | 100% of `tests/smoke` pass against the Dev URL |
| V7 | Error budget check | HTTP 5xx rate < 1% over the 5-minute post-deploy window |
| V8 | Log sanity | No `FATAL`/`panic` entries since rollout start |

### 11.2 Steps

```bash
# V1–V2
kubectl -n <app>-dev rollout status deploy/<app> --timeout=300s
kubectl -n <app>-dev get pods -l app.kubernetes.io/name=<app> \
  -o custom-columns=NAME:.metadata.name,READY:.status.containerStatuses[0].ready,RESTARTS:.status.containerStatuses[0].restartCount

# V3–V5 (in-cluster, avoids ingress dependency)
kubectl -n <app>-dev run smoke-$RANDOM --rm -i --restart=Never --image=curlimages/curl:8.8.0 -- \
  sh -c 'curl -fsS http://<app>.<app>-dev.svc.cluster.local:8080/healthz &&
         curl -fsS http://<app>.<app>-dev.svc.cluster.local:8080/readyz &&
         curl -fsS http://<app>.<app>-dev.svc.cluster.local:8080/version'

# V6
npm run test:smoke -- --base-url "https://<app>-dev.<domain>"

# V8
kubectl -n <app>-dev logs -l app.kubernetes.io/name=<app> --since=10m --tail=-1 \
  | grep -Ei 'fatal|panic|unhandled' || echo "clean"
```

### 11.3 Manual Acceptance (for user-visible change)

The change author confirms in the PR/ticket: feature behaves as specified behind its flag, no regression in adjacent flows, telemetry emitted. Record a one-line confirmation with timestamp.

### 11.4 Failure Handling

- Any V-gate fails ⇒ the trunk commit is **not eligible for release** (§12.1). Trunk is treated as broken (§4.5).
- Remediate by fix-forward PR, or `git revert` the offending commit if a fix is not immediate.
- Do not tag a release from a commit whose Dev validation failed. The PRD workflow fails closed on this check.

### 11.5 Evidence

Validation job log, smoke report artifact, `/version` output, manual acceptance note.

---

## 12. OPS-05 — Release Candidate Selection and Tagging

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-05 |
| **Trigger** | Business decision to release; trunk commit validated in Dev |
| **Actor** | Release Manager |
| **Expected duration** | ≤ 5 minutes |

### 12.1 Pre-conditions (all mandatory)

1. Candidate commit is on `main`.
2. OPS-02, OPS-03 and OPS-04 all succeeded for that exact commit.
3. The image digest for that commit exists in GHCR and is signed.
4. No active deployment freeze (OPS-14) or an approved exception exists.
5. Candidate commit has been running in Dev for ≥ 30 minutes (soak), or an expedited justification is recorded (OPS-10).

### 12.2 Determine the Version

Semantic version derived from Conventional Commits since the previous tag:

```bash
git fetch --tags --force
PREV=$(git describe --tags --abbrev=0 --match 'v*')
git log --oneline "$PREV..HEAD"        # review scope
# feat!/BREAKING ⇒ major | feat ⇒ minor | fix/perf ⇒ patch
```

### 12.3 Steps

```bash
git switch main && git pull --ff-only
COMMIT=$(git rev-parse HEAD)

# 1. Confirm Dev validation for this exact commit
gh run list --branch main --commit "$COMMIT" --workflow cd-trunk-dev.yml --limit 1

# 2. Create an annotated, signed tag on the validated commit
git tag -s v1.8.0 "$COMMIT" -m "Release v1.8.0

Scope: PLT-482 retry policy, PLT-501 header validation
Image: ghcr.io/<org>/<app>@sha256:<digest>
Dev validated: run <run-id> at <timestamp>"

# 3. Push the tag — this triggers the PRD workflow up to the approval gate
git push origin v1.8.0
```

> ⚠ Tags are immutable. A tag MUST NOT be moved or deleted. A mistake is corrected by cutting the next patch version.

### 12.4 Verification

```bash
git tag -v v1.8.0                                   # signature valid, points at expected commit
gh run list --workflow cd-release-prd.yml --limit 1 # workflow queued, paused at approval
```

### 12.5 Release Notes

Auto-generated from Conventional Commits between tags, then reviewed by the Release Manager for: customer-visible changes, flags enabled by this release, migration/compatibility notes, and rollback constraints.

### 12.6 Evidence

Signed tag, release notes, link to the Dev validation run.

---

## 13. OPS-06 — Production Approval Gate

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-06 |
| **Trigger** | PRD workflow reaches the `prd` environment |
| **Actor** | Production Approver (not the change author) |
| **Expected duration** | ≤ 30 minutes during business hours |

### 13.1 Pre-flight Evidence Presented to the Approver

The workflow publishes an approval summary before pausing. The approver MUST confirm each line:

| # | Item | Source |
|---|------|--------|
| A1 | Release tag and commit SHA | Workflow summary |
| A2 | Image digest, and proof it is byte-identical to the Dev-validated digest | Digest equality check |
| A3 | Signature + provenance verified | `cosign` / `gh attestation` step |
| A4 | Dev validation (OPS-04) passed for this commit | Linked run |
| A5 | Vulnerability scan: no unresolved High/Critical | Scan step |
| A6 | Helm diff between current PRD release and candidate reviewed | `helm diff upgrade` output |
| A7 | Change ticket approved; release window valid; no freeze | Ticket link |
| A8 | Rollback target identified (previous PRD revision + digest) | Workflow summary |
| A9 | Approver is not the author (SoD-2) | GitHub identity |

### 13.2 Steps

1. Approver opens the workflow run → `prd` environment → **Review deployments**.
2. Verify A1–A9. Inspect the Helm diff carefully: unexpected changes to replicas, resources, probes, secrets or ingress are grounds for rejection.
3. **Approve** with a comment referencing the change ticket, or **Reject** with the reason.

### 13.3 Rejection Criteria (non-exhaustive)

- Digest mismatch between Dev and PRD candidate — reject and raise an incident (indicates pipeline compromise or rebuild).
- Helm diff shows changes not described in the change ticket.
- Unresolved High/Critical vulnerability without a documented, time-bound exception.
- Approver is the author, or no second person is available — escalate, do not self-approve.
- Active freeze without an approved exception.

### 13.4 Evidence

GitHub Environment approval record (approver identity, timestamp, comment) — immutable and retained per §7.3.

---

## 14. OPS-07 — Production Deployment (Exact-Image Promotion)

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-07 |
| **Trigger** | Approval granted in OPS-06 |
| **Actor** | Automated, observed by Release Manager + Platform Engineer |
| **Expected duration** | ≤ 10 minutes |

### 14.1 Pre-conditions

1. OPS-06 approval recorded.
2. PRD cluster healthy; no active Sev-1/Sev-2 incident on this service.
3. Current PRD revision and digest captured as the rollback target.

### 14.2 Steps

1. **Capture rollback target** (executed by the workflow, printed to the summary):
   ```bash
   PREV_REV=$(helm -n <app>-prd history <app> -o json | jq -r 'map(select(.status=="deployed"))|last|.revision')
   PREV_IMG=$(kubectl -n <app>-prd get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].image}')
   echo "Rollback target: revision=$PREV_REV image=$PREV_IMG"
   ```
2. **Resolve the promotion digest from the release tag** — never rebuild:
   ```bash
   DIGEST=$(crane digest ghcr.io/<org>/<app>:sha-${SHORT_SHA})
   ```
3. **Fail-closed equality check** — the digest deployed to Dev MUST equal the digest to be deployed to PRD:
   ```bash
   test "$DIGEST" = "$DEV_VALIDATED_DIGEST" || { echo "::error::Digest mismatch — promotion aborted"; exit 1; }
   ```
4. **Verify provenance again at the point of use** (`cosign verify`, `gh attestation verify`).
5. **Render and review the diff** (archived as an artifact):
   ```bash
   helm diff upgrade <app> ./charts/<app> -n <app>-prd \
     -f ./charts/<app>/values.yaml -f ./charts/<app>/values-prd.yaml \
     --set image.digest="${DIGEST#sha256:}"
   ```
6. **Deploy** ⚠:
   ```bash
   helm upgrade --install <app> ./charts/<app> \
     --namespace <app>-prd \
     --values ./charts/<app>/values.yaml \
     --values ./charts/<app>/values-prd.yaml \
     --set image.repository=ghcr.io/<org>/<app> \
     --set image.digest=${DIGEST#sha256:} \
     --set-string podAnnotations."app\.kubernetes\.io/version"=${RELEASE_TAG} \
     --set-string podAnnotations."app\.kubernetes\.io/commit"=${GITHUB_SHA} \
     --atomic \
     --wait \
     --timeout 10m \
     --history-max 20
   ```
   Surge-only rolling update (`maxUnavailable: 0`) preserves capacity throughout. `--atomic` performs an automatic rollback if the rollout does not become healthy within the timeout.
7. Proceed to OPS-08 validation.

### 14.3 Verification

```bash
kubectl -n <app>-prd rollout status deploy/<app> --timeout=600s
kubectl -n <app>-prd get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
helm -n <app>-prd history <app> --max 3
```

The running image string MUST contain the approved digest, and MUST NOT contain a floating tag.

### 14.4 Failure Handling

| Failure | Action |
|---------|--------|
| Digest mismatch (step 3) | **Stop.** Do not override. Raise Sev-2 and investigate pipeline integrity. |
| Signature/provenance verification fails | **Stop.** Treat as potential supply-chain compromise; Sev-1. |
| `--atomic` auto-rollback fired | Service is on the previous revision. Confirm with OPS-08 checks, then triage per §24 and fix-forward (OPS-10). |
| Timeout without auto-rollback (e.g. `--wait` edge case) | Execute OPS-09 manual rollback immediately. |
| Partial rollout, some pods unhealthy | PDB + `maxUnavailable: 0` protects capacity; execute OPS-09 if error rate rises. |

### 14.5 Evidence

Approval record, digest equality proof, `helm diff` artifact, Helm revision, rollout status, deployment annotations.

---

## 15. OPS-08 — Production Validation

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-08 |
| **Trigger** | Completion of OPS-07 |
| **Actor** | Automated + On-Call Responder observation |
| **Expected duration** | 10 minutes automated + 30 minutes observation |

### 15.1 Gate Set

| Phase | Window | Check | Pass criterion | On failure |
|-------|--------|-------|----------------|------------|
| Immediate | 0–2 min | Rollout complete; all replicas Ready | `rollout status` returns success | OPS-09 |
| Immediate | 0–2 min | `/healthz`, `/readyz` 200 on every pod | 100% | OPS-09 |
| Immediate | 0–2 min | `/version` reports the released commit | Exact match | OPS-09 |
| Functional | 2–5 min | Read-only production smoke suite | 100% pass | OPS-09 |
| Stability | 5–15 min | HTTP 5xx rate | < 0.5% and not above pre-deploy baseline + 0.2pp | OPS-09 |
| Stability | 5–15 min | p95 latency | ≤ pre-deploy baseline × 1.2 | Assess; OPS-09 if sustained |
| Stability | 5–15 min | Pod restarts | 0 unexpected restarts | OPS-09 |
| Stability | 5–15 min | Saturation (CPU/memory) | < 80% of limits | Assess |
| Soak | 15–45 min | Alert silence | No new Sev-1/Sev-2 alerts | OPS-09 |
| Soak | 15–45 min | Business KPI (orders/logins/etc.) | Within normal band | Escalate to service owner |

### 15.2 Commands

```bash
kubectl -n <app>-prd rollout status deploy/<app> --timeout=600s
kubectl -n <app>-prd get pods -l app.kubernetes.io/name=<app> \
  -o custom-columns=NAME:.metadata.name,READY:.status.containerStatuses[0].ready,RESTARTS:.status.containerStatuses[0].restartCount,AGE:.metadata.creationTimestamp
kubectl -n <app>-prd get events --sort-by=.lastTimestamp | tail -30
npm run test:smoke -- --base-url "https://<app>.<domain>" --read-only
```

### 15.3 Release Closure

The release is **complete** only when: all gates in §15.1 pass, the change ticket is updated with the release tag and digest, and the release announcement is posted to the operations channel. Until then the release is **in progress** and the Release Manager remains on point.

### 15.4 Evidence

Validation logs, smoke report, dashboard screenshots or metric snapshots at T+15, release closure note.

---

## 16. OPS-09 — Rollback and Recovery

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-09 |
| **Trigger** | Failed OPS-08 gate, production incident, or on-call judgement |
| **Actor** | On-Call Responder / Platform Engineer |
| **Authority** | On-call may roll back **without prior approval**; notification is retrospective |
| **Target** | Rollback initiated ≤ 5 min from detection; service restored ≤ 15 min |

### 16.1 Decision Matrix

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Rollout never completed; `--atomic` already reverted | Verify health, then triage | Automatic recovery occurred |
| Error rate > 5%, or total outage | **Immediate rollback** | Containment first |
| Error rate 1–5% sustained > 5 min | **Rollback** | Exceeds error budget burn |
| Latency p95 > 2× baseline sustained > 10 min | Rollback | User-visible degradation |
| Single non-critical feature broken, flag-guarded | **Disable flag (OPS-13)** — no rollback | Faster, lower blast radius |
| Data-affecting defect | Rollback + engage data owner ⚠ | Rollback may not undo data effects |
| Defect with a trivial, tested fix and low impact | Fix-forward (OPS-10) | Rollback churn not justified |
| Cause unknown, impact material | Rollback | Never debug in a degraded production |

> **Flag-first rule:** if the faulty behaviour is behind a feature flag, disabling the flag is always attempted first — it is seconds, not minutes, and requires no deployment.

### 16.2 Method 1 — Helm Rollback (primary)

```bash
# 1. Identify revisions
helm -n <app>-prd history <app>

# 2. Roll back to the last known-good revision (N-1 unless otherwise determined) ⚠
helm -n <app>-prd rollback <app> <REVISION> --wait --timeout 10m

# 3. Verify
kubectl -n <app>-prd rollout status deploy/<app> --timeout=600s
kubectl -n <app>-prd get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

Preferred execution path is the **`rollback-prd.yml` workflow** (Appendix C.4), which performs the same action with an audit record and notification. Direct CLI is the fallback when GitHub Actions is unavailable.

### 16.3 Method 2 — Redeploy the Previous Digest

Use when Helm history is unusable (e.g. corrupted release secret).

```bash
helm upgrade --install <app> ./charts/<app> \
  --namespace <app>-prd \
  -f ./charts/<app>/values.yaml -f ./charts/<app>/values-prd.yaml \
  --set image.repository=ghcr.io/<org>/<app> \
  --set image.digest=<PREVIOUS_GOOD_DIGEST> \
  --atomic --wait --timeout 10m
```

### 16.4 Method 3 — Kubernetes Rollout Undo (last resort)

```bash
kubectl -n <app>-prd rollout undo deploy/<app>       # ⚠ desynchronises Helm state
```

> Method 3 leaves Helm's recorded state inconsistent with the cluster. It is permitted only to restore service when Helm is unavailable, and **MUST** be followed within 24 hours by a reconciling `helm upgrade` to the intended digest.

### 16.5 Post-Rollback Actions (mandatory, in order)

1. Confirm recovery against the OPS-08 immediate and stability gates.
2. Notify stakeholders: service restored, version now running, impact window.
3. Freeze further releases of this service until root cause is understood (OPS-14, service-scoped).
4. Preserve forensic evidence **before** pods are recycled:
   ```bash
   kubectl -n <app>-prd logs <pod> --previous > incident-<id>-pod.log
   kubectl -n <app>-prd describe pod <pod> > incident-<id>-describe.txt
   kubectl -n <app>-prd get events --sort-by=.lastTimestamp > incident-<id>-events.txt
   ```
5. Raise the incident record (§25) and schedule a blameless post-incident review within 5 business days.
6. Remediate via OPS-10 fix-forward. **Never re-release the identical failed digest.**

### 16.6 Rollback Constraints

| Constraint | Handling |
|------------|----------|
| Irreversible database migration | Rollback of code only; data remediation is a separate, owner-led action. Migrations MUST be backward-compatible (expand/contract) precisely so rollback stays safe. |
| Consumer already depends on new API field | Prefer fix-forward; rolling back may break downstream consumers. |
| Rollback target image garbage-collected | Prevented by §7.3 retention; if it occurs, rebuild from the tagged commit as an emergency exception (OPS-15) and record a defect against retention policy. |

---

## 17. OPS-10 — Hotfix (Fix-Forward on Trunk)

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-10 |
| **Trigger** | Production defect requiring a code change |
| **Actor** | Developer + Platform Engineer + Approver |
| **Target** | Merged to trunk ≤ 60 min, in PRD ≤ 90 min from decision |

> Under trunk-based development there is **no hotfix branch**. A hotfix is an ordinary, minimal PR to `main`, fast-tracked. This preserves a single linear history and guarantees the fix is present in all future releases.

### 17.1 Pre-conditions

1. Service has been contained (rollback or flag disable) where impact warranted.
2. Root cause identified and the fix is **minimal and targeted** — unrelated changes MUST NOT ride along.
3. Trunk is green. If trunk is red, fixing trunk comes first.

### 17.2 Steps

1. Create the branch from current `main`:
   ```bash
   git switch main && git pull --ff-only
   git switch -c fix/INC-1042-null-tenant-header
   ```
2. Implement the smallest correct fix **plus a regression test that fails without it**.
3. Open the PR, label `hotfix` and `priority:critical`, link the incident.
4. Full CI still runs (OPS-01). **Gates are never skipped.** Speed comes from prioritised review, not reduced verification.
5. Obtain expedited review (on-call reviewer rota; SLA 15 minutes).
6. Merge via the merge queue (squash).
7. OPS-02 → OPS-03 → OPS-04 execute normally. Dev soak may be shortened to the time required for smoke tests to pass, with the reduction recorded in the incident.
8. Cut a **patch** release tag (OPS-05), e.g. `v1.8.1`.
9. OPS-06 approval: incident commander may approve if not the author; state "hotfix for INC-####" in the approval comment.
10. OPS-07 deploy, OPS-08 validate with heightened observation (60-minute soak).

### 17.3 If the Fix Must Bypass Normal Flow

Only when the pipeline itself is unavailable — see OPS-15 Break-Glass. Bypassing CI for speed alone is prohibited.

### 17.4 Evidence

Incident link, PR, CI results, tag, approval, validation, post-incident review record.

---

## 18. OPS-11 — Configuration-Only Change

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-11 |
| **Trigger** | Change to replicas, resources, HPA bounds, probes, env vars, ingress or flag defaults |
| **Actor** | Platform Engineer / Developer |

### 18.1 Principle

Configuration is code. A configuration change follows the **identical** path: PR to trunk → CI → Dev → tag → approval → PRD. Editing live objects with `kubectl edit`, `kubectl scale` or `kubectl patch` is **prohibited** outside a declared incident, because the next Helm upgrade silently reverts it and the audit trail is lost.

### 18.2 Steps

1. Edit `charts/<app>/values-dev.yaml` and/or `values-prd.yaml` on a short-lived branch.
2. Include the rendered impact in the PR:
   ```bash
   helm template <app> ./charts/<app> -f charts/<app>/values.yaml -f charts/<app>/values-prd.yaml > /tmp/after.yaml
   git stash && helm template <app> ./charts/<app> -f charts/<app>/values.yaml -f charts/<app>/values-prd.yaml > /tmp/before.yaml && git stash pop
   diff -u /tmp/before.yaml /tmp/after.yaml
   ```
3. Merge, validate in Dev, tag (usually a `chore`/`fix` patch release), approve, deploy.

### 18.3 Emergency Capacity Change

During a declared incident, an on-call engineer MAY scale imperatively:

```bash
kubectl -n <app>-prd scale deploy/<app> --replicas=8    # ⚠ incident only
```

This MUST be reconciled by a PR updating `values-prd.yaml` **within 24 hours**, and recorded in the incident timeline.

---

## 19. OPS-12 — Secret Management and Rotation

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-12 |
| **Actor** | Platform Engineer (with Security for production credentials) |

### 19.1 Rules

| # | Rule |
|---|------|
| S1 | Secrets MUST NOT be committed to Git in any form, including base64-encoded Kubernetes Secret manifests. |
| S2 | Application secrets are delivered to the cluster by the external secret manager (External Secrets Operator / CSI driver) and referenced by the chart; they are never rendered by Helm values. |
| S3 | Pipeline secrets live in GitHub **Environment** secrets (`dev`, `prd`), never repository-wide, so environment protection rules apply. |
| S4 | Cluster and cloud access uses OIDC federation with short-lived tokens; static credentials are prohibited. |
| S5 | Secrets are masked in logs; workflows MUST NOT `echo` secret values or write them to artifacts. |
| S6 | Every secret has a named owner and a rotation period (≤ 90 days standard, ≤ 365 days for signing keys with documented compensating controls). |
| S7 | A leaked or suspected-leaked secret is **rotated first**, investigated second. |

### 19.2 Routine Rotation

1. Generate the new credential at the source system; keep the old one valid (dual-validity window).
2. Update the value in the secret manager (new version).
3. Trigger propagation and restart consumers:
   ```bash
   kubectl -n <app>-prd annotate externalsecret <app>-secrets force-sync="$(date +%s)" --overwrite
   kubectl -n <app>-prd rollout restart deploy/<app>
   kubectl -n <app>-prd rollout status deploy/<app> --timeout=600s
   ```
4. Validate with OPS-08 immediate gates.
5. Revoke the old credential at the source once traffic is confirmed healthy.
6. Record rotation date, operator and next due date in the secret register.

### 19.3 Emergency Revocation (suspected compromise) ⚠

1. Revoke the compromised credential immediately at the source — accept the service impact.
2. Issue a replacement and apply §19.2 steps 2–4 on an expedited basis.
3. Raise a Sev-1/Sev-2 security incident; engage Security.
4. Audit access logs for the exposure window.
5. If exposure occurred via Git, purge history **after** rotation, and force cache invalidation of forks/mirrors.

### 19.4 Verification That No Secret Is Exposed

```bash
kubectl -n <app>-prd get deploy <app> -o yaml | grep -Ei 'password|token|secret|key' # expect only secretKeyRef
gh secret list --env prd
```

---

## 20. OPS-13 — Feature Flag Operations

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-13 |
| **Actor** | Developer / Release Manager / On-Call |

Feature flags are what make trunk-based development safe: they decouple **deploy** (artifact reaches production) from **release** (behaviour reaches users).

### 20.1 Rules

| # | Rule |
|---|------|
| F1 | Any change that cannot be completed within one short-lived branch MUST be merged dark behind a flag. |
| F2 | Flags default to **off** in PRD and are enabled deliberately after deployment. |
| F3 | Every flag has an owner, a purpose, a creation date and a planned removal date (≤ 90 days for release flags). |
| F4 | Code MUST behave correctly with the flag both on and off; both paths are covered by tests. |
| F5 | Stale flags (past removal date or fully rolled out) MUST be removed by a cleanup PR. Flag debt is reviewed monthly. |
| F6 | Kill-switch flags for risky subsystems MUST be togglable without deployment. |

### 20.2 Progressive Enablement

| Stage | Audience | Dwell | Exit criteria |
|-------|----------|-------|---------------|
| 1 | Internal users only | ≥ 1 h | No errors attributable to the flag |
| 2 | 5% of traffic | ≥ 2 h | Error rate and latency within baseline |
| 3 | 25% | ≥ 4 h | KPIs neutral or positive |
| 4 | 100% | ≥ 24 h | Stable |
| 5 | Remove flag from code | — | Cleanup PR merged |

### 20.3 Emergency Disable

Disabling a flag is the **first** containment action for a flag-guarded defect (§16.1). Record the action, time and reason in the incident timeline; no approval is required from on-call.

---

## 21. OPS-14 — Deployment Freeze and Release Windows

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-14 |
| **Actor** | Release Manager / Platform Lead |

### 21.1 Standard Windows

| Window | Policy |
|--------|--------|
| Business hours, Mon–Thu 09:00–16:00 local | **Preferred.** Full support available. |
| Friday after 12:00 | Discouraged; requires Platform Lead sign-off. |
| Weekends / public holidays | Hotfix and incident remediation only. |
| Declared freeze periods (peak trading, audit, major event) | Only Sev-1/Sev-2 remediation, with named exception approval. |

Dev deployment is **never** frozen — trunk must keep flowing. Freezes apply to PRD promotion only.

### 21.2 Enacting a Freeze

1. Announce scope, reason, start/end in the operations channel and change calendar.
2. Add required reviewers / disable the `prd` environment deployment branch policy, or set the repository variable `RELEASE_FREEZE=true`, which the PRD workflow checks and fails closed on.
3. Exceptions require: incident reference or business justification, Platform Lead approval, and post-freeze review.

### 21.3 Lifting a Freeze

Set `RELEASE_FREEZE=false`, announce, and process queued releases oldest-first, validating each fully before starting the next.

---

## 22. OPS-15 — Break-Glass Emergency Deployment

| Field | Value |
|-------|-------|
| **Procedure ID** | OPS-15 |
| **Actor** | On-Call Responder + Platform Lead (dual authorisation) |
| **Use only when** | GitHub Actions or the normal pipeline is unavailable **and** production is materially impaired |

> ⚠ Break-glass bypasses automated controls. It is an exceptional, fully audited action. Convenience or schedule pressure are **not** valid reasons.

### 22.1 Authorisation

Requires two people: the On-Call Responder executing, and the Platform Lead (or delegate) authorising. Both identities are recorded in the incident.

### 22.2 Procedure

1. Declare the incident and state that break-glass is being invoked, with reason.
2. Activate the time-boxed break-glass role (60-minute TTL, auto-expiring):
   ```bash
   # Elevation is requested through the access broker; it emits an audit event.
   request-access --role prd-breakglass --ttl 60m --justification "INC-1042 pipeline outage"
   ```
3. Execute the minimum necessary action, preferring reversal over novel change:
   ```bash
   helm -n <app>-prd history <app>
   helm -n <app>-prd rollback <app> <REVISION> --wait --timeout 10m    # ⚠
   ```
4. Verify with OPS-08 immediate gates.
5. Capture the full terminal transcript and attach it to the incident.
6. Confirm role expiry:
   ```bash
   kubectl auth can-i update deploy -n <app>-prd     # expect "no" after TTL
   ```

### 22.3 Mandatory Follow-Up (within 1 business day)

1. Reconcile Git and Helm with the actual cluster state — the repository MUST again be the source of truth.
2. Post-incident review including: why the pipeline was unavailable, what manual action was taken, and what will prevent recurrence.
3. Security review of the elevated-access audit log.

---

# Part C — Operations

## 23. Monitoring, Alerting and Service Levels

### 23.1 Golden Signals

| Signal | Metric | Dev threshold | PRD threshold |
|--------|--------|---------------|---------------|
| Latency | p95 request duration | informational | ≤ 300 ms (alert at > 500 ms for 5 min) |
| Traffic | requests/sec | informational | Drop > 50% vs. 7-day same-hour baseline = alert |
| Errors | HTTP 5xx ratio | informational | < 0.5% (alert at > 1% for 5 min) |
| Saturation | CPU/memory vs. limits | informational | < 80% (alert at > 85% for 10 min) |

### 23.2 Deployment-Specific Alerts

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| `DeploymentRolloutStuck` | `progressing` false > 10 min | Sev-2 | OPS-09 assessment |
| `PodCrashLooping` | restarts > 3 in 15 min | Sev-2 | §24.4 |
| `ImagePullFailure` | `ImagePullBackOff` > 5 min | Sev-2 | §24.3 |
| `ReplicasBelowPDB` | available < `minAvailable` | Sev-1 | Immediate response |
| `PostDeployErrorSpike` | 5xx > 1% within 15 min of a rollout | Sev-1 | Rollback (OPS-09) |
| `HPAMaxed` | at `maxReplicas` > 15 min | Sev-3 | Capacity review |
| `PipelineFailureOnTrunk` | OPS-02/03/04 failed on `main` | Sev-3 (engineering) | §4.5 |
| `ReleaseApprovalPending` | gate waiting > 24 h | Sev-4 | Release Manager chases |
| `CertificateExpiringSoon` | < 21 days | Sev-3 | Renewal procedure |

### 23.3 Service Level Objectives

| SLO | Target | Measurement window |
|-----|--------|--------------------|
| Availability (successful requests) | 99.9% | 30-day rolling |
| Latency: p95 | ≤ 300 ms | 30-day rolling |
| Deployment success rate (no rollback) | ≥ 95% | 30-day rolling |
| Time to restore service after failed release | ≤ 15 min | per incident |

Error-budget policy: when 50% of the monthly budget is consumed, new feature releases require Platform Lead sign-off; at 100%, only reliability work and hotfixes are released until the budget recovers.

### 23.4 Observability Requirements on the Application

- Structured JSON logs including `commit_sha`, `release_tag`, `trace_id`, `tenant_id`.
- `/healthz` (liveness: process alive), `/readyz` (readiness: dependencies usable), `/version` (commit, tag, build time) — `/readyz` MUST fail when a hard dependency is down so traffic is withdrawn.
- RED metrics exposed for scraping; deployment annotations emitted as metric labels so dashboards can overlay release markers.

---

## 24. Troubleshooting Guide

### 24.1 First-Response Triage (any deployment problem)

```bash
NS=<app>-prd      # or <app>-dev
kubectl -n $NS get pods -l app.kubernetes.io/name=<app> -o wide
kubectl -n $NS get events --sort-by=.lastTimestamp | tail -40
kubectl -n $NS describe deploy <app> | sed -n '/Conditions/,/Events/p'
helm -n $NS history <app> --max 5
kubectl -n $NS logs -l app.kubernetes.io/name=<app> --tail=200 --since=15m
```

Answer three questions in order: **(1)** What changed? **(2)** What is the blast radius? **(3)** What is the fastest safe containment?

### 24.2 Symptom Index

| Symptom | Likely cause | Go to |
|---------|--------------|-------|
| `ImagePullBackOff` / `ErrImagePull` | Digest wrong, registry auth, network | §24.3 |
| `CrashLoopBackOff` | App startup failure, bad config, missing secret | §24.4 |
| Pods `Running` but never `Ready` | Readiness probe or dependency | §24.5 |
| `OOMKilled` (exit 137) | Memory limit too low / leak | §24.6 |
| `Pending` pods | Insufficient resources, quota, affinity | §24.7 |
| Helm: `another operation in progress` | Interrupted prior operation | §24.8 |
| Helm: `has no deployed releases` | All prior revisions failed | §24.9 |
| Rollout stuck at partial replicas | Surge blocked by quota/PDB/node capacity | §24.10 |
| 5xx after deploy, pods healthy | Application/config/dependency defect | §24.11 |
| Workflow: OIDC/permission denied | Identity federation or job permissions | §24.12 |
| Slow or queued pipeline | Runner capacity, cache miss | §24.13 |

### 24.3 ImagePullBackOff / ErrImagePull

```bash
kubectl -n $NS describe pod <pod> | grep -A5 -i 'failed\|image'
kubectl -n $NS get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
crane manifest ghcr.io/<org>/<app>@sha256:<digest> >/dev/null && echo "digest exists"
kubectl -n $NS get secret ghcr-pull -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq '.auths|keys'
```

| Cause | Resolution |
|-------|------------|
| Digest does not exist (GC'd or typo) | Re-resolve digest from the release tag; if truly absent, treat as retention defect and use OPS-15 to restore service |
| Pull secret missing/expired in namespace | Recreate the secret; verify `imagePullSecrets` in the service account |
| Package not linked to repo / private visibility | Fix GHCR package settings and repository linkage |
| Registry outage | Check provider status; images already cached on nodes keep running |
| Node cannot reach `ghcr.io` | Check egress NetworkPolicy, proxy and DNS from the node |

### 24.4 CrashLoopBackOff

```bash
kubectl -n $NS logs <pod> --previous --tail=200
kubectl -n $NS describe pod <pod> | sed -n '/State/,/Events/p'   # note exit code
kubectl -n $NS get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}{"\n"}'
```

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 1 / 2 | Application error at startup | Read logs; usually config or dependency |
| 137 | OOMKilled / SIGKILL | §24.6 |
| 139 | Segfault | Runtime/native dependency defect — rollback |
| 143 | SIGTERM | Probe or scheduler terminated it; check probe timings |

Common root causes: missing environment variable or secret key, unreachable dependency at boot, failed migration on startup, incorrect file permissions under read-only root filesystem, insufficient `initialDelaySeconds` for a slow-starting JVM/runtime.

### 24.5 Ready Never True

```bash
kubectl -n $NS get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].readinessProbe}' | jq
kubectl -n $NS exec <pod> -- curl -fsS localhost:8080/readyz -v
```

Checks: probe path and port match the container; `initialDelaySeconds` ≥ real startup time (prefer a `startupProbe` for slow starts); `/readyz` is not gated on an optional dependency; the Service selector matches pod labels; the container listens on `0.0.0.0`, not `127.0.0.1`.

### 24.6 OOMKilled

```bash
kubectl -n $NS top pods -l app.kubernetes.io/name=<app>
kubectl -n $NS get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].resources}' | jq
```

Immediate: raise the memory limit via a values change (OPS-11); during an incident, scale horizontally for headroom. Follow-up: profile for leaks; for JVM/Node runtimes ensure heap settings are container-aware (`-XX:MaxRAMPercentage`, `--max-old-space-size`) and below the limit.

### 24.7 Pods Pending

```bash
kubectl -n $NS describe pod <pod> | sed -n '/Events/,$p'
kubectl -n $NS get resourcequota
kubectl get nodes -o custom-columns=NAME:.metadata.name,ALLOCATABLE_CPU:.status.allocatable.cpu,ALLOCATABLE_MEM:.status.allocatable.memory
```

Causes: namespace quota exhausted (raise quota via change, or reduce requests); no node with sufficient allocatable capacity (scale the node pool); node selector/affinity/taint mismatch; unbound PersistentVolumeClaim.

### 24.8 Helm: "another operation is in progress"

```bash
helm -n $NS list --all
helm -n $NS history <app>
```

If the release is stuck in `pending-install` / `pending-upgrade` and **no workflow is running**:

```bash
helm -n $NS rollback <app> <LAST_DEPLOYED_REVISION> --wait          # ⚠ preferred
# Only if rollback is impossible and the stuck revision is confirmed abandoned:
kubectl -n $NS delete secret -l owner=helm,name=<app>,version=<STUCK_REVISION>   # ⚠⚠
```

Never delete Helm release secrets while a deployment workflow is still executing — confirm in GitHub Actions first.

### 24.9 Helm: "has no deployed releases"

Occurs when the very first install failed and left only failed revisions.

```bash
helm -n $NS uninstall <app>        # ⚠ Dev only; in PRD escalate to Platform Lead
helm upgrade --install <app> ./charts/<app> -n $NS -f ... --atomic --wait
```

In PRD, prefer `helm rollback` to any successful prior revision; uninstall causes downtime and requires incident authorisation.

### 24.10 Rollout Stuck at Partial Replicas

```bash
kubectl -n $NS describe deploy <app> | grep -A10 Conditions
kubectl -n $NS get pdb
kubectl -n $NS get rs -l app.kubernetes.io/name=<app>
```

With `maxUnavailable: 0`, the new pod must become Ready before an old one is removed — so a failing readiness probe halts the rollout with **no capacity loss**. Diagnose the new pod (§24.5); if unrecoverable, OPS-09.

### 24.11 Errors After a Successful Rollout

1. Confirm the running digest matches the approved one (§14.3).
2. Compare error signatures before and after the release marker on dashboards.
3. Check dependencies (database, cache, downstream APIs) — the release may have exposed, not caused, the fault.
4. If a flag guards the change, disable it (OPS-13) and observe.
5. If errors persist and are release-correlated, roll back (OPS-09).

### 24.12 Workflow Authentication / Permission Failures

| Message | Cause | Fix |
|---------|-------|-----|
| `Error: could not fetch an ID token` | Missing `permissions: id-token: write` | Add to the job |
| `denied: permission_denied: write_package` | Missing `packages: write` or package not linked | Fix job permissions / package settings |
| `error: You must be logged in to the server (Unauthorized)` | OIDC trust `sub` mismatch | Verify the trust policy matches `repo:<org>/<app>:environment:<env>` |
| `Error: Resource not accessible by integration` | Default token scope too low | Elevate only the specific permission required |

### 24.13 Slow Pipeline

Check runner queue time vs. execution time; verify build-cache hit rate; parallelise independent gates; ensure dependency caching keys are stable; move long-running non-blocking scans to a nightly workflow while keeping blocking gates within the 10-minute budget.

---

## 25. Incident Management

### 25.1 Severity Definitions

| Severity | Definition | Response | Update cadence | Rollback authority |
|----------|------------|----------|----------------|--------------------|
| Sev-1 | Complete outage or critical data/security impact | Immediate, 24×7 | 30 min | On-call, immediate |
| Sev-2 | Major degradation; core function impaired | ≤ 30 min, 24×7 | 60 min | On-call, immediate |
| Sev-3 | Minor degradation; workaround exists | Next business day | Daily | Normal change process |
| Sev-4 | Cosmetic / no user impact | Backlog | — | Normal change process |

### 25.2 Response Flow

```
Detect (alert | validation gate | report)
   └▶ Declare severity + assign Incident Commander
        └▶ CONTAIN  ── flag off (OPS-13) → rollback (OPS-09) → scale/isolate
             └▶ COMMUNICATE (stakeholders, status page if customer-visible)
                  └▶ DIAGNOSE (preserve evidence first)
                       └▶ REMEDIATE (OPS-10 fix-forward)
                            └▶ VERIFY (OPS-08 gates)
                                 └▶ CLOSE + blameless post-incident review ≤ 5 business days
```

### 25.3 Incident Record Contents

Incident ID and severity; detection time, source and detector; affected service, version/digest, environment; user impact and duration; timeline of actions with timestamps and actors; root cause; containment and remediation actions; evidence links (logs, runs, approvals); corrective actions with owners and due dates.

### 25.4 Corrective Action Standard

Every Sev-1/Sev-2 must produce at least one **preventive** action (a new test, gate, alert or guardrail), not only a code fix. Actions are tracked to closure and reviewed monthly.

---

## 26. Audit, Evidence and Compliance

### 26.1 Evidence per Release (retained per §7.3)

| # | Evidence | System of record |
|---|----------|------------------|
| E1 | PR with review approval and CI results | GitHub PR |
| E2 | Merge-queue commit on trunk | Git history |
| E3 | Build run, image digest, SBOM, provenance, signature | Actions + GHCR |
| E4 | Vulnerability scan results | Actions artifacts |
| E5 | Dev deployment + validation results | Actions run |
| E6 | Signed release tag and release notes | Git / GitHub Releases |
| E7 | PRD approval: approver identity, timestamp, comment | GitHub Environments |
| E8 | Digest equality proof (Dev == PRD) | Actions log |
| E9 | `helm diff` for the PRD change | Actions artifact |
| E10 | PRD Helm revision and rollout status | Actions log + cluster |
| E11 | PRD validation results | Actions artifact |
| E12 | Rollback / break-glass records, if any | Incident record |

### 26.2 Control Assertions

| Control | Assertion | How it is evidenced |
|---------|-----------|---------------------|
| C1 Change control | No change reaches PRD without a reviewed PR | Branch protection + PR history |
| C2 Separation of duties | Author ≠ approver at both PR and deployment gates | PR reviews + environment approval records |
| C3 Artifact integrity | The artifact validated in Dev is exactly the artifact in PRD | Digest equality check (fail-closed) |
| C4 Provenance | Every production image is signed and attested to a trunk commit | cosign / SLSA attestation |
| C5 Least privilege | No standing human write access to PRD | RBAC review + break-glass logs |
| C6 Reversibility | Every release has a tested rollback path | Helm history + rollback drill records |
| C7 Traceability | Running pod → digest → commit → PR → ticket | Pod annotations + Git history |

### 26.3 Periodic Reviews

| Activity | Frequency | Owner |
|----------|-----------|-------|
| RBAC and environment-reviewer review | Quarterly | Platform Lead |
| Break-glass usage review | Monthly (and ≤ 1 business day per event) | Security |
| Secret rotation compliance | Monthly | Platform Engineering |
| Rollback drill in PRD-like environment | Quarterly | Platform Engineering |
| Runbook accuracy review | 6-monthly or on change | Platform Engineering |
| Branch-protection drift check | Automated weekly | Platform Engineering |
| Feature-flag debt review | Monthly | Application Team |

### 26.4 Traceability Query (pod → source)

```bash
kubectl -n <app>-prd get pod <pod> -o jsonpath='{.metadata.annotations}' | jq
# → app.kubernetes.io/commit, app.kubernetes.io/version, app.kubernetes.io/run-id
git log -1 <commit>
gh pr list --search "<commit>" --state merged
gh run view <run-id>
```

---

## 27. Delivery Performance Metrics

Trunk-based delivery is measured, not assumed. The following are reported monthly to the Platform Lead.

| Metric | Definition | Target | Source |
|--------|------------|--------|--------|
| Deployment frequency | PRD releases per week | ≥ 5 (daily capable) | Release tags |
| Lead time for change | First commit → running in PRD | < 24 h (p50) | PR + release data |
| Change failure rate | Releases causing rollback or hotfix | < 15% | Incident + rollback records |
| Time to restore service | Detection → service healthy | < 30 min (p50) | Incident records |
| Mean branch age at merge | Branch creation → merge | < 24 h | GitHub API |
| PR size (p90) | Lines changed per PR | < 400 | GitHub API |
| PR review latency (p50) | Open → first review | < 4 h | GitHub API |
| CI duration (p95) | PR gate wall-clock | < 10 min | Actions |
| Trunk red time | Minutes/month `main` is failing | < 60 | Actions |
| Rollback rate | Rollbacks / releases | < 5% | Rollback workflow runs |
| Flag debt | Flags older than 90 days | 0 | Flag register |

Trend, not absolute value, is the primary signal: a rising branch age or PR size predicts a future rise in change failure rate.

---

# Part D — Appendices

## Appendix A — Command Reference

### A.1 Daily Trunk Workflow

```bash
git switch main && git pull --ff-only
git switch -c feat/PLT-482-retry-policy
git commit -m "feat(api): add configurable retry policy"
git push -u origin feat/PLT-482-retry-policy
gh pr create --fill --base main
gh pr checks --watch
gh pr merge --squash --auto --delete-branch
```

### A.2 Release

```bash
git switch main && git pull --ff-only && git fetch --tags --force
git tag -s v1.8.0 -m "Release v1.8.0"
git push origin v1.8.0
gh run watch                       # approve at the prd gate in the UI
```

### A.3 Inspect Deployed State

```bash
NS=<app>-prd
helm -n $NS list
helm -n $NS history <app>
helm -n $NS get values <app>
kubectl -n $NS get deploy <app> -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
kubectl -n $NS get pods -l app.kubernetes.io/name=<app> -o wide
kubectl -n $NS get pod <pod> -o jsonpath='{.metadata.annotations}' | jq
```

### A.4 Rollback

```bash
gh workflow run rollback-prd.yml -f revision=<N> -f reason="INC-1042 5xx spike"
# fallback
helm -n <app>-prd history <app>
helm -n <app>-prd rollback <app> <N> --wait --timeout 10m    # ⚠
kubectl -n <app>-prd rollout status deploy/<app> --timeout=600s
```

### A.5 Diagnostics Bundle

```bash
NS=<app>-prd; ID=INC-1042; mkdir -p ./$ID
kubectl -n $NS get all -o yaml                 > ./$ID/all.yaml
kubectl -n $NS get events --sort-by=.lastTimestamp > ./$ID/events.txt
kubectl -n $NS describe deploy <app>           > ./$ID/deploy.txt
for p in $(kubectl -n $NS get pods -l app.kubernetes.io/name=<app> -o name); do
  kubectl -n $NS logs "$p" --tail=-1 --since=1h > "./$ID/${p##*/}.log" 2>/dev/null
  kubectl -n $NS logs "$p" --previous --tail=-1 > "./$ID/${p##*/}.prev.log" 2>/dev/null
  kubectl -n $NS describe "$p"                  > "./$ID/${p##*/}.describe.txt"
done
helm -n $NS history <app> -o yaml              > ./$ID/helm-history.yaml
tar czf "$ID-bundle.tgz" "./$ID"
```

### A.6 Supply-Chain Verification

```bash
crane digest ghcr.io/<org>/<app>:sha-<short-sha>
cosign verify ghcr.io/<org>/<app>@sha256:<digest> \
  --certificate-identity-regexp "https://github.com/<org>/<app>/.github/workflows/.*" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/<org>/<app>@sha256:<digest> --owner <org>
```

---

## Appendix B — Branch Protection and Repository Configuration

### B.1 Required `main` Protection (enforced, including administrators)

| Setting | Value |
|---------|-------|
| Require a pull request before merging | Enabled |
| Required approvals | 1 (2 for `charts/**` and `.github/workflows/**` via CODEOWNERS) |
| Dismiss stale approvals on new commits | Enabled |
| Require review from Code Owners | Enabled |
| Require approval of the most recent push | Enabled (blocks self-approval of own push) |
| Require status checks to pass | Enabled — `lint`, `unit-test`, `sast`, `sca`, `build-image`, `image-scan`, `helm-lint`, `policy-check` |
| Require branches to be up to date | Enabled (satisfied by merge queue) |
| Require merge queue | Enabled |
| Require conversation resolution | Enabled |
| Require signed commits | Enabled |
| Require linear history | Enabled (squash-merge only) |
| Allow force pushes | Disabled |
| Allow deletions | Disabled |
| Enforce for administrators / no bypass list | Enabled |

Repository merge settings: **squash merge only**; merge commits and rebase merges disabled; auto-delete head branches enabled; default squash commit message = PR title + description.

Tag protection: pattern `v*` — only the Release Manager team may create; tags are immutable and may not be deleted.

### B.2 Apply via CLI

```bash
gh api -X PUT repos/<org>/<app>/branches/main/protection \
  --input docs/reference/branch-protection.json

gh api -X PATCH repos/<org>/<app> \
  -f allow_squash_merge=true -F allow_merge_commit=false \
  -F allow_rebase_merge=false -F delete_branch_on_merge=true
```

### B.3 GitHub Environments

| Environment | Reviewers | Wait timer | Deployment branch/tag policy | Secrets |
|-------------|-----------|-----------|------------------------------|---------|
| `dev` | none | 0 | `main` only | Dev OIDC config |
| `prd` | `production-approvers` team (1 required) | 0 | Tags matching `v*` only | PRD OIDC config |

`prd` MUST additionally enforce "prevent self-review" by ensuring the approvers team excludes the deploying author; where the platform cannot enforce this technically, SoD-2 is an attested manual control verified in the quarterly review.

### B.4 CODEOWNERS (reference)

```
*                       @<org>/app-team
/charts/                @<org>/platform-engineering
/.github/workflows/     @<org>/platform-engineering
/docs/DOC-RUNBOOK-001*  @<org>/platform-engineering
```

---

## Appendix C — Reference Workflow Implementations

Working reference implementations are stored alongside this runbook:

| File | Procedure |
|------|-----------|
| `docs/reference/workflows/ci-pull-request.yml` | OPS-01 |
| `docs/reference/workflows/cd-trunk-dev.yml` | OPS-02, OPS-03, OPS-04 |
| `docs/reference/workflows/cd-release-prd.yml` | OPS-05 trigger, OPS-06, OPS-07, OPS-08 |
| `docs/reference/workflows/rollback-prd.yml` | OPS-09 |
| `docs/reference/branch-protection.json` | Appendix B |

They are held under `docs/reference/` so that they are reviewable as documentation; to activate them, copy into `.github/workflows/` and substitute `<org>`, `<app>` and cluster identity values.

Key invariants that MUST be preserved in any adaptation:

1. Image is built **once** on trunk and referenced by digest thereafter.
2. The PRD job compares the Dev-validated digest with the promotion digest and **fails closed** on mismatch.
3. The PRD job runs in the `prd` GitHub Environment so the approval gate applies.
4. `--atomic --wait` on every `helm upgrade`.
5. Job-level `permissions` are minimal and explicit.
6. The rollback workflow is independently runnable without a new build.

---

## Appendix D — Operational Checklists

Printable checklists: `docs/checklists/`.

### D.1 Pre-Release (Release Manager)

- [ ] Candidate commit is on `main` and CI is green
- [ ] OPS-03 Dev deployment succeeded for this exact commit
- [ ] OPS-04 validation passed; soak ≥ 30 min (or expedited justification recorded)
- [ ] Image digest exists, signed and attested
- [ ] No unresolved High/Critical vulnerabilities
- [ ] Change ticket approved and linked
- [ ] Release window valid; no active freeze
- [ ] Release notes reviewed
- [ ] Feature flags for this release default to **off**
- [ ] Rollback target (revision + digest) recorded
- [ ] Approver identified and available (non-author)
- [ ] On-call notified of the release window

### D.2 Production Approval (Approver)

- [ ] I am not the author of this change (SoD-2)
- [ ] Release tag and commit SHA match the change ticket
- [ ] Digest equality (Dev == PRD) verified in the run summary
- [ ] Signature and provenance verified
- [ ] `helm diff` reviewed — no unexpected changes
- [ ] Dev validation evidence reviewed
- [ ] Rollback target recorded
- [ ] Approval comment references the change ticket

### D.3 Post-Deployment (Release Manager / On-Call)

- [ ] Rollout completed; all replicas Ready
- [ ] `/healthz`, `/readyz`, `/version` correct
- [ ] Smoke suite passed
- [ ] Error rate and latency within thresholds at T+15
- [ ] No unexpected pod restarts
- [ ] No new Sev-1/Sev-2 alerts at T+45
- [ ] Change ticket updated with tag, digest and revision
- [ ] Release announced; evidence archived

### D.4 Rollback (On-Call)

- [ ] Decision recorded against the §16.1 matrix
- [ ] Flag-disable considered first
- [ ] Forensic evidence captured **before** pods recycled
- [ ] Rollback executed (workflow preferred)
- [ ] OPS-08 immediate gates re-verified
- [ ] Stakeholders notified
- [ ] Service-scoped release freeze applied
- [ ] Incident raised; post-incident review scheduled
- [ ] Fix-forward (OPS-10) planned with an owner

---

## Appendix E — RACI Matrix

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

| Activity | Developer | Reviewer | Release Mgr | Approver | Platform Eng | On-Call | Security |
|----------|:---------:|:--------:|:-----------:|:--------:|:------------:|:-------:|:--------:|
| OPS-01 PR CI | R | R | I | — | A | — | C |
| OPS-02 Build & publish | C | — | I | — | A/R | — | C |
| OPS-03 Dev deploy | I | — | I | — | A/R | — | — |
| OPS-04 Dev validation | R | — | C | — | A | — | — |
| OPS-05 Release tag | C | — | A/R | I | C | I | — |
| OPS-06 PRD approval | I | — | C | A/R | C | I | — |
| OPS-07 PRD deploy | I | — | C | I | A/R | I | — |
| OPS-08 PRD validation | C | — | A/R | I | R | C | — |
| OPS-09 Rollback | I | — | C | I | R | A/R | I |
| OPS-10 Hotfix | R | R | C | A | C | C | I |
| OPS-11 Config change | R | R | C | A | R | I | — |
| OPS-12 Secrets | C | — | I | I | A/R | I | A |
| OPS-13 Feature flags | A/R | C | C | I | I | R | — |
| OPS-14 Freeze | I | — | A/R | C | C | I | — |
| OPS-15 Break-glass | I | — | I | I | A | R | C |
| Post-incident review | R | C | C | C | A/R | R | C |

---

## Appendix F — Glossary

| Term | Definition |
|------|------------|
| Trunk | The single long-lived branch, `main`, always in a releasable state |
| Trunk-Based Development | Practice where all developers integrate into trunk at least daily via short-lived branches |
| Short-lived branch | A change branch living ≤ 48 hours before merge |
| Merge queue | GitHub mechanism that re-tests a PR against the current trunk head before merging |
| Digest | Content-addressable image identifier (`sha256:…`); immutable and authoritative |
| Exact-image promotion | Deploying to PRD the byte-identical image validated in Dev, without rebuild |
| Feature flag | Runtime switch decoupling deployment from user-visible release |
| Dark launch | Merging and deploying code that is inert until its flag is enabled |
| Fix-forward | Remediating a defect with a new commit on trunk rather than a maintenance branch |
| `--atomic` | Helm flag that automatically rolls back a failed upgrade |
| Gate | A blocking automated or human control that must pass before progression |
| SoD | Separation of Duties |
| SBOM | Software Bill of Materials |
| SLSA provenance | Signed attestation of how and from what source an artifact was built |
| Break-glass | Audited emergency access bypassing normal controls |
| Error budget | Allowed unreliability implied by an SLO |
| RC | Release candidate: a validated trunk commit eligible for tagging |
| DORA metrics | Deployment frequency, lead time, change failure rate, time to restore |

---

## Appendix G — Document History and Approval

### G.1 Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 25-Sep-2026 | Platform Engineering | Initial runbook, branch-per-environment model |
| 2.0 | 28-Sep-2026 | Platform Engineering | Rewritten for trunk-based development: single trunk, merge queue, tag-based release, feature flags, fix-forward, digest-pinned exact-image promotion, expanded troubleshooting, supply-chain verification, DORA metrics |

### G.2 Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Platform Engineering Lead | | | |
| Application Owner | | | |
| Security Representative | | | |
| Operations Manager | | | |

### G.3 Related Documents

| ID | Title |
|----|-------|
| DOC-HLDD-001 | CICD Dev-PRD Delivery Platform — High-Level Design |
| DOC-RUNBOOK-010 | Kubernetes Cluster Operations |
| DOC-RUNBOOK-011 | Network, Ingress and Certificate Operations |
| DOC-RUNBOOK-020 | Database Migration Procedures |
| DOC-DRP-001 | Disaster Recovery Plan |
| DOC-POL-AUDIT-002 | Audit Evidence Retention Policy |

### G.4 Maintenance

This runbook is version-controlled in `<org>/<app>` at `docs/DOC-RUNBOOK-001-production-operations-runbook.md`. Changes follow the same trunk-based process as code: short-lived branch → PR → Platform Engineering review → merge to `main`. Any procedure found inaccurate during an incident MUST be corrected within 5 business days of the post-incident review.

**— End of Document —**
