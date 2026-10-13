# Answer Key — Session 6 Recall Quiz

Every answer includes a **domain label** (Fundamentals · Offerings · Techniques · Strategy)
and a **Revisit** pointer to the exact section to re-read if you missed it.

> **Warning:** do not read further until you have written answers to all 60 items in
> [session-6-recall-quiz.md](session-6-recall-quiz.md).

---

## Part A — Rapid recall (25 items)

**A1.** *(Fundamentals)* A **foundation model** is a very large model pre-trained on massive,
broad, mostly unlabeled data that develops general world understanding and can be adapted to
many downstream tasks. Businesses rarely train one from scratch because pretraining requires
enormous data, specialised talent, and very large compute investment — it is cheaper, faster,
and lower-risk to consume a foundation model and adapt it with prompting, grounding, or
fine-tuning. *Revisit:* Session 1 §3.

**A2.** *(Fundamentals)* An **LLM** is a type of foundation model specialised for
understanding and generating human language (and often code). Every LLM is a foundation
model; not every foundation model is an LLM (Imagen and Veo are foundation models for images
and video). *Revisit:* Session 1 §1 and §3.

**A3.** *(Fundamentals)* A **diffusion model** generates content by starting from random
noise and iteratively denoising it into a coherent output guided by a prompt. Google's
**Imagen** (images) and **Veo** (video) use diffusion-style generation. *Revisit:* Session 1
§1 and §7.

**A4.** *(Fundamentals)* **Supervised** (learns from labeled data — input/answer pairs),
**unsupervised** (finds natural groupings in unlabeled data), and **reinforcement** (learns
through interaction and feedback to maximise reward). **Supervised learning requires labeled
data.** *Revisit:* Session 1 §2.

**A5.** *(Fundamentals)* **Self-supervised learning** lets a model manufacture its own
training signal from raw data (for example, predicting the next token). It matters because it
is how foundation models learn from vast amounts of *unlabeled* text without humans labelling
everything — which is what makes their breadth possible. *Revisit:* Session 1 §2.

**A6.** *(Fundamentals)* **Data ingestion and preparation** (Cloud Storage, BigQuery, Dataflow,
Dataproc, Dataplex) → **model training** (Agent Platform custom training, AutoML, Model
Garden, Colab Enterprise) → **model deployment** (Agent Platform endpoints, Model Registry,
Cloud Run, GKE) → **model management** (Model Monitoring, Feature Store, Pipelines, Model
Registry). *Revisit:* Session 1 §5.

**A7.** *(Fundamentals/Offerings)* **Model Registry** versions models; **Model Monitoring**
detects performance degradation and **drift**. *Revisit:* Session 1 §5 and Session 4 §1.2.

**A8.** *(Fundamentals)* **Structured data** is organised into rows/columns and is easy to
query — e.g., transactions in a data warehouse. **Unstructured data** has no predefined
structure — e.g., contracts, emails, call recordings, images. Gen AI's commercial unlock is
the **unstructured** majority: it can read, summarise, search, and extract from content that
traditional analytics could never process at scale. *Revisit:* Session 1 §4.1.

**A9.** *(Fundamentals)* Accessibility covers whether data is **readily available, usable, in
the right format, at acceptable cost, with the right permissions**. It is a business problem
because value depends on organisational decisions — ownership, governance, licensing, access
rights, and data-sharing — not just on engineering. *Revisit:* Session 1 §4.2.

**A10.** *(Fundamentals)* A **token** is a meaningful chunk of text (roughly a word-piece or
punctuation mark). Leaders care because tokens determine **cost, latency, and limits** — token
count drives your bill and your response times. *Revisit:* Session 1 §3 and Session 3 §3.

**A11.** *(Fundamentals/Techniques)* The **context window** is how much text the model can
consider at one time (prompt + conversation + retrieved content). A larger window allows more
context, but it **costs more compute/money and can reduce precision** if irrelevant material
dilutes the prompt — a capability/cost trade-off, not a free upgrade. *Revisit:* Session 1 §3.

**A12.** *(Techniques)* **Temperature** controls the creativity/randomness of the model's word
choices. Lower it for **factual, deterministic** work — support replies, extraction, code,
compliance, summarisation of official documents. *Revisit:* Session 3 §3.

