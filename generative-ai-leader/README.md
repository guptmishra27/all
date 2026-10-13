# Generative AI Leader — Complete Study Reference

A self-contained, six-session study program plus a complete reference for the
**Google Cloud Certified Generative AI Leader** exam.

> **Version:** October 2026 · aligned to the current official exam guide and study guide
> (including the 2026 product-branding changes — see [Naming changes](#naming-changes-you-must-know)).

---

## Start here

| If you want to… | Open |
| --- | --- |
| Understand the exam and follow the 6-session plan | this page |
| Session 1 — Fundamentals: AI, ML, DL, FMs, LLMs, data, ML lifecycle | [session-1-fundamentals.md](session-1-fundamentals.md) |
| Session 2 — Google Cloud offerings, matched to tasks | [session-2-google-cloud-offerings.md](session-2-google-cloud-offerings.md) |
| Session 3 — Prompting, grounding, and RAG (with practice) | [session-3-prompting-and-rag.md](session-3-prompting-and-rag.md) |
| Session 4 — Limitations, responsible AI, and secure AI | [session-4-limitations-and-responsible-ai.md](session-4-limitations-and-responsible-ai.md) |
| Session 5 — Business strategy, model selection, measurable value | [session-5-business-strategy.md](session-5-business-strategy.md) |
| Session 6 — Recall quiz (no answers in the file) | [session-6-recall-quiz.md](session-6-recall-quiz.md) |
| Scenario-question decision framework for exam day | [final-exam-mindset.md](final-exam-mindset.md) |
| Glossary, master mapping tables, cheat sheets | [complete-reference.md](complete-reference.md) |
| Quiz answers with explanations and remediation links | [answer-key.md](answer-key.md) |

**How to use it:** read one session file per sitting. Each session ends with an
*Exam traps* box and a short *Rapid self-check* with answers at the bottom of the
file. Do Session 6 (the quiz) **closed-book** first, mark it, then use the remediation
links in the answer key to revisit only the weak areas. Finish with the
complete reference as a last-pass revision before exam day.

---

## Exam facts

| Item | Detail |
| --- | --- |
| Certification | Google Cloud Certified Generative AI Leader (no prerequisites) |
| Length / format | 90 minutes · 50–60 multiple-choice questions |
| Delivery | Online-proctored or test-center proctored |
| Fee | $99 (plus tax where applicable) |
| Validity | 3 years (renewal exam available inside the renewal window) |
| Languages | English, Japanese, Spanish, Portuguese |
| Audience | Business and technical professionals who must *influence* gen AI adoption — conceptual, not implementation-level |

### Official blueprint and how it maps to these sessions

| Domain | Weight | Covered in |
| --- | --- | --- |
| 1. Fundamentals of gen AI | ~30% | Session 1 (plus model theory in Sessions 3 and 5) |
| 2. Google Cloud's gen AI offerings | ~35% | Session 2 |
| 3. Techniques to improve gen AI model output | ~20% | Sessions 3 and 4 |
| 4. Business strategies for a successful gen AI solution | ~15% | Sessions 4 and 5 |

The **largest single block of marks is Google Cloud's offerings (~35%)**, and roughly
**two-thirds of the exam (65%) sits in Domains 1 and 2** — concepts + product matching.
Techniques, responsible AI, and strategy are the remaining third, and they mostly appear
as *scenario* questions ("what should the leader do next?"). Budget your study time
in roughly that ratio.

---

## Suggested study plan

| Session | Focus | Time | Deliverable for you |
| --- | --- | --- | --- |
| 1 | Fundamentals in plain words | 60–90 min | Explain AI → ML → DL → FM → LLM and the ML lifecycle out loud |
| 2 | Google Cloud offerings → task matching | 90–120 min | Be able to route any use case to the right product without notes |
| 3 | Prompting, grounding, RAG (hands-on) | 60–90 min | Rewrite one real prompt 4 ways; sketch one RAG flow |
| 4 | Limitations, responsible AI, secure AI | 60–90 min | Write your own "limitation → mitigation → control" table from memory |
| 5 | Business strategy and value | 60 min | Build a 5-line business case with a baseline metric and a KPI |
| 6 | Closed-book quiz + remediation | 60–90 min | Score ≥ 80% on the recall quiz without notes |
| Final | Full reference sweep + exam mindset | 30–45 min | Read [final-exam-mindset.md](final-exam-mindset.md) twice |

Pair the reading with the official free **Cloud Skills Boost "Generative AI Leader"
learning path** and the official **sample questions**, then take the real exam.

---

## The five ideas the whole exam is built on

If you remember nothing else:

1. **Value verbs.** Gen AI creates value by helping you **create, summarize, discover,
   and automate** — map every scenario to one of those four verbs.
2. **Right tool, right layer.** Match the need to the layer: **application** (Gemini app,
   Gemini for Workspace, Gemini Enterprise), **platform** (Agent Platform, Agent Studio,
   AI Studio), **model** (Gemini, Gemma, Imagen, Veo), **agent + tools**, or **API**.
3. **Ground it.** Hallucinations and knowledge cutoff are the default failure modes;
   **grounding, RAG, and Google Search grounding** are the default fixes. Fine-tuning
   changes *behavior*, grounding changes *facts*.
4. **Humans stay in the loop.** High-stakes decisions need **HITL**, monitoring, and
   evaluation — plus **SAIF**, **IAM**, and **Security Command Center** on the security side.
5. **Business goal first.** On scenario questions, identify the business goal, then the
   constraint (privacy, latency, cost, modality, risk), *then* the product and the control.

---

## Naming changes you must know

Google renamed several products, and the exam was explicitly updated to reflect the new
branding. The exam may still use either form, so learn both columns.

| Older name (may still appear) | Current name (as used in the latest official materials) |
| --- | --- |
| Vertex AI | **Gemini Enterprise Agent Platform** (often shortened to **Agent Platform**) |
| Vertex AI Studio | **Agent Studio** |
| Vertex AI Search / Vertex AI Search and Conversation | **Agent Search** |
| Agentspace | **Gemini Enterprise** |
| NotebookLM | **Gemini Notebook** |
| Vertex AI Agent Engine | **Agent Runtime** (part of Agent Platform) |
| Customer Engagement Suite / Conversational Agents / Conversational Insights | **Gemini Enterprise for Customer Experience** — **Customer Experience (CX) Agent Studio**, **Agent Assist**, **Customer Experience Insights** |

> Google AI Studio is a *different* product from Agent Studio, and the exam tests the
> difference. **Google AI Studio = free, quick prototyping with the Gemini API.
> Agent Studio = building and deploying production-grade AI applications and agents.**

---

## Source of truth

This guide consolidates and explains, in plain language:

- The official *Generative AI Leader* certification exam guide and study guide.
- Google Cloud product documentation for Agent Platform, Agent Search, Gemini,
  Gemini Enterprise, Google AI Studio, the Cloud AI APIs, and SAIF.
- Google's published AI Principles and the Secure AI Framework (SAIF).

Product lineups and model versions change quickly. The exam tests the **patterns** —
which category of model or service solves which class of problem — far more than
version numbers. Where a specific version is named here, treat it as an illustration
and confirm the current lineup before you quote it to a customer.
