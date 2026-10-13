# Session 3 — Prompting, Grounding, and RAG (with practice)

**Exam domains:** 3. Techniques to improve gen AI model output (~20%, shared with Session 4)
· objective 3.2 (prompt engineering) and 3.3 (grounding techniques)
**Goal of this session:** know *which* prompting technique or grounding approach a scenario
calls for, and be able to write the prompts yourself. Practice beats memorisation here — the
worked examples below are the same shapes the exam describes.

---

## 1. Prompt engineering in plain words

**Prompting** is simply how you interact with a foundation model: you give it instructions
or inputs, and it generates output.

**Prompt engineering** is the art and science of crafting those inputs deliberately — so the
output is accurate, on-format, on-brand, and repeatable — and of tailoring a single model to
many needs **without changing the model itself**.

Why it matters to a business: prompt engineering is the **cheapest, fastest lever** you have.
One well-engineered prompt can raise quality, cut rework, reduce token spend, and make
output consistent enough to automate downstream. It is also the first thing to try before
you spend money on fine-tuning.

**Anatomy of a good prompt (a checklist you can reuse):**

| Element | Purpose | Example fragment |
| --- | --- | --- |
| **Role / persona** | Sets expertise, voice, and frame | "You are a senior insurance claims analyst…" |
| **Task** | The single, unambiguous ask | "…summarise the policy exclusions…" |
| **Context** | Background the model needs | "…for an adjuster deciding on claim #4471…" |
| **Input data** | The material to work on (and where it sits) | "…using only the attached policy text…" |
| **Constraints** | Boundaries, rules, what to avoid | "…do not speculate; if the text is silent, say 'not specified'." |
| **Format** | Exact output shape | "…return a table with columns: Exclusion, Section, Impact." |
| **Examples** | Show, don't just tell (few-shot) | "…for example: …" |
| **Length/tone** | Style control | "…maximum 150 words, plain English, no jargon." |

---

## 2. Prompting techniques and when to use them (objective 3.2)

### 2.1 The core techniques

| Technique | What it is | Use when | Worked example |
| --- | --- | --- | --- |
| **Zero-shot** | Ask for the task with **no examples** — rely on the model's general capability | Simple, common, well-understood tasks; quick drafts | "Classify this support ticket as Billing, Technical, or Refund." |
| **One-shot** | Give **one** example of the desired input→output | The format is unusual or you want a specific style, but examples are scarce | "Ticket: 'charged twice' → Billing. Now classify: 'app crashes on upload' →" |
| **Few-shot** | Give **several** examples (typically 3–5) so the model infers the pattern | Consistent formatting, domain-specific labels, edge-case handling, tone matching | Three labelled tickets, then the new one — the model copies your pattern and taxonomy |
| **Role prompting** | Assign a **persona** to influence style, tone, depth, and focus | You need domain voice or audience-appropriate framing | "You are a CFO writing to the board: concise, numbers-first, no marketing language." |
| **Prompt chaining** | Break a complex job into **a sequence of prompts**, each feeding the next | Multi-step work where a single mega-prompt would be unreliable, or different steps need different data/checks | Step 1 extract clauses → Step 2 compare against policy → Step 3 draft a plain-language summary |
| **Chain-of-thought (CoT)** | Guide the model through **intermediate reasoning steps** before the answer | Maths, multi-constraint logic, planning, diagnosis — anything where "show your work" improves accuracy | "Work through the calculation step by step before giving the final number." |
| **ReAct (reason + act)** | Let the model **reason and take action** — call tools, look things up, then continue reasoning | Agents, live data lookups, anything requiring interaction with systems | "Think about what you need, call the order-lookup tool, then answer the customer." |
| **Metaprompting** | Use prompting to have the model **generate, modify, or interpret other prompts** | Scaling prompt creation, standardising prompt quality across teams, building prompt templates | "Write five variations of this prompt for different reading levels and critique them." |

### 2.2 Choosing the technique — the exam's decision tree

1. **Is the task simple and common?** → **Zero-shot**.
2. **Does the output need a specific format or taxonomy?** → **One-shot / few-shot**.
3. **Does the voice, depth, or expertise level matter?** → **Role prompting**.
4. **Is the task multi-stage or does it need verification between steps?** → **Prompt chaining**.
5. **Does the task need reasoning (maths, logic, planning)?** → **Chain-of-thought**.
6. **Must the model use tools or live systems?** → **ReAct** (this is the bridge to agents).
7. **Are you generating prompts at scale rather than answers?** → **Metaprompting**.

### 2.3 Streamlining prompting workflows

| Practice | What it does | Why it matters |
| --- | --- | --- |
| **Reusable prompt templates** | Save prompts as templates for repeated use | Consistency across teams and turns; faster onboarding |
| **Prompt chaining in a conversation** | Continue in the same chat to preserve context | Avoids re-supplying context; keeps continuity |
| **Saved info / stored context** | Persist facts the model should always know | Consistent behaviour without repeating yourself |
| **Gems** | Personalised assistants with fixed instructions and knowledge | Turns a good prompt into a reusable "colleague" — no code required |

