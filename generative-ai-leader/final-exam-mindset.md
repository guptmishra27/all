# Final Exam Mindset — How to Answer Any Scenario Question

Most Generative AI Leader questions are short business situations with four plausible
sounding options. This file is the decision procedure to apply on every one of them. Read it
twice on exam day.

---

## 1. The five-step scenario algorithm

Run this in your head for every scenario question. It takes about 20 seconds.

| Step | Ask yourself | What it filters out |
| --- | --- | --- |
| **1. What is the business goal?** | Growth, cost, productivity, CX, risk, speed, or compliance? | Options that are technically neat but don't serve the stated goal |
| **2. What is the constraint?** | Privacy, residency, latency, cost, connectivity, modality, regulation, skill level, timeline? | Options that ignore the stated limitation |
| **3. Which layer and verb?** | Create / summarize / discover / automate — and is this an **application**, **platform**, **model**, **agent tool**, or **API** need? | Options from the wrong layer (e.g., a model when the question is about a user surface) |
| **4. Which technique?** | Prompting (which technique?), grounding/RAG (which data source?), fine-tuning (behaviour only), or tooling? | Options that fix the wrong thing (fine-tuning to fix facts, bigger context to fix freshness) |
| **5. Which responsible/secure control?** | HITL, IAM, monitoring, safety, Model Armor, residency, audit trail? | Options that skip the control a leader would never skip |

**The one-sentence version:** *Business goal first → constraint → layer/verb → technique →
control.*

---

## 2. The answer-choice language of the exam

Correct answers in this certification tend to share a vocabulary. Learn to hear it.

| Phrase in the correct answer | Why it's right |
| --- | --- |
| "Ground the model on the organisation's own data with citations" | Fixes hallucination and the knowledge cutoff, and creates auditability |
| "Add human review before the decision takes effect" | High-risk decisions need HITL and accountability |
| "Start with the business requirement and constraints" | Domain 4 rewards business-first thinking |
| "Use least-privilege access and an audit trail" | Standard secure-AI posture for agents and apps |
| "Establish a baseline and define a KPI" | Measurement is the only credible path to proving value |
| "Pilot with a focused, high-value use case" | Matches the recommended prioritisation approach |
| "Combine top-down vision with bottom-up experimentation" | The official strategy guidance |
| "Use the lightest solution that meets the need" | Avoids over-engineering |
| "Monitor for drift and performance degradation after launch" | Reflects the management stage of the ML lifecycle |
| "Screen inputs and outputs" | Prompt injection, jailbreak, and data-leakage defence |

---

## 3. Distractor patterns — how wrong answers are built

| Distractor pattern | Example | Why it's wrong |
| --- | --- | --- |
| **Right goal, wrong layer** | Recommending a model upgrade when the problem is that users can't find documents | The issue is discovery/grounding, not model quality |
| **Fine-tune everything** | "Fine-tune the model on the latest price list" | Fine-tuning doesn't reliably add facts; use grounding |
| **Maximum capability reflex** | "Use the most powerful model for every task" | Ignores latency, cost, and volume; Flash tiers exist for a reason |
| **Context-stuffing** | "Put all 10,000 documents in the context window" | Costly and less precise than retrieval; context windows are not a substitute for RAG |
| **Remove the human** | "Automate fully and remove review once accuracy is good" | High-stakes decisions keep HITL, accountability, and escalation |
| **Security/ethics swap** | Offering "bias testing" as the answer to an attack question | Responsible AI ≠ secure AI — check the stem's verb |
| **Consumer tool for an enterprise need** | Using the free consumer surface where governance and residency are required | Enterprise requirements demand enterprise controls |
| **Tool naming confusion** | "Google AI Studio for production deployment" | AI Studio = free prototyping; Agent Studio = production build/deploy |
| **Bigger is better bias** | "Use a larger context window / larger model to fix accuracy" | Fixes the symptom, not the cause; costs more |
| **Technology-first answer** | "Build a custom model from scratch" as the opening move | Prebuilt/API/adapt paths come first |
| **Unmeasured value claim** | "Improves efficiency by 40%" with no baseline or metric named | Value claims must be measurable and specific |
| **Old-name trap** | "Vertex AI Studio" or "Agentspace" | Translate to current names — don't dismiss the option just for using the older label |

---

## 4. Keyword → likely answer (fast pattern matching)

Use this when a stem is long and you need to triangulate quickly. It is a *hint*, not a
substitute for the five steps.

