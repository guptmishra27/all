# Session 4 — Limitations, Responsible AI, and Secure AI

**Exam domains:** 3. Techniques to improve model output (objective 3.1) + 4. Business
strategies (objectives 4.2 and 4.3)
**Goal of this session:** recognise a limitation from a scenario, name the right mitigation,
and pick the right responsible/security control from Google's toolset. This is where
*scenario* questions concentrate — leaders are expected to know what to do, not just what
things are called.

---

## 1. Foundation model limitations (objective 3.1)

| Limitation | Plain-language explanation | How it shows up in a business scenario |
| --- | --- | --- |
| **Data dependency** | Model quality depends heavily on the data it learned from. Biased, sparse, or unrepresentative data produces biased, sparse answers | "Our model performs poorly for customers in one region/language/segment" |
| **Knowledge cutoff** | Models are trained up to a cutoff date, so they lack knowledge of anything after it | "It doesn't know about our new product/regulation/price change" |
| **Hallucination** | The model produces output that isn't accurate or isn't based on real information — confidently | "It invented a policy clause / a citation / a statistic" |
| **Bias** | Models learn from datasets that contain societal and historical bias; subtle bias can be **amplified** in outputs | "Screening summaries skew unfavourably by gender or postcode" |
| **Fairness** | Assessing whether outcomes are equitable across groups is a core responsibility, not a nice-to-have | "Legal asks how we demonstrate non-discrimination" |
| **Edge cases** | Rare, atypical inputs expose weaknesses and produce unexpected results | "It works in demos but fails on unusual but real customer situations" |

**Related constraints worth naming in answers:** context window limits, cost and latency at
scale, token limits, and the fact that models are **non-deterministic** — the same prompt can
produce different outputs.

### 1.1 Google Cloud–recommended practices to address limitations

| Mitigation | Addresses | Notes |
| --- | --- | --- |
| **Prompt engineering** | Format, tone, ambiguity, some reliability issues | Cheapest first move; no model change |
| **Grounding** | Hallucination, knowledge cutoff, traceability | Anchors answers to verifiable sources |
| **RAG** | Hallucination, freshness, private knowledge, citations, access control | Retrieval + augmentation + generation (+ optional iteration) |
| **Fine-tuning** | Style, format, domain conventions, narrow task accuracy | Changes *behaviour*, not factual freshness; needs data, skill, and a retraining plan |
| **Human in the loop (HITL)** | High-stakes accuracy, bias catches, accountability | Human input and feedback integrated directly into ML workflows |
| **Safety settings & filters** | Harmful or inappropriate content | Applied to output; a governance decision |
| **Evaluation and monitoring** | Drift, regressions, unknown failure modes | Continuous, not one-and-done |

> **Model exam answer:** hallucination + knowledge cutoff in an enterprise knowledge scenario →
> **ground the model on enterprise data (RAG/Agent Search) with citations and human review for
> high-stakes items.**

### 1.2 Continuous monitoring and evaluation of gen AI models

The exam guide lists these explicitly. Learn them as a set:

| Practice | Purpose | Google Cloud mechanism |
| --- | --- | --- |
| **Automatic model upgrades** | Keep models current and secure without manual migration pain | Managed model lifecycle on Agent Platform, with version control and staged rollout |
| **Key performance indicators (KPIs)** | Decide whether the system is working — in *business* terms, not just model terms | Custom evaluation + your chosen metrics; see Session 5 |
| **Security patches and updates** | Keep the deployed system protected as threats evolve | Managed platform patching, SAIF-aligned controls |
| **Versioning** | Know what's deployed, support rollback and audit | **Model Registry** |
| **Performance tracking** | Watch model metrics over time | Model metrics + **Model Monitoring** |
| **Drift monitoring** | Detect when real-world data changes and accuracy degrades | **Model Monitoring** |
| **Data/feature management** | Keep the features a model uses consistent and reusable | **Agent Platform Feature Store** |
| **Pipeline automation** | Make retraining and redeployment repeatable | **Agent Platform Pipelines** |

**Useful concept — the three kinds of drift you can mention:**

- **Data drift** — the input distribution changes (customer behaviour shifts).
- **Concept drift** — the relationship between inputs and outcomes changes (fraud patterns evolve).
- **Model/training-serving skew** — the model sees different features in production than in training.

### 1.3 Human in the loop (HITL)

**Definition:** a process where human input and feedback are **directly integrated into ML
workflows**.