**A13.** *(Techniques)* **Top-p** controls the cumulative probability pool of the most likely
tokens considered at each step (nucleus sampling) — another randomness/precision dial alongside
temperature. *Revisit:* Session 3 §3.

**A14.** *(Techniques)* Prompt engineering is the deliberate design of model inputs — wording,
structure, examples, constraints, and format — to maximise output quality and consistency
**without changing the model**. *Revisit:* Session 3 §1.

**A15.** *(Techniques)* **One-shot** provides a single example of the desired input→output;
**few-shot** provides several (typically 3–5) so the model infers a pattern, taxonomy, or
style. Few-shot is stronger for consistent formatting and domain-specific labels. *Revisit:*
Session 3 §2.1.

**A16.** *(Techniques)* **Prompt chaining** breaks a complex task into a sequence of prompts,
each feeding the next. It is better than one long prompt when the task is multi-stage, when
steps need different data or tools, or when a human should check intermediate output — it
improves reliability and auditability. *Revisit:* Session 3 §2.1 and §5.

**A17.** *(Techniques)* **Chain-of-thought** prompts the model to work through intermediate
reasoning steps before answering — improving accuracy on maths, logic, planning, and
multi-constraint problems. *Revisit:* Session 3 §2.1.

**A18.** *(Techniques/Offerings)* **ReAct (reason + act)** lets the model reason *and take
action* — calling tools and external systems, then continuing to reason on the result. It is
the bridge from single-turn prompting to **agents**, which need to interact with their
environment to achieve a goal. *Revisit:* Session 3 §2.1 and §5.

**A19.** *(Techniques)* **Grounding** connects model output to verifiable sources of
information. Beyond accuracy, it delivers **auditability** — citable answers, freshness past
the knowledge cutoff, and defensible answers for legal, risk, and compliance review. *Revisit:*
Session 3 §4.

**A20.** *(Techniques)* **First-party/enterprise data** → Agent Search / prebuilt RAG, RAG APIs,
data stores. **Third-party data** → licensed or connected external sources via connectors in
your RAG pipeline. **World data** → **Grounding with Google Search**. *Revisit:* Session 3 §4.1.

**A21.** *(Techniques)* **Retrieval → Augmentation → Generation → Iteration (optional).**
Generation over retrieved content — with source IDs preserved from retrieval — is what makes
answers **auditable**. *Revisit:* Session 3 §4.2.

**A22.** *(Techniques/Strategy)* **HITL** integrates human input and feedback directly into ML
workflows. **Pre-generation review:** experts validate model outputs before deployment so
users are never exposed to errors or bias. **Post-generation review:** continuous human review
after launch so the model improves and adapts. *Revisit:* Session 4 §1.3.

**A23.** *(Strategy)* **Responsible AI** = ensuring AI applications don't cause harm and are
used ethically (fairness, privacy, transparency, accountability, explainability) throughout the
lifecycle. **Secure AI** = protecting AI applications from malicious attacks, misuse, and theft
(threats, access control, resilience). *Revisit:* Session 4 §3.1.

**A24.** *(Strategy)* (1) Expand strong security foundations to the AI ecosystem; (2) extend
detection and response to bring AI into your threat universe; (3) automate defences to keep
pace with threats; (4) harmonise platform-level controls across the organisation; (5) adapt
controls to create faster feedback loops; (6) contextualise AI system risks in the surrounding
business processes. *Revisit:* Session 4 §3.2.

**A25.** *(Strategy)* **Anonymisation** irreversibly removes identifying information.
**Pseudonymisation** replaces identifiers with tokens and keeps a separate mapping key, so
re-identification is possible — meaning **pseudonymised data remains personal data** under many
privacy regimes and must still be protected. *Revisit:* Session 4 §2.1.

---

## Part B — Matching (12 items)

