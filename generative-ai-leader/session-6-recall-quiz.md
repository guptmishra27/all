# Session 6 — Recall Quiz (closed book)

**How to use this file**

1. Close every other file. No notes, no tabs, no search.
2. Set a timer: **60 minutes** for all 60 items. The real exam gives you roughly 90 seconds
   per question, so this is a realistic pace.
3. Write your answers down (paper or a scratch file) — recall beats recognition.
4. Score yourself with [answer-key.md](answer-key.md). Each explanation includes a
   **Revisit** pointer back to the exact session section for anything you miss.
5. **Target: 48/60 (80%)** before you book the exam. Below 80%, re-read the flagged sessions
   and retake this quiz after 24 hours.

**Do not open the answer key until you have written answers to all 60 items.**

---

## Part A — Rapid recall (25 items)

Give a one- or two-sentence answer. Be precise about *why it matters to a business*.

1. Define a **foundation model** and say why businesses rarely train one from scratch.
2. Define a **large language model** and state how it relates to foundation models.
3. What is a **diffusion model**, and which two Google Cloud model families use that approach?
4. Name the three primary ML learning approaches and say which one requires **labeled** data.
5. What is **self-supervised learning**, and why does it matter for foundation models?
6. List the four stages of the **ML lifecycle**, and name one Google Cloud tool for each.
7. Which Google Cloud capability **versions** models, and which one detects **drift**?
8. Distinguish **structured** from **unstructured** data with one example of each, and explain
   which one gen AI unlocks commercially.
9. What does **data accessibility** include, and why is it a business rather than a technical
   problem?
10. What is a **token**, and why do leaders care about token counts?
11. What is a **context window**, and what is the trade-off of making it larger?
12. **Temperature** — what does it control, and when do you lower it?
13. What does **top-p (nucleus sampling)** control?
14. Define **prompt engineering** in one sentence.
15. What is the difference between **one-shot** and **few-shot** prompting?
16. What is **prompt chaining**, and when is it better than one long prompt?
17. What is **chain-of-thought** prompting for?
18. What is **ReAct**, and how does it relate to agents?
19. Define **grounding** and explain the business benefit beyond accuracy.
20. Name the three types of **grounding data** and one Google mechanism for each.
21. List the four steps of **RAG** and say which step makes answers auditable.
22. Define **human in the loop (HITL)** and give one pre-generation and one post-generation
    example.
23. In one line each: **responsible AI** versus **secure AI**.
24. Name the six **SAIF core elements** in short form.
25. What is the difference between **anonymisation** and **pseudonymisation**, and which one
    leaves data still subject to privacy rules?

---

## Part B — Matching (12 items)

Match each Google Cloud offering (1–12) to its intended task (a–l). Each task is used once.

| # | Offering |
| --- | --- |
| 1 | Agent Assist |
| 2 | Document AI API |
| 3 | Agent Search |
| 4 | Grounding with Google Search |
| 5 | Model Garden |
| 6 | Agent Platform AutoML |
| 7 | Gems |
| 8 | Gemini Nano |
| 9 | Imagen |
| 10 | Model Armor |
| 11 | Agent Platform Feature Store |
| 12 | Customer Experience Insights |

| # | Task |
| --- | --- |
| a | Generate images from text descriptions |
| b | Analyse all customer conversations for insight |
| c | Provide real-time help to live human contact-centre agents |
| d | Extract structured data from documents and automate data capture |
| e | Enterprise search and prebuilt RAG over your own content |
| f | Ground answers in current public information |
| g | Discover, compare, and use first-party, third-party, and open-source models |
| h | Train a custom model with minimal technical expertise |
| i | Create reusable, personalised assistants with fixed instructions |
| j | Run generative AI on-device (edge) |
| k | Screen prompts and responses for injection attempts and data leakage |
| l | Manage and serve model features consistently across training and serving |

---

## Part C — Scenario questions (15 items)

Choose the **best** answer. These mirror the real exam's style: a short business situation
with four plausible options.

**C1.** A hospital wants clinicians to summarise patient notes. Accuracy is critical and
errors could affect care. What is the most appropriate approach?
- A. Fine-tune a model on public medical literature and deploy it without further review
- B. Raise the temperature so the model produces richer summaries
- C. Ground the model on the hospital's own notes with citations, and add human review before
  anything reaches the clinical record
- D. Generate summaries and write them directly into the patient record to save time

**C2.** A company's employees cannot find answers spread across 12 internal systems, and
legal requires that users only see documents they are permitted to see. What should you
propose?
- A. Gemini for Google Workspace for everyone
- B. Google AI Studio
- C. A custom model trained from scratch on data from all 12 systems
- D. Gemini Enterprise with Agent Search and IAM-backed permissions

**C3.** A team's prompt returns inconsistent category labels. What is the cheapest, fastest
first fix?
- A. Add few-shot examples that demonstrate the exact taxonomy
- B. Fine-tune the model
- C. Train a custom model
- D. Increase the maximum output length

