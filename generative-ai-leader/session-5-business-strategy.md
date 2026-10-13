# Session 5 — Business Strategy: Model Selection and Measurable Business Value

**Exam domain:** 4. Business strategies for a successful gen AI solution (~15%, objective 4.1)
**Goal of this session:** answer scenario questions the way a leader should — start from the
business goal, respect the constraints, choose the lightest solution that works, and express
value in numbers the business already cares about.

---

## 1. Types of gen AI solutions

| Solution type | What it delivers | Typical metric of success |
| --- | --- | --- |
| **Text generation** | Drafts, replies, summaries, reports, translations, code | Time saved per output, first-draft acceptance rate, revision cycles |
| **Image generation** | Product imagery, marketing assets, design concepts | Cost per asset, campaign cycle time, asset volume |
| **Code generation** | Scaffolding, tests, refactors, migration help, documentation | Developer velocity, defect escape rate, onboarding time |
| **Video / audio generation** | Campaign video, training content, voice experiences | Production cost and turnaround time |
| **Data analysis & discovery** | Conversational analytics, anomaly and trend discovery | Time-to-insight, questions answered without data-team help |
| **Personalised user experience** | Recommendations, dynamic content, tailored journeys | Conversion, engagement, retention, average order value |
| **Document processing & automation** | Extraction, classification, routing, summarisation at scale | Straight-through processing rate, manual touch time, error rate |
| **Agents** | Multi-step task completion across systems | Tasks fully resolved without human intervention, handle time, cost per resolution |

**Augmentation vs automation** — a favourite framing:

- **Augmentation** assists a human who remains responsible (drafting, summarising, suggesting). Lower risk, faster to adopt, easier to justify.
- **Automation** completes work without a human in the loop. Higher value per unit, but requires HITL design, escalation paths, and tighter controls.

**Recommended path:** *augment first, automate where the evidence supports it.*

---

## 2. Needs and constraints that shape the solution

### 2.1 Needs (from the official study guide — learn this list)

| Factor | The question to ask | How it changes the solution |
| --- | --- | --- |
| **Scale** | How many users / interactions / documents? | Drives model tier (Flash-Lite vs Pro), infrastructure, and provisioned throughput |
| **Customisation** | How specialised is the domain or behaviour? | Prompting → grounding → fine-tuning → custom model |
| **User interaction** | Chat, embedded, batch, voice, agentic? | Determines modality, latency budget, and UI surface |
| **Privacy** | How sensitive is the data? | Deployment location, encryption, residency, on-device or self-hosted models (Gemma), pseudonymisation |
| **Latency** | What response time is acceptable? | Flash/Flash-Lite tiers, caching, edge deployment, retrieval tuning |
| **Connectivity** | Always-online, intermittent, or offline? | On-device models (Gemini Nano), edge deployment (LiteRT), local models |

### 2.2 Resources

| Resource | The question to ask |
| --- | --- |
| **People** | Do we have AI/ML expertise, or do we need low-code tools, AutoML, and partners? |
| **Money** | What's the budget — build, buy, or consume APIs? What's the run-rate at volume? |
| **Time** | What's the deadline? Prebuilt solutions ship in weeks; custom models take quarters. |

### 2.3 Technical constraints that quietly decide the answer

- **Model availability and reliability** — uptime, redundancy, disaster recovery, regional availability.
- **Context window** — how much content must be in view at once, and what it costs.
- **Modality coverage** — does the model handle the input/output types you need?
- **Data readiness** — quality, accessibility, governance, and permissions.
- **Compliance** — data residency, sector regulation, retention, auditability.
- **Integration** — does it connect to the systems of record (CRM, ERP, ITSM, data warehouse)?

---

## 3. Choosing the right model for the business need

The exam lists the selection factors explicitly — memorise them as a checklist, then apply
them to the scenario's *stated* constraints.

| Factor | The question | Trap to avoid |
| --- | --- | --- |
| **Modality** | Does the model's input/output type match the task (text, image, audio, video, code)? | Choosing a text-only model for an image task, or a heavyweight multimodal model for plain text |
| **Context window** | How much data must be considered at once? | Assuming "bigger is always better" — bigger raises cost and can dilute relevance |
| **Security and privacy** | Where can the data live, who can access it, what controls are required? | Ignoring residency and access-control requirements |
| **Availability and reliability** | Uptime guarantees, redundancy, DR, regional coverage | Assuming a preview model is suitable for a critical production service |
| **Cost** | Input/output token economics, volume, fine-tuning and serving cost, total cost of ownership | Comparing only per-token price and ignoring latency, retries, and human review cost |
| **Performance** | Accuracy, speed, and efficiency for *this* task — with your evaluation set | Assuming the largest model is always most accurate for a narrow task |
| **Fine-tuning and customisation** | Do you need to adapt behaviour, or just supply context? | Fine-tuning to fix facts (use grounding) |