| # | Offering | Answer | Why |
| --- | --- | --- | --- |
| 1 | Agent Assist | **c** | Real-time support for **live human** agents during interactions |
| 2 | Document AI API | **d** | Extracts structured data from documents; automates data capture and document processing |
| 3 | Agent Search | **e** | Enterprise search/recommendation with **prebuilt RAG** over your own content |
| 4 | Grounding with Google Search | **f** | Grounds answers in current **public/world** information |
| 5 | Model Garden | **g** | Catalogue for discovering and using first-party, third-party, and open-source models |
| 6 | Agent Platform AutoML | **h** | Trains custom models with **minimal technical knowledge** |
| 7 | Gems | **i** | Reusable personalised assistants with fixed instructions inside Gemini |
| 8 | Gemini Nano | **j** | On-device/edge model for private, low-latency, offline use (with LiteRT) |
| 9 | Imagen | **a** | Text-to-image diffusion generation and editing |
| 10 | Model Armor | **k** | Screens prompts/responses for injection, jailbreak, and data leakage |
| 11 | Agent Platform Feature Store | **l** | Manages and serves features consistently between training and serving |
| 12 | Customer Experience Insights | **b** | Analytics across all customer conversations |

*Revisit:* Session 2 §7 (master matching table).

---

## Part C — Scenario questions (15 items)

**C1 — Answer: C** *(Techniques/Strategy)* Ground the model on the hospital's own notes with
citations and keep a human in the loop before anything reaches the clinical record. Fine-tuning
on *public* literature wouldn't reflect this hospital's patients (facts come from grounding,
not fine-tuning), raising temperature increases fabrication risk, and writing unreviewed output
into a clinical record removes the accountability control required in a sensitive application.
*Revisit:* Session 4 §1.1 and §4.

**C2 — Answer: D** *(Offerings)* **Gemini Enterprise** with **Agent Search** gives governed
enterprise-wide search and conversation agents over internal sources, and it honours
**IAM-backed permissions** so users only see what they're authorised to see. The Gemini app and
Workspace don't solve cross-system enterprise knowledge, AI Studio is a prototyping tool, and
training a custom model from scratch is unnecessary and doesn't solve permissions. *Revisit:*
Session 2 §2 and §4.3.

**C3 — Answer: A** *(Techniques)* **Few-shot prompting** with labelled examples demonstrating
the taxonomy is the cheapest and fastest fix — it shapes output without touching the model.
Fine-tuning and custom training are expensive and premature. *Revisit:* Session 3 §2.1.

**C4 — Answer: D** *(Techniques)* Ground on a refreshed, citable source — Google Search
grounding for public/current facts and/or a refreshed enterprise RAG index — so the answer is
both current and verifiable. Lowering temperature doesn't add knowledge, chaining doesn't
retrieve anything, and dumping an entire archive into context raises cost while hurting
precision. *Revisit:* Session 3 §4.

**C5 — Answer: C** *(Fundamentals/Offerings)* At 50k conversations a month with sub-second
latency and cost sensitivity, a **Flash/Flash-Lite tier** model is right. The flagship model
would blow the latency and cost budget; a custom-trained model is over-engineering for a
standard support task. *Revisit:* Session 5 §3.1.

**C6 — Answer: B** *(Offerings)* An **extension** connects the agent to external services via
APIs. (Functions define specific actions in your code; data stores provide information; safety
settings filter content.) *Revisit:* Session 2 §5.2.

**C7 — Answer: D** *(Offerings)* A **data store** provides the agent with access to information
so it can ground its answers in the company's policy documents. *Revisit:* Session 2 §5.2.

**C8 — Answer: C** *(Techniques)* Raise **temperature** (and/or top-p) to increase the variety
of generated ideas. *Revisit:* Session 3 §3.

**C9 — Answer: C** *(Techniques)* **Model Monitoring** detects **drift** — here, data/concept
drift as customer behaviour changes. *Revisit:* Session 4 §1.2.

**C10 — Answer: D** *(Strategy)* Value is measured against a **pre-launch baseline** in
business terms (handling time, CSAT), not by benchmark scores, model recency, or project
delivery dates. *Revisit:* Session 5 §5.2.

**C11 — Answer: D** *(Strategy)* Least-privilege **IAM** plus **VPC Service Controls** are
secure-AI controls (protecting systems from attack and misuse). Fairness audits, disclosure,
and explainability are responsible-AI practices. *Revisit:* Session 4 §3.1 and §3.3.

**C12 — Answer: C** *(Strategy)* SAIF's first element deliberately **adapts proven security
foundations** — input sanitisation, IAM, supply-chain practices — to AI systems, rather than
building a parallel programme from scratch or waiting for regulation. *Revisit:* Session 4 §3.2.