> **Exam cue:** "The team keeps re-typing the same long prompt with inconsistent results" →
> **prompt templates + Gems**. "The task is too complex for one prompt" → **prompt
> chaining**. "We need the team to produce good prompts quickly" → **metaprompting**.

---

## 3. Sampling parameters: controlling model behaviour (objective 3.3)

These are the dials on the model. The exam tests *direction* and *when to use which setting*.

| Parameter | What it controls | Turn it **down** when… | Turn it **up** when… |
| --- | --- | --- | --- |
| **Token count** | The meaningful chunks of text (words/punctuation pieces) the model reads or writes — basis for cost and limits | You need lower cost/latency | You need longer inputs or outputs (watch cost) |
| **Temperature** | The "creativity"/randomness of word choices | **Factual answers, extraction, support replies, code, compliance** — you want determinism | **Brainstorming, marketing copy, naming, ideation** — you want variety |
| **Top-p (nucleus sampling)** | The cumulative probability pool of the most likely tokens considered at each step — another randomness control | Precision tasks | Creative exploration (use temperature *or* top-p as your main dial, not both aggressively) |
| **Output length / max output tokens** | The maximum length of generated text | You need terse summaries or cheaper responses | You need full reports or long documents |
| **Safety settings** | Filters that block or reduce potentially harmful/inappropriate content | Never removed in a consumer-facing or regulated deployment | Only tuned with governance approval, documented, and tested |

**Preset logic you can quote in a scenario:**

- **Customer support / compliance / data extraction:** low temperature, tight output length, safety settings on, grounding on.
- **Creative campaign ideation:** higher temperature, generous output length, human review downstream.
- **Real-time chat:** smaller max output tokens for snappy responses and predictable cost.

---

## 4. Grounding: connecting output to verifiable sources (objective 3.3)

**Grounding** means connecting the model's output to **verifiable sources of information**, so
the answer is anchored in evidence rather than the model's memory. Grounding is Google's
primary recommended answer to two of the biggest foundation-model limitations:
**hallucination** and the **knowledge cutoff**.

### 4.1 Three kinds of grounding data — know the difference

| Grounding source | What it means | Example | Google Cloud mechanism |
| --- | --- | --- | --- |
| **First-party (enterprise) data** | *Your* private content: documents, tickets, wikis, databases, sites, contracts | "What's our refund policy for enterprise customers?" answered from the actual policy | **Agent Search / prebuilt RAG**, **RAG APIs**, data stores |
| **Third-party data** | Data licensed or sourced from outside providers, or federated enterprise systems you connect to | Industry benchmarks, partner catalogues, connected SaaS records | Connectors/data stores inside your RAG pipeline |
| **World data** | Public, current information from the open web | "What did the regulator announce this morning?" | **Grounding with Google Search** |

**Why this matters commercially:** grounding converts a plausible-sounding assistant into an
**auditable** one. You can point to the source, cite it, and update it — which is exactly what
risk, legal, and audit teams ask for.

### 4.2 The RAG pipeline — four steps

**Retrieval-augmented generation (RAG)** = retrieving relevant information from external
sources and putting it into the prompt so the model generates a grounded answer.

| Step | What happens | Leader-level talking point |
| --- | --- | --- |
| **1. Retrieval** | The system searches external sources (vector databases, indexes, documents) for content relevant to the query | Your content must be indexed, fresh, and permission-aware |
| **2. Augmentation** | The retrieved content is inserted into the prompt alongside the user's question | Context window and ranking quality decide answer quality and cost |
| **3. Generation** | The model produces a response **based on the retrieved context** | You can require citations and reject unsupported claims |
| **4. Iteration (optional)** | The model may refine its search, retrieve again, and improve the answer | Improves multi-hop questions; adds latency and cost — a real trade-off |

**How RAG changes the generated output:** it shifts answers from *plausible from memory* to
*supported by retrieved evidence*, reduces hallucination, adds freshness past the knowledge
cutoff, enables citations, and lets you apply **access control** so users only see what
they're allowed to see.

### 4.3 Grounding vs fine-tuning vs prompting — the exam's favourite confusion

| Approach | Changes | Fixes | Doesn't fix | Cost/time |
| --- | --- | --- | --- | --- |
| **Prompt engineering** | The input | Format, tone, simple reliability | Missing knowledge | Minutes |
| **Grounding / RAG** | The context | **Hallucination, freshness, citations, access control** | Behaviour/style at depth | Hours–days |
| **Fine-tuning** | The model | **Style, format, domain conventions, narrow task skill** | **Current facts** — it can still hallucinate; needs retraining to stay fresh | Days–weeks |

> **One-liner for the exam:** *Facts come from grounding. Behaviour comes from fine-tuning.
> Cheap wins come from prompting.*

