# CICD Dev-PRD Delivery Platform

Trunk-based continuous delivery from a single `main` branch to Kubernetes Dev and Production
namespaces, with immutable digest-pinned artifacts and an explicit production approval gate.

```
short-lived branch → PR (CI gate) → merge queue → main → build once (digest)
     → Dev deploy + validate → signed tag vX.Y.Z → approval gate → PRD (same digest) → validate
```

## Documentation

| Document | Description |
|----------|-------------|
| [Production Operations Runbook (DOC-RUNBOOK-001 v2.0)](./docs/DOC-RUNBOOK-001-production-operations-runbook.md) | Authoritative operational procedures OPS-01 … OPS-15, troubleshooting, audit |
| [Documentation index](./docs/README.md) | All documents and reference artifacts |
| [Release checklists](./docs/checklists/release-checklists.md) | Printable pre-release, approval, post-deploy, rollback checklists |
| [Reference workflows](./docs/reference/workflows/) | Runnable GitHub Actions implementations of the runbook procedures |

## Ground Rules

1. `main` is the only long-lived branch and is always releasable.
2. Change branches live ≤ 48 hours; merge by squash through the merge queue.
3. Unfinished work ships dark behind a feature flag — never held on a branch.
4. An image is built once and promoted to production **by digest**, never rebuilt.
5. Production requires approval from someone other than the change author.
6. Fix-forward is the default remediation; rollback is the containment action.