**C13 — Answer: D** *(Offerings)* **Agent Assist** supports live human agents in real time.
CX Agent Studio builds customer-facing virtual agents and CX Insights analyses conversations
after the fact. *Revisit:* Session 2 §3.

**C14 — Answer: C** *(Strategy)* **Regional data residency controls** keep data in the
required jurisdiction and **CMEK** puts encryption-key control in the bank's hands. RAG alone
and open models alone don't address residency or key ownership. *Revisit:* Session 4 §3.3.

**C15 — Answer: D** *(Strategy)* High-risk decisions need human judgement over the model's
output: an AI recommendation with **mandatory human review and sign-off** before the decision
takes effect, supported by logging and accountability. Fine-tuning never justifies removing
human oversight for high-consequence decisions. *Revisit:* Session 4 §1.3 and Session 5 §1.

---

## Part D — Spot the flaw (8 items)

**D1.** *(Techniques)* **Flaw:** fine-tuning teaches *behaviour and style*, not fresh facts —
it can still hallucinate and would need retraining every time pricing changes. **Correct:**
use **grounding/RAG** over the current pricing and policy sources so answers stay accurate and
citable; reserve fine-tuning for tone, format, or domain conventions.
*Revisit:* Session 3 §4.3.

**D2.** *(Techniques)* **Flaw:** high temperature increases randomness — unacceptable for
compliance summaries. **Correct:** use **low temperature** for deterministic, faithful output,
with safety settings on and human review for anything consequential.
*Revisit:* Session 3 §3.

**D3.** *(Fundamentals/Offerings)* **Flaw:** Gemma is Google's **open** model family designed
for **customisable, largely local/self-hosted deployments** — it is not the flagship hosted
model. **Correct:** **Gemini** is the flagship family (multimodal, available via Google Cloud
and Google AI Studio); Gemma is chosen for control, local deployment, and cost predictability.
*Revisit:* Session 1 §7 and Session 2 §1.

**D4.** *(Offerings)* **Flaw:** the free prototyping tool is **Google AI Studio**. **Correct:**
**Agent Studio** is for building and deploying **production-ready** AI applications and agents
at scale with enterprise governance. *Revisit:* Session 2 §4.2.

**D5.** *(Strategy)* **Flaw:** SAIF is Google's **security** framework for AI (protecting AI
systems from attacks and misuse). **Correct:** responsible AI covers ethics, fairness,
transparency, and accountability; the two are complementary and should not be conflated.
*Revisit:* Session 4 §3.1 and §3.2.

**D6.** *(Strategy)* **Flaw:** pseudonymised data **can be re-identified** using the mapping
key. **Correct:** pseudonymised data generally remains **personal data** and is still subject
to privacy regulation — protect the key and apply full privacy controls.
*Revisit:* Session 4 §2.1.

**D7.** *(Techniques)* **Flaw:** a larger context window increases **cost** and can reduce
precision by diluting relevance; it is not automatically better. **Correct:** retrieve only the
relevant content (RAG), right-size the model tier, and balance capability against cost —
"more context" is a trade-off, not a free win. *Revisit:* Session 1 §3 and Session 3 §4.2.

**D8.** *(Techniques/Strategy)* **Flaw:** post-deployment review alone means users are exposed
to errors first. **Correct:** use **both** — pre-generation review to validate outputs and
catch bias before launch, and post-generation review to keep improving and adapt after launch.
*Revisit:* Session 4 §1.3.

---

## How to use your score

| Missed items | What to re-read |
| --- | --- |
| Any of A1–A11 | Session 1 in full |
| Any of A6, A7, B1–B12, C2, C6, C7, C13 | Session 2 in full (the largest exam domain) |
| Any of A10–A22, C3, C4, C8, D1, D2, D7 | Session 3 in full |
| Any of A22–A25, C1, C9, C11, C12, C15, D5, D6, D8 | Session 4 in full |
| Any of C5, C10, C14 | Session 5 in full |
| Any item you answered correctly but slowly | [complete-reference.md](complete-reference.md) condensed tables |

Then take the quiz again after 24 hours. Aim for 54+/60 before exam day.