| HITL pattern | What it looks like | Best for |
| --- | --- | --- |
| **Content moderation** | Humans review flagged user-generated content contextually, catching what algorithms miss | Social platforms, marketplaces, community tools |
| **Sensitive applications** | Domain experts validate outputs in regulated, high-consequence fields | Healthcare, financial services, legal |
| **High-risk decision-making** | Human review of outputs before they take effect | Anything that materially affects a person: credit, hiring, eligibility, medical guidance |
| **Pre-generation review** | Experts validate model inputs/outputs **before deployment** — catching errors or bias before users are exposed | Pre-launch testing and sign-off |
| **Post-generation review** | Continuous human review and feedback **after** deployment, so the model improves and adapts | Ongoing quality management and retraining signals |

**Design patterns to recommend in answers:**

- **Human in the loop** — human approves *before* the action executes (highest control).
- **Human in the loop over the loop** — humans monitor a sample and intervene; the system runs automatically (scales better).
- **Human on the loop** — humans supervise dashboards, escalation queues, and anomaly alerts.

Always name **escalation paths** and **audit trails** for high-risk automation.

---

## 2. Responsible AI in business (objective 4.3)

**Definition:** responsible AI means ensuring your AI applications **don't cause harm and are
used ethically** — and it must be considered **throughout the entire AI lifecycle**, from data
preparation and model training through deployment and ongoing monitoring.

### 2.1 The dimensions the exam tests

| Dimension | What it means | Practical controls |
| --- | --- | --- |
| **Transparency** | People should know when they're interacting with AI, what it can do, and how it's used | Disclosures, watermarks/labels for generated media (e.g., SynthID-style provenance), documentation, model cards |
| **Privacy** | Protect personal data across the lifecycle | Data minimisation, purpose limitation, consent, retention limits, access control, **anonymisation and pseudonymisation** |
| **Data quality, bias, and fairness** | Biased or low-quality data yields unfair outcomes; fairness must be assessed deliberately | Representative data, bias testing across groups, disaggregated evaluation, HITL review, monitoring for skew |
| **Accountability** | A named human and organisation remain answerable for outcomes | Governance councils, RACI, approval gates, logging, escalation, incident response |
| **Explainability** | Decisions must be understandable to the people affected and to auditors | Citations from grounding, reasoning summaries, plain-language explanations, documentation |
| **Safety & security** | Systems resist misuse, attack, and unintended harm | Safety settings, red teaming, SAIF controls, Model Armor, IAM |

**Anonymisation vs pseudonymisation** — a frequently examined pair:

| | Anonymisation | Pseudonymisation |
| --- | --- | --- |
| What it does | Irreversibly removes identifying information | Replaces identifiers with pseudonyms/tokens, keeping a separate key |
| Re-identification risk | Effectively none | Possible if the key is available — so the key needs strong protection |
| Business use | Open datasets, analytics without personal data | Longitudinal analysis, personalisation, R&D where linkage is still needed |
| Note | Over-aggressive anonymisation can destroy analytical value | Considered **pseudonymised data is still personal data** under many regimes (e.g., GDPR) |

### 2.2 Google's AI Principles — the seven objectives

Memorise the seven; the exam may ask which principle a scenario violates or supports.

1. **Be socially beneficial.**
2. **Avoid creating or reinforcing unfair bias.**
3. **Be built and tested for safety.**
4. **Be accountable to people.**
5. **Incorporate privacy design principles.**
6. **Uphold high standards of scientific excellence.**
7. **Be made available for uses that accord with these principles.**

Google also publishes **applications it will not pursue** — technologies likely to cause
overall harm, weapons or technologies whose principal purpose is to cause injury, and
technologies used for surveillance that violate internationally accepted norms. For a leader,
this is the template for writing your **own** "use cases we will not pursue" list.

---

## 3. Secure AI and SAIF (objective 4.2)

**Definition:** **secure AI** means protecting your AI applications **from harm** — malicious
attacks, misuse, and theft — across the whole ML lifecycle.

### 3.1 Responsible AI vs secure AI — never confuse these

| | **Responsible AI** | **Secure AI** |
| --- | --- | --- |
| Question it answers | "Are we doing the right thing?" | "Are we protected from attack and misuse?" |
| Concerns | Fairness, privacy, transparency, accountability, explainability, avoiding harm | Threats, vulnerabilities, data protection, access control, resilience |
| Typical mechanisms | AI Principles, governance, HITL, bias testing, documentation | SAIF, IAM, Security Command Center, Model Armor, VPC Service Controls, encryption |
| Exam cue | Ethics, bias, trust, disclosure, accountability | Attack, injection, exfiltration, permissions, monitoring |

### 3.2 SAIF — Google's Secure AI Framework