### 3.1 Model tier selection in practice

| Need | Tier pattern | Example Google option |
| --- | --- | --- |
| Deep reasoning, complex analysis, long-context understanding, hardest quality bar | Flagship | **Gemini Pro** |
| High-volume production, agents, coding, balanced cost/latency | Workhorse | **Gemini Flash** |
| Simple, high-throughput tasks (classification, extraction, routing) | Cheapest capable | **Gemini Flash-Lite** |
| On-device, private, offline | Edge | **Gemini Nano** with **LiteRT** |
| Self-hosted, fully custom, open weights | Open | **Gemma** |
| Images | Diffusion | **Imagen** |
| Video | Video generation | **Veo** |
| Speech | Speech models | **Chirp** |

### 3.2 Build vs buy vs adapt

| Path | When it's right | Time to value |
| --- | --- | --- |
| **Consume a prebuilt app** (Gemini app/Workspace/Enterprise) | The need is standard productivity or knowledge access | Days–weeks |
| **Consume APIs with prompts + grounding** | Your use case is specific but the model doesn't need changing | Weeks |
| **Build on the platform with AutoML / prebuilt RAG** | You need custom behaviour or private-data grounding without ML specialists | Weeks–months |
| **Custom training / fine-tuning** | You have unique data, deep ML skill, and a durable differentiator | Months+ |

> **Exam principle:** choose the **lightest solution that satisfies the constraints.** Answers
> that jump straight to custom training when a prebuilt option exists are usually wrong.

---

## 4. Integrating gen AI into an organisation (objective 4.1)

### 4.1 The recommended planning steps

| Step | What it means | Leader's evidence of progress |
| --- | --- | --- |
| **1. Establish a clear vision** | Tie gen AI to specific business goals; write your "use cases we will not pursue" list | A one-page strategy with named owners |
| **2. Prioritise use cases** | Rank by value, feasibility, data readiness, and risk; pick focused implementations with clear business value | A ranked portfolio, with 2–3 pilots starting |
| **3. Invest in capabilities** | Data strategy, platform, skills, governance; leverage existing resources; develop AI talent | Data quality remediation underway; training plan delivered |
| **4. Manage change** | Process redesign, role clarity, communications, adoption support | Adoption metrics tracked; champions in each function |
| **5. Measure value** | Baselines, KPIs, business impact reporting | An executive dashboard with before/after numbers |
| **6. Champion responsible AI** | Ethics guidelines, security, privacy, HITL, monitoring | Governance body live; controls mapped to SAIF |

**Top-down + bottom-up:** the successful pattern combines **leadership setting the vision,
strategy, and guardrails** with **employees identifying practical applications and feeding
back what works**. Neither alone is sufficient: purely top-down produces shelfware, purely
bottom-up produces ungoverned shadow AI.

**Additional leadership themes the exam rewards:** strategic focus, encouraging exploration
and collaboration, resourcing (data strategy, existing assets, talent), impact measurement,
and **continuous improvement** based on feedback and data.

### 4.2 Where to start — pilot selection criteria

| Criterion | Ask |
| --- | --- |
| **Value** | Does it move a metric the business already tracks? |
| **Feasibility** | Is the data accessible and good enough today? |
| **Risk** | Can we contain the blast radius with HITL and controls? |
| **Adoption** | Will people actually change how they work? |
| **Reusability** | Does it build a capability we'll use again (retrieval, governance, evaluation)? |

---

## 5. Explaining measurable business value

### 5.1 The value categories to quote

| Category | What to measure | Example framing |
| --- | --- | --- |
| **Revenue growth** | Conversion, upsell, cross-sell, new offerings, faster quoting | "Personalised recommendations lift conversion by X%" |
| **Cost reduction / avoidance** | Labour hours, processing cost, vendor spend, error remediation | "Invoice processing cost per document down X%" |
| **Productivity** | Time per task, throughput per person, cycle time | "Average handling time down 4 minutes per contact" |
| **Customer experience** | CSAT, NPS, first-contact resolution, response time | "First-response time cut from hours to seconds" |
| **Risk & compliance** | Incident rates, audit findings, control coverage | "100% of customer responses screened and logged" |
| **Speed / innovation** | Time to market, experiment velocity, launch cadence | "Campaign asset turnaround from 3 weeks to 3 days" |

### 5.2 The measurement discipline — what makes it credible

1. **Establish a baseline before you launch.** No baseline, no credible claim.
2. **Define the KPI in business terms**, then map to model metrics (accuracy/groundedness
   explain *why* the business metric moved).
3. **Use an evaluation set** with real cases, including edge cases, and check quality with
   humans on a sample.
4. **Track adoption**, not just availability — licences assigned is not transformation.
5. **Model the unit economics:** cost per interaction or per document (tokens + retrieval +
   review time) versus the value of the outcome.