**C4.** An assistant is asked about a regulation that changed last week, and the answer must
be verifiable. What is the best fix?
- A. Lower the temperature
- B. Use prompt chaining
- C. Paste the entire regulatory archive into the context window
- D. Ground responses on a refreshed, citable source (Google Search grounding and/or a
  refreshed enterprise RAG index)

**C5.** A support chatbot handles 50,000 conversations a month and must reply in under a
second, with tight cost control. Which model tier fits best?
- A. The largest flagship reasoning model
- B. A custom-trained model on dedicated silicon
- C. A Flash / Flash-Lite tier model
- D. A video-generation model

**C6.** An agent must call a third-party logistics provider's service over its API to get
live shipment status. Which agent capability is required?
- A. A safety setting
- B. An extension (connecting the agent to external services via APIs)
- C. A prompt template
- D. A larger context window

**C7.** An agent must answer from the company's internal policy documents. Which agent
capability provides that?
- A. A plugin that changes the agent's personality
- B. A higher temperature setting
- C. Model Registry
- D. A data store

**C8.** A marketing team wants 50 diverse tagline options. Which sampling parameter should
you raise?
- A. Output length only
- B. Safety settings
- C. Temperature (and/or top-p)
- D. Nothing — leave the defaults

**C9.** Six months after launch, a model's predictions have quietly become less accurate
because customer behaviour changed. Which capability detects this, and what is the phenomenon
called?
- A. Model Registry; it is called versioning
- B. Security Command Center; it is called a finding
- C. Model Monitoring; it is called drift
- D. Feature Store; it is called skew

**C10.** Which statement best demonstrates **measurable** business value for a gen AI pilot?
- A. "The model scored 0.91 on our internal benchmark"
- B. "We deployed on the newest model available"
- C. "The pilot was completed on time"
- D. "Average handling time fell from 9 to 5 minutes with CSAT unchanged, measured against a
  pre-launch baseline"

**C11.** Which of these is a **secure AI** control rather than a responsible AI practice?
- A. A fairness audit across customer segments
- B. A published disclosure that AI is being used
- C. An explainability note for each decision
- D. Least-privilege IAM roles plus a VPC Service Controls perimeter

**C12.** Which activity best expresses the SAIF core element *"expand strong security
foundations to the AI ecosystem"*?
- A. Build a completely separate AI security programme that ignores existing controls
- B. Wait for regulators to publish AI-specific rules before implementing anything
- C. Adapt proven controls — input sanitisation, IAM, supply-chain practices — to AI systems
- D. Rely solely on the model provider's safety filters

**C13.** Contact-centre leadership wants to support **live human agents** with real-time
suggestions during calls. Which offering?
- A. Customer Experience Agent Studio
- B. Customer Experience Insights
- C. Google AI Studio
- D. Agent Assist

**C14.** A European bank must keep data inside the EU and manage its own encryption keys.
Which combination of controls addresses this?
- A. Higher temperature and longer output
- B. Prebuilt RAG alone
- C. Regional data residency controls plus customer-managed encryption keys (CMEK)
- D. Model Garden's open models, with no additional configuration

**C15.** Which design is most appropriate for a high-risk decision such as approving a large
credit line?
- A. Full automation with high temperature for flexibility
- B. Fine-tuning the model until it is perfect, then removing human review
- C. Batch processing overnight with no human oversight
- D. An AI-generated recommendation with mandatory human review and sign-off before the
  decision takes effect

---

## Part D — Spot the flaw (8 items)

Each statement below is **wrong in an important way**. State the flaw and give the correct
version.

**D1.** "Fine-tuning is the best way to teach the model our latest pricing and policies."
**D2.** "For compliance summarisation, raise the temperature so the model produces richer
answers."
**D3.** "Gemma is Google's flagship hosted model, available only through Google Cloud APIs."
**D4.** "Agent Studio is Google's free tool for quick prompt prototyping."
**D5.** "SAIF is Google's responsible-AI ethics framework, covering fairness and transparency."
**D6.** "Because data has been pseudonymised, it can no longer identify anyone and is out of
scope for privacy regulation."
**D7.** "A bigger context window always improves answer quality and reduces cost."
**D8.** "Post-generation human review after launch is sufficient; no pre-launch human
validation is needed."

---

## Scoring

| Score | Interpretation | Next step |
| --- | --- | --- |
| 54–60 | Exam-ready on recall | Do a full reference sweep: [complete-reference.md](complete-reference.md) and [final-exam-mindset.md](final-exam-mindset.md) |
| 48–53 | Solid, with gaps | Re-read the sessions flagged in the answer key, retake the quiz in 24 hours |
| 40–47 | Not yet | Re-read Sessions 1–2 in full (65% of the exam), then Sessions 3–5, then retake |
| Below 40 | Start again | Work the sessions in order with the self-checks, then retake |

**Domain-by-domain check:** tally your misses by domain using the answer key's labels
(Fundamentals · Offerings · Techniques · Strategy). If one domain is under 70%, that's your
next study block — the exam weights are 30% / 35% / 20% / 15%.