**Purpose:** SAIF helps organisations **manage AI/ML model risks and ensure security**, by
applying proven security engineering to AI systems rather than inventing a parallel universe
of controls. It is technology-agnostic and intended for collaborative industry use.

**The six core elements (in Google's own words, with the practical meaning):**

| # | Core element | What it means in practice |
| --- | --- | --- |
| 1 | **Expand strong security foundations to the AI ecosystem** | Existing AppSec, IAM, and supply-chain controls apply to AI — adapt proven mitigations (e.g., input sanitisation against prompt injection) |
| 2 | **Extend detection and response to bring AI into an organisation's threat universe** | Put AI systems in scope for your SOC, threat intel, and incident response — not a separate silo |
| 3 | **Automate defences to keep pace with existing and new threats** | Attackers use automation; defences must run at machine speed |
| 4 | **Harmonise platform-level controls for consistent security across the organisation** | One control plane for AI, not per-team snowflakes |
| 5 | **Adapt controls to adjust mitigations and create faster feedback loops for AI deployment** | Red-team, learn from incidents, update data/models, shorten the fix cycle — AI risk isn't static |
| 6 | **Contextualise AI system risks in surrounding business processes** | Risk depends on the business process the model sits in, not the model alone |

**The four components SAIF maps controls across:** **Data · Infrastructure · Model ·
Application.** (If an answer option lists controls by domain, these are the domains.) SAIF's
control families span data management and sanitisation, model access and integrity, input and
output validation, application access and agent permissions/observability, plus assurance and
governance activities such as red teaming, vulnerability management, threat detection, and
incident response.

**Threats SAIF is designed against (name these in scenario answers):**

| Threat | What it is |
| --- | --- |
| **Prompt injection** | Malicious instructions hidden in input or retrieved content that hijack the model's behaviour |
| **Jailbreak** | Techniques that bypass safety guardrails to get prohibited output |
| **Data poisoning** | Tampering with training/fine-tuning data to corrupt model behaviour |
| **Training data extraction / disclosure** | Pulling sensitive or private data out of a model |
| **Model theft** | Stealing model weights or reverse-engineering the model |
| **Data exfiltration** | Moving your data out of its authorised boundary via the AI system |
| **Insecure output handling** | Downstream systems trusting model output and executing it unsafely |
| **Denial of service / resource abuse** | Overwhelming the system or running up model costs |

### 3.3 Google Cloud security tools and their purposes

| Tool / capability | Purpose | One-line memory hook |
| --- | --- | --- |
| **Secure-by-design infrastructure** | Google's own hardened foundations you inherit | "You don't have to build the vault" |
| **Identity and Access Management (IAM)** | Control **who can access which resources** — least privilege, roles, service accounts, agent identities | "Who can do what" |
| **Security Command Center** | **Security posture visibility**: findings, misconfigurations, threats across the estate | "The dashboard that tells you what's wrong" |
| **Workload monitoring tools** | Observe running workloads for anomalies and policy violations; build and maintain secure AI systems | "Watch it while it runs" |
| **Model Armor** | Screen prompts and responses to block injection/jailbreak attempts and prevent sensitive-data disclosure | "The bouncer for prompts and answers" |
| **VPC Service Controls** | Service perimeters that prevent data exfiltration | "Fence the data" |
| **Cloud KMS / CMEK** | Customer-managed encryption keys — you control the keys | "Bring your own keys" |
| **Cloud Logging / audit logs** | Full audit trail of actions, tool calls, and access | "Evidence" |
| **Data residency / location controls** | Keep data in approved regions to meet sovereignty rules | "Data stays home" |

### 3.4 Security throughout the ML lifecycle

| Stage | Security concern | Control direction |
| --- | --- | --- |
| **Data ingestion & preparation** | Poisoning, unauthorised data, PII leakage | Data provenance, sanitisation, access control, privacy-enhancing techniques |
| **Model training** | Model theft, insecure tooling, supply chain | Secure-by-default tooling, access/integrity management, model inventory |
| **Deployment** | Insecure endpoints, over-permissioned service accounts, exfiltration | IAM least privilege, VPC Service Controls, CMEK, endpoint hardening |
| **Management / operations** | Drift, new attack techniques, unpatched systems, hijacked agents | Model Monitoring, red teaming, vulnerability management, threat detection, incident response, agent observability, prompt/response screening |

> **Agent-specific security (increasingly examined):** agents act autonomously, so they need
> **scoped identity and permissions**, **user authorisation** for sensitive actions,
> **observability** of decisions and tool calls, and **guardrails on tool payloads** — plus
> human escalation paths. "An agent with broad credentials and no audit trail" is always the
> wrong answer.

---

## 4. The leader's playbook: limitation → mitigation → responsible control

Rehearse this table; it converts almost any Domain 3/4 scenario into the right answer.

| Scenario symptom | Mitigation (technique) | Responsible / secure control |
| --- | --- | --- |
| Invents facts, policies, citations | Ground with RAG/Agent Search; require citations; lower temperature | Human review on high-stakes answers; monitor groundedness |
| Doesn't know recent information | Grounding with Google Search; refresh RAG index | Document freshness SLAs; disclose recency limits |
| Skewed outcomes for a group | Improve data representativeness; bias testing | Disaggregated fairness evaluation; HITL; AI Principles review |
| Errors in a regulated decision | HITL pre-generation review; expert validation | Accountability/RACI, audit logs, escalation path |
| Quality degrades after launch | Drift monitoring; retrain; version and roll back | Change control, Model Registry, incident response |
| Users paste sensitive data into a chatbot | Data-loss prevention, scoped access, pseudonymisation | IAM, VPC Service Controls, Model Armor, employee policy and training |
| Attacker hides instructions in content | Input validation and sanitisation; output validation | Model Armor, red teaming, threat detection |
| Agent might take a wrong action at scale | Restrict tools and permissions; require approval for irreversible actions | Agent identity, observability, audit trail, kill switch |

---

## Exam traps in this session

1. **Responsible AI ≠ secure AI.** Ethics/trust vs protection from attack. Read the stem's verb.
2. **SAIF is about securing AI systems**, and it *builds on* existing controls rather than
   replacing them — the "expand strong security foundations" element is a favourite distractor.
3. **HITL has pre- and post-generation forms.** "Before users are exposed" = pre-generation;
   "continuous feedback after launch" = post-generation.
4. **Fine-tuning is not a hallucination fix.** Grounding/RAG is.
5. **Monitoring is not just uptime.** Performance tracking, drift monitoring, versioning, and
   KPI evaluation are the four pillars the exam names.
6. **Anonymisation is irreversible; pseudonymisation is reversible with the key.**
7. **Bias comes from data as much as from models**, so the fix usually starts upstream
   (data quality and representation), not with a bigger model.
8. **Auto-upgrades are a security and quality practice**, not only a maintenance chore — they
   deliver patches and improvements continuously.

## Rapid self-check

1. Name five limitations of foundation models and one mitigation each.
2. What's the difference between pre-generation and post-generation HITL review?
3. List the six core elements of SAIF in your own words.
4. Which tool gives you security posture visibility, and which prevents data exfiltration?
5. A model's accuracy silently degrades six months after launch. What are the two likely
   causes and which Google Cloud capability detects it?
6. Your company must not store personal data in prompts. Name three controls.
7. Which is reversible: anonymisation or pseudonymisation — and why does that matter legally?

### Answers

1. **Data dependency** → better/more representative data; **knowledge cutoff** → grounding
   (Google Search) and refreshed retrieval; **hallucination** → grounding/RAG, citations,
   HITL; **bias/fairness** → representative data, bias testing, disaggregated evaluation;
   **edge cases** → testing with real-world edge cases, HITL, red teaming; (**context
   window/cost** → retrieval instead of stuffing, model tier selection).
2. **Pre-generation review** validates outputs before deployment so users are never exposed;
   **post-generation review** continuously reviews outputs after deployment so the system
   improves and adapts.
3. (1) Expand strong security foundations to AI; (2) extend detection and response to bring AI
   into your threat universe; (3) automate defences to keep pace with threats; (4) harmonise
   platform-level controls organisation-wide; (5) adapt controls with faster feedback loops;
   (6) contextualise AI risk within the surrounding business process.
4. **Security Command Center** for posture visibility; **VPC Service Controls** (with CMEK,
   IAM, and Model Armor) to prevent exfiltration.
5. **Data drift** (inputs changed) and **concept drift** (relationships changed) — detected by
   **Model Monitoring**, with versioning in **Model Registry** and retraining via **Pipelines**.
6. **IAM** least-privilege access, **pseudonymisation/anonymisation** or redaction before
   prompting, **VPC Service Controls** perimeters, plus **Model Armor** output screening and
   clear employee data-handling policy.
7. **Pseudonymisation** — the mapping key allows re-identification, so the data remains
   personal data under many privacy regimes and needs protection; anonymisation is intended to
   be irreversible.

---

**Next:** [Session 5 — Business strategy and measurable value](session-5-business-strategy.md)