6. **Attribute honestly:** use control groups where possible; beware claiming credit for
   seasonality.
7. **Report continuously** — value reporting is a standing cadence, not a launch document.

**A five-line business case you can reuse in any scenario:**

> **Goal:** reduce invoice processing cost while improving compliance.
> **Baseline:** 14 minutes and $6.20 per invoice, 4% error rate, 60,000 invoices/year.
> **Approach:** Document AI extraction + Gemini summarisation, grounded on the vendor master;
> human review for exceptions above $25,000 (HITL).
> **Value:** 70% straight-through processing → approx. $230k annualised saving plus reduced
> late-payment penalties; payback in two quarters.
> **Risk controls:** least-privilege access, full audit logging, Model Armor screening, drift
> monitoring, and quarterly bias reviews.

### 5.3 Worked scenario patterns

| Industry | Scenario | Best-fit approach |
| --- | --- | --- |
| **Retail** | Better product discovery on the site; support volume spiking at peak | **Agent Search** for discovery; **Gemini Enterprise for Customer Experience** for support; Flash tier for cost at peak |
| **Financial services** | Analysts spend hours reading dense filings; compliance needs citations | **Gemini Notebook** for research over a curated set; grounded RAG with **citations**; HITL for anything customer-facing; **IAM + VPC Service Controls + CMEK** |
| **Healthcare** | Clinicians need summaries of patient notes; accuracy is critical | Grounded summarisation on **private data** with **HITL pre-generation review**; de-identification/pseudonymisation; no autonomous clinical decisions |
| **Manufacturing** | Technicians need instant access to maintenance manuals; some sites lack connectivity | **Agent Search** over manuals; **Gemma/Gemini Nano on-device** for offline sites with **LiteRT** |
| **Public sector** | Multilingual citizen services; strict data residency | **Translation API + Text-to-Speech** for multilingual access; **on-prem/self-hosted** open models plus residency controls |
| **Software** | Developers want faster code review and test generation | Code-focused **Gemini Flash/Pro** in the IDE and pipeline; **human review** mandatory; secrets scanning and least privilege |
| **Professional services** | Proposal teams rewrite the same content repeatedly | **Gems** and prompt templates for brand-voice reuse; **Agent Search** over past proposals; measure win rate and turnaround |

**How to answer any of these on the exam:** name the *verb* (create/summarise/discover/
automate), the *surface* (app, Workspace, Enterprise, platform, API), the *technique*
(prompting/grounding/RAG/fine-tuning), and the *control* (HITL, IAM, monitoring) — in that
order.

---

## Exam traps in this session

1. **Business goal first, technology second.** Answers that lead with the model name are
   usually the distractor.
2. **Don't over-engineer.** Prefer prebuilt/API solutions unless the constraints demand custom.
3. **"Highest accuracy" isn't automatically the right choice** if latency or cost breaks the
   use case.
4. **Cost means total cost of ownership**, including retrieval, human review, and integration —
   not just tokens.
5. **Adoption is part of value.** A technically successful pilot nobody uses has zero value.
6. **Top-down only ≠ strategy.** The recommended approach blends top-down vision with
   bottom-up discovery.
7. **Value must be measurable.** If the scenario asks how to demonstrate value, the answer
   involves a baseline, a KPI, and a business metric — not a model benchmark.
8. **Augment before you automate** in high-stakes processes.

## Rapid self-check

1. List the six "needs" factors and the three "resources" from the official study guide.
2. Name the seven model-selection factors.
3. A support team has 50,000 chats/month, needs sub-second responses, and is price-sensitive.
   Which model tier, and why?
4. What two directional strategies must combine for a successful gen AI strategy?
5. Give three ways to demonstrate value for a document-processing solution, with the metric
   for each.
6. Why is a baseline essential before launching a pilot?

### Answers

1. **Needs:** scale, customisation, user interaction, privacy, latency, connectivity.
   **Resources:** people, money, time.
2. **Modality, context window, security, availability and reliability, cost, performance,
   fine-tuning/customisation.**
3. A **Flash or Flash-Lite tier** model — high volume plus latency sensitivity plus cost
   sensitivity rules out the largest flagship model; add prompt caching and retrieval tuning
   to control cost.
4. **Top-down** (leadership sets vision, priorities, guardrails) combined with **bottom-up**
   (employees find practical applications and give feedback).
5. E.g., **cost per document processed** (cost reduction), **straight-through processing
   rate / manual touch time** (productivity), **error and audit-finding rate** (risk and
   compliance), plus **turnaround time** (speed).
6. Without a pre-launch baseline you cannot attribute improvement, prove ROI, or distinguish
   the pilot's effect from seasonality — and you lose the ability to defend the investment
   when budget is reviewed.

---

**Next:** [Session 6 — Recall quiz](session-6-recall-quiz.md) · then
[Final exam mindset](final-exam-mindset.md)