---

## 5. Practice: one task, four techniques

Take a realistic task and watch how the technique changes the prompt and the result.

**Business task:** *A telecom company wants a weekly digest of customer complaints by
category, with severity, from raw ticket text.*

**Zero-shot**
> "Summarise these customer complaints by category."

*Result:* generic, inconsistent categories, no severity. Fine for a first look; not
production-grade.

**Few-shot**
> "Categorise each complaint using these categories: Network, Billing, Device, Support.
> Examples:
> 'no signal at home since Tuesday' → Network
> 'charged twice this month' → Billing
> 'phone battery drains in an hour' → Device
> Now categorise: 'the app logs me out constantly' →"

*Result:* consistent taxonomy, predictable labels. **Use when format and consistency matter.**

**Role prompting**
> "You are a telecom customer-experience analyst preparing a board-level weekly digest.
> Be concise, quantify where possible, and flag emerging trends."

*Result:* executive-appropriate tone and framing. **Use when the audience shapes the answer.**

**Prompt chaining + chain-of-thought**
> Prompt 1: "Extract each complaint and its stated issue."
> Prompt 2: "Classify each extracted issue and assign severity (Low/Medium/High) with a
> one-line reason."
> Prompt 3: "Produce a digest: top three categories, counts, severity mix, and one
> recommended action per category."

*Result:* traceable, verifiable, higher quality — and each step can be checked by a human.
**Use when a single prompt would be unreliable or unauditable.**

**Grounding / RAG added**
> "Use only the retrieved ticket records and the current policy document. Cite the ticket ID
> for every claim. If the data doesn't support a statement, say so."

*Result:* no invented categories, every claim traceable, policy claims current. **Use when
accuracy and auditability are non-negotiable.**

**ReAct (when it becomes an agent)**
> "Reason about what you need. Call the ticket-search tool for the last 7 days, then the
> policy-lookup tool for current SLAs. Then produce the digest."

*Result:* the model pulls live data instead of relying on what's in the prompt. **This is the
bridge from prompting to agents.**

---

## Exam traps in this session

1. **Grounding vs fine-tuning** — grounding adds facts; fine-tuning changes behaviour. If a
   scenario wants *current, citation-backed answers*, pick grounding/RAG.
2. **RAG is not just "a big context window."** RAG retrieves *relevant* content; stuffing the
   whole corpus in raises cost and hurts precision.
3. **Few-shot ≠ fine-tuning.** Examples in the prompt change nothing about the model.
4. **Temperature direction.** Support/claims/extraction scenarios want **low** temperature;
   creative scenarios want **higher**.
5. **Prompt chaining vs chain-of-thought.** Chaining = multiple prompts/steps (often with
   different data or human checks). CoT = reasoning steps inside the response.
6. **World data vs enterprise data.** "Latest news/public info" → Google Search grounding.
   "Our policy/our catalogue" → enterprise RAG.
7. **Top-p and temperature are both randomness controls.** If a question says "reduce
   randomness," both are valid levers; choose based on what the scenario emphasises.
8. **Safety settings are governance decisions**, not performance tuning.

## Rapid self-check

1. Name four prompting techniques and one situation each is best for.
2. What are the four steps of RAG, and which one makes answers *auditable*?
3. Your team says the assistant invents policy details. Name the two best fixes, in order.
4. A branding team wants 50 tagline options. Which sampling parameter do you raise, and why?
5. What does ReAct add over plain chain-of-thought?
6. What's the difference between grounding on first-party, third-party, and world data — with
   one Google Cloud mechanism for each?

### Answers

1. **Zero-shot** — simple, common tasks; **few-shot** — enforcing a format/taxonomy;
   **role prompting** — audience-appropriate voice; **prompt chaining** — complex multi-step
   work needing checks; (**chain-of-thought** — reasoning tasks; **ReAct** — tool use).
2. **Retrieval → Augmentation → Generation → Iteration (optional)**. Generation over retrieved
   context (with citations) is what makes output auditable — supported by the retrieval step
   that preserves source IDs.
3. **Grounding/RAG on the policy documents first** (fast, factual, citable), then consider
   fine-tuning only if the *behaviour/format* is still wrong — never fine-tuning alone for
   facts.
4. **Temperature** (and/or top-p) — higher values increase diversity of ideas; output length
   should also be generous enough to return many options.
5. **Tool use / actions.** CoT reasons in the response; ReAct reasons *and* acts on external
   systems (search, APIs, databases), then continues reasoning.
6. **First-party** = your private content (Agent Search / prebuilt RAG, data stores);
   **third-party** = externally sourced/licensed or connected systems' data (connectors in
   your RAG pipeline); **world** = public current web knowledge (**Grounding with Google
   Search**).

---

**Next:** [Session 4 — Limitations and responsible AI](session-4-limitations-and-responsible-ai.md)