| If the stem mentions… | The likely answer involves… |
| --- | --- |
| Documents buried across systems, employees can't find answers | **Gemini Enterprise** + **Agent Search** (prebuilt RAG) with permission-aware access |
| "Must be current / latest announcement / public information" | **Grounding with Google Search** |
| "Our own policies / catalogue / contracts" | **Enterprise RAG** (Agent Search or RAG APIs) with citations |
| "Invents / makes up / hallucinating" | Grounding/RAG, lower temperature, HITL, evaluation |
| "Consistent format, specific labels" | **Few-shot prompting** (or fine-tuning if behaviour must persist at depth) |
| "Multi-step process, needs checks between steps" | **Prompt chaining** (plus HITL for high stakes) |
| "Reasoning through a calculation or logic" | **Chain-of-thought** |
| "Agent must look something up / act in a system" | **Tools** — extension (external API), function (defined action), data store (information), plugin |
| "Agents from different vendors must work together" | **A2A protocol** |
| "Prototype fast and free" | **Google AI Studio** |
| "Production, scale, governance" | **Agent Studio** on **Agent Platform** |
| "Choose among many models / avoid lock-in / open models" | **Model Garden**; **Gemma** for self-hosted |
| "Train a model but we lack ML expertise" | **Agent Platform AutoML** |
| "High volume, latency-sensitive, cost-sensitive" | **Flash / Flash-Lite tier** |
| "On-device / offline / no connectivity" | **Gemini Nano** + **LiteRT** (or Gemma self-hosted) |
| "Transcribe calls / voice interface" | **Speech-to-Text** / **Text-to-Speech** |
| "Extract data from invoices/forms" | **Document AI API** |
| "Translate documents keeping layout" | **Document Translation API** |
| "Moderate images / analyse video" | **Cloud Vision** / **Cloud Video Intelligence** |
| "Sentiment / entities / classification" | **Natural Language API** |
| "Contact centre, virtual agents, live-agent assist" | **Gemini Enterprise for Customer Experience** (CX Agent Studio / Agent Assist / CX Insights) |
| "Cost per interaction, prove ROI, budget approval" | Baseline + KPI + business metric (Session 5 §5) |
| "Regulated, sensitive, high-stakes decision" | HITL + accountability + logging + least privilege |
| "Attack, injection, jailbreak, leakage" | **Model Armor**, input/output validation, IAM, VPC Service Controls, SAIF |
| "Who can access what" | **IAM** |
| "Security posture visibility / findings" | **Security Command Center** |
| "Keep data in-country / own the keys" | Data residency controls + **CMEK** |
| "Quality degrading over time" | **Model Monitoring** (drift), versioning in **Model Registry**, retraining via **Pipelines** |
| "Bias, fairness, transparency, accountability" | Responsible AI practices + **Google's AI Principles** + HITL + disaggregated evaluation |
| "A framework to secure AI systems" | **SAIF** (six core elements) |

---

## 5. Time and format management

- **Budget:** with 50–60 questions in 90 minutes you have ~90 seconds each. Flag and skip any
  question that takes longer than two minutes; come back at the end.
- **Answer everything.** There is no penalty for guessing — an unanswered question is a
  guaranteed loss.
- **Read the last sentence first** on long scenarios; it usually contains the actual question.
- **Watch qualifiers:** "most appropriate", "best", "first step", "biggest risk", "primary
  benefit". They change which option wins.
- **When two options look right,** prefer the one that:
  1. serves the **stated business goal** most directly,
  2. respects **every stated constraint** (there's usually one option that quietly violates it),
  3. adds the **control** a leader would require (HITL, audit, least privilege),
  4. is the **least complex** solution that satisfies 1–3.
- **When the stem is vague,** the answer is usually the one that starts with the **business
  requirement** or a **discovery/assessment step**, not a technology purchase.

---

## 6. The guaranteed-topic checklist

If you can explain each of these in two sentences, you are ready:

- [ ] AI → ML → deep learning → gen AI nesting, and what a foundation model and an LLM are
- [ ] Supervised, unsupervised, reinforcement, and self-supervised learning
- [ ] The ML lifecycle (four stages) with one Google Cloud tool per stage
- [ ] Structured vs unstructured, labeled vs unlabeled, data quality dimensions
- [ ] The five layers of the gen AI landscape and one product example per layer
- [ ] Gemini, Gemma, Imagen, Veo — what each is for, Pro vs Flash vs Flash-Lite
- [ ] Gemini app vs Gemini for Workspace vs Gemini Enterprise vs Gemini Notebook
- [ ] Google AI Studio vs Agent Studio
- [ ] Model Garden, Model Builder, AutoML, Pipelines, Model Registry, Model Monitoring, Feature Store
- [ ] Agent Search, RAG APIs, Grounding with Google Search
- [ ] Agent components (model, tools, reasoning loop) and tool types (extensions, functions, data stores, plugins)
- [ ] The eight Cloud AI APIs and their tasks
- [ ] Zero-shot, one-shot, few-shot, role, chaining, chain-of-thought, ReAct, metaprompting
- [ ] Grounding types (first-party, third-party, world) and the four RAG steps
- [ ] Sampling parameters: temperature, top-p, token count, output length, safety settings
- [ ] The six foundation-model limitations and their mitigations
- [ ] HITL: pre-generation vs post-generation, and where each applies
- [ ] Monitoring and evaluation: versioning, performance tracking, drift, KPIs, auto-upgrades
- [ ] Responsible AI dimensions + Google's seven AI Principles
- [ ] SAIF's six core elements, and the difference between responsible AI and secure AI
- [ ] IAM, Security Command Center, Model Armor, VPC Service Controls, CMEK — what each does
- [ ] Model selection factors and build/buy/adapt
- [ ] How to express value: baseline → KPI → business metric; the six value categories
- [ ] The naming changes (Vertex AI → Agent Platform, and the rest)

---

## 7. Exam-day routine

1. **Night before:** read this file and [complete-reference.md](complete-reference.md) once.
   Do not cram new material.
2. **Morning of:** skim the guaranteed-topic checklist above; say the five-step algorithm out
   loud.
3. **During:** first pass answers everything you know; flagged questions get a second pass with
   the two-option tiebreaker rule.
4. **Never leave blanks.** If a question is entirely unfamiliar, choose the option that serves
   the business goal with a grounding or governance control attached — that combination is
   correct far more often than not.

**Final reminder:** this exam tests judgement, not memorisation of feature lists. When in
doubt, ask: *"What would a responsible leader who understands grounding, governance, and cost
do next?"* Then pick that option.
