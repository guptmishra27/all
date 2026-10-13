# Session 1 — Fundamentals: AI, ML, Deep Learning, Foundation Models, LLMs, Data, and the ML Lifecycle

**Exam domain:** 1. Fundamentals of gen AI (~30% of the exam)
**Covers objectives:** 1.1, 1.2, 1.3, 1.4
**Goal of this session:** explain every core term in your own words, and connect each
concept to a *business* implication — the exam never asks for a dictionary definition in
isolation; it asks what a concept means for a business decision.

---

## 1. The family tree: AI → ML → Deep Learning → Generative AI

Think of nested circles. Each inner circle is a more specialised way of delivering the
outer one.

| Term | Plain-language explanation | Everyday example | Exam cue |
| --- | --- | --- | --- |
| **Artificial intelligence (AI)** | Building machines that perform tasks that normally need human intelligence: learning, reasoning, problem-solving, perception, decision-making. AI is the umbrella. | A rules-based system that routes insurance claims by fixed if/then logic | "Umbrella term." Every ML system is AI; not every AI system is ML. |
| **Machine learning (ML)** | A subfield of AI where the machine **learns patterns from data** instead of being given hand-written rules, then uses those patterns to predict or classify. | A model that predicts which customers will churn | Data-driven, not rule-driven. |
| **Deep learning (DL)** | A subset of ML that uses **artificial neural networks with many layers** to extract complex patterns from data — images, audio, language — that simpler methods miss. | Face recognition, speech transcription | "Many-layered neural networks." Needs more data and compute. |
| **Generative AI (gen AI)** | An application of ML (specifically deep learning) that **creates new content** — text, images, audio, video, code — rather than only predicting a label or number. | Drafting a marketing email, generating a product image | Output is *new content*, and it can be **multimodal**. |
| **Natural language processing (NLP)** | The broader field of getting computers to work with human language: classify, extract, translate, summarise, converse. | Sentiment analysis, entity extraction, translation | NLP is the *task family*; LLMs are one modern way to do it. |
| **Foundation model (FM)** | A very large model **pre-trained on massive, broad (mostly unlabeled) data** that develops a general understanding of the world and can be adapted to many downstream tasks. | A base Gemini or Gemma model | "Foundation" = general-purpose starting point, adaptable. |
| **Large language model (LLM)** | A type of foundation model specialised for **understanding and generating human language** (text, and often code). | A chat model that writes and edits text | LLM ⊂ foundation models. |
| **Multimodal foundation model** | A foundation model that natively handles **more than one modality** — e.g., text + images + audio + video in, and one or more out. | Ask about a photo and get a written answer | Multimodality is a primary model-selection criterion. |
| **Diffusion model** | A generative model that starts from random noise and iteratively **denoises** it into a coherent image or video guided by your prompt. | Imagen generating a product shot; Veo generating a video | Signature image/video generation technique; contrast with LLMs for text. |

**Why a leader cares:** the nesting tells you how to spend. AI strategy without data is
aspiration; ML without quality data fails; gen AI inherits every one of those
dependencies *plus* new ones (hallucination, grounding, safety).

---

## 2. How models learn: the three primary approaches

| Approach | Plain-language explanation | Data it needs | Business examples | Exam cue |
| --- | --- | --- | --- | --- |
| **Supervised learning** | Learns from **labeled** examples — input paired with the correct answer — to predict the answer for new inputs. | Labeled data (expensive to create) | Spam detection, demand forecasting, document classification | "Right answers provided." |
| **Unsupervised learning** | Finds **natural groupings and patterns** in data with no labels. | Unlabeled data | Customer segmentation, anomaly detection, topic discovery | "No right answers given — find structure." |
| **Reinforcement learning (RL)** | Learns by **interaction and feedback**, taking actions to maximise reward and minimise penalty. | An environment + a reward signal | Robotics, game-playing agents, ad bidding, some agent/alignment training | "Trial, error, and reward." |

**Plus the technique that made foundation models possible:** **self-supervised
learning** — the model manufactures its own training signal from raw data (for example,
predict the next token). That is how a foundation model can learn from vast *unlabeled*
text with no humans labelling it.

**Labeled vs unlabeled data**

| | Labeled data | Unlabeled data |
| --- | --- | --- |
| Definition | Has tags/annotations: a name, class, or number attached | Raw, untagged information with no meaning attached by itself |
| Example | 10,000 support tickets tagged "refund" / "technical" / "billing" | 10 million raw call recordings |
| Used by | Supervised learning | Unsupervised and self-supervised learning; also the pretraining phase of FMs |
| Business trade-off | Accurate but slow and costly to produce; may need human experts | Abundant and cheap, but needs sophisticated techniques to extract value |

---

## 3. Foundation models and LLMs: what makes them special

**Four characteristics to remember about foundation models:**

1. **Trained on diverse, massive data** — broad world knowledge, not one narrow domain.
2. **Flexible across many use cases** — one base model can summarise, classify, draft, extract, translate.
3. **Adaptable to specialised domains** through additional targeted training (fine-tuning), tuning, or prompting.
4. **Capital-intensive to build** — very few organisations train their own; most *consume and adapt*.

**Prompting vs prompt engineering vs prompt tuning vs fine-tuning** — the exam loves this distinction:

| Activity | What you change | Effort | Best for |
| --- | --- | --- | --- |
| **Prompting** | Nothing — you just give the model instructions or inputs and read the output | Minutes | Everyday use |
| **Prompt engineering** | The wording, structure, examples, and decomposition of the **input** | Minutes to hours | Getting reliable, higher-quality output from a model you don't touch |
| **Prompt tuning / fine-tuning** | The **model** (adds or adjusts trainable parameters) | Days to weeks, needs data and ML skills | Teaching consistent behaviour, tone, domain conventions, or a narrow task |
| **Grounding / RAG** | The **context** you supply at inference time | Hours to days | Correcting facts, freshness, and traceability (see Session 3) |

> **Rule of thumb:** try prompts → then grounding → then fine-tuning. Fine-tuning is the
> most expensive lever and is the *worst* way to add facts.

**Tokens, context window, and output length**

- A **token** is a meaningful chunk of text — roughly a word-piece or a punctuation mark.
  Cost, limits, and latency are all measured in tokens, not characters.
- The **context window** is how much text (prompt plus conversation plus retrieved
  documents) the model can consider at once. A large context window lets you supply long
  documents, but it costs more compute and money — the exam frames this as a
  **trade-off between capability and cost**, not a free win.
- Current Gemini models work at roughly a **1M-token context window** with tens of
  thousands of tokens of output. Treat exact figures as illustrative and check the
  current model card.

---

## 4. Data types and their business implications (objective 1.2)

Data is information in any form: numbers, dates, text, images, audio, video, sensor
readings. Gen AI's usefulness is bounded by it.

### 4.1 Structured vs unstructured

| | Structured data | Unstructured data |
| --- | --- | --- |
| Definition | Organised, highly searchable, fits neatly into rows and columns; often in relational databases | No predefined structure; needs sophisticated analysis techniques |
| Examples | Transactions, inventory counts, CRM fields, financial ledgers, clickstreams | Emails, contracts, call recordings, PDFs, images, video, chat logs, tickets |
| Business implication | Easy to query, report on, and train tabular models with; already governed | Holds the **majority of enterprise value** and is exactly what gen AI unlocks — summarising contracts, mining calls, searching documents |
| Gen AI role | Feeds analytics, forecasting, personalisation features, and RAG metadata filters | The prime fuel and the prime target of gen AI: summarise, extract, classify, search |

**Key insight:** roughly **80% of enterprise data is unstructured**, and it has historically
been the hardest to exploit. Gen AI's biggest business promise is turning that dormant
archive into a searchable, summarisable, conversational asset — which is why
**prebuilt RAG with Agent Search** (Session 2) matters commercially.

### 4.2 Data quality and accessibility

| Dimension | The question to ask | If it's weak… |
| --- | --- | --- |
| **Accuracy** | Is the data correct? | The model confidently repeats wrong facts |
| **Completeness** | Are records and fields present? | Gaps become blind spots and biased outputs |
| **Consistency** | Do definitions and formats agree across systems? | The same question returns different answers |
| **Relevance** | Does this data actually inform the use case? | Noise dilutes retrieval and wastes context |
| **Availability / accessibility** | Can teams and models reach it, in the right format, at a workable cost? | Projects stall in integration, not in modelling |
| **Timeliness** | Is it fresh enough for the decision? | Knowledge-cutoff-style failures in RAG (stale answers) |

> **Exam framing:** "Garbage in, garbage out" is real, but the exam's favourite version is
> **data quality and accessibility are prerequisites** — a data strategy and governance
> come before the shiny model. When a scenario says "pilot results are inconsistent," the
> mature answer is usually *fix data quality/coverage first*, not *buy a bigger model*.

### 4.3 Data and modality — what practitioners call the "4 Vs" trap

Watch for questions mixing these up:

- **Volume** — how much data (affects feasibility and cost).
- **Velocity** — how fast it arrives (affects architecture: batch vs streaming).
- **Variety** — how many forms (structured/unstructured; text/image/audio/video).
- **Veracity** — how trustworthy it is (quality dimensions above).

The exam tests **variety** and **veracity** most often, because those drive *which model*
and *which tool* you choose.

---

## 5. The ML lifecycle (objective 1.1)

Four stages in the official framing — with two "data" phases bundled into the first.
Learn this as a cycle, not a line: deployment feeds monitoring, monitoring feeds the next
round of data and retraining.

| Stage | What actually happens | Why a leader cares | Example Google Cloud tools |
| --- | --- | --- | --- |
| **1. Data ingestion and preparation** | Collect, clean, label, transform raw data into a usable format; govern and catalogue it | Most of the project's time and risk live here; quality problems are cheapest to fix now | Cloud Storage, BigQuery, Pub/Sub, Dataflow, Dataproc, Dataplex (governance) |
| **2. Model training** | Create the model from data — from prompting/fine-tuning a foundation model, to AutoML, to fully custom training | Decides the cost/skill trade-off: use pre-trained, tune, or build | Agent Platform training (custom training + AutoML), Model Garden, Colab Enterprise, GPUs/TPUs |
| **3. Model deployment** | Make the trained model available for use — endpoint, app, batch job, or edge device | Determines latency, scale, and serving cost | Agent Platform endpoints, Model Registry, Cloud Run, GKE, LiteRT + Gemini Nano for edge |
| **4. Model management** | Manage and maintain models over time: version, monitor, retrain, govern | The stage leaders most often underfund — and where trust, compliance, and drift are won or lost | Model Registry (versioning), Model Monitoring (performance + drift), Agent Platform Feature Store, Agent Platform Pipelines (MLOps automation) |

**Two additional lifecycle facts the exam rewards:**

- **Security and responsible AI apply at every stage**, not just at the end: training data
  can be poisoned, models can leak, deployed agents can be hijacked (Session 4).
- **Model management is continuous**: **automatic model upgrades**, **performance
  tracking**, **drift monitoring**, and **security patches and updates** are the
  Google-recommended practices.

---

## 6. The gen AI landscape: five layers (objective 1.3)

The exam expects you to place a product in the right layer and explain the **business
implication** of that layer.

| Layer | What it is | Business implication | Google examples |
| --- | --- | --- | --- |
| **Infrastructure** | Core compute: physical hardware (servers, **GPUs**, Google's custom **TPUs**), storage, networking, data centres | Determines cost, scale, performance, and where data physically sits; the "hypercomputer" story is about making large-scale AI affordable and fast | TPUs, GPUs, Hypercomputer, global data centres, Cloud Storage/BigQuery |
| **Models** | Complex algorithms trained on vast data that learn patterns and generate content | The capability and cost engine; you choose quality vs latency vs price here | Gemini (Pro/Flash/Flash-Lite), Gemma, Imagen, Veo, Gemini Nano, embeddings |
| **Platforms** | APIs, data management, and model deployment tooling that remove infrastructure complexity | Turns experimentation into governed production: evaluation, monitoring, security, governance, scale | Gemini Enterprise Agent Platform (Agent Studio, Model Garden, Agent Search, AutoML, Pipelines), Google AI Studio |
| **Agents** | Software that **pursues a goal by observing the world and acting on it** with the tools available | Shifts AI from "answers" to "outcomes" — multi-step work with audit, permissions, and escalation needs | Agent Development Kit (ADK), Agent Runtime, Agent Garden, Gemini Enterprise |
| **Applications** | The user-facing surface where people consume AI | Adoption and value realisation happen here; this is what you measure and what you train people on | Gemini app, Gemini for Google Workspace, Gemini Enterprise, Gemini Notebook, Gemini Enterprise for Customer Experience |

> **Mnemonic:** **I**nfrastructure → **M**odels → **P**latforms → **A**gents →
> **A**pplications. "I Make Practical Agent Apps."

---

## 7. Google's foundation models (objective 1.4)

| Model family | Modality | What it is best at | Typical business use |
| --- | --- | --- | --- |
| **Gemini** | Multimodal (text, image, audio, video, code) | Flagship general reasoning, conversation, coding, content creation, question answering over long context | Chat assistants, document understanding, code assistance, agent reasoning engines. Variants: **Pro** (deepest reasoning/quality), **Flash** (balanced speed + cost, the agentic workhorse and app default), **Flash-Lite** (lowest cost for high volume), **Nano** (on-device/edge) |
| **Gemma** | Text and multimodal open models | Open, lightweight, customisable models you can run **locally or on your own infrastructure** | Data-sensitive or offline/edge deployments, research, customisation where you want full control and no per-call API cost |
| **Imagen** | Text → image (diffusion) | High-quality image **generation and editing** from textual descriptions | Marketing assets, product imagery, design iteration, storyboards |
| **Veo** | Text or image → video | Cinematic-quality **video generation** | Campaign videos, previsualisation, training content, rapid creative iteration |
| **Also worth knowing** | | | |
| **Chirp** | Speech | Speech-to-text and text-to-speech at scale | Contact-centre transcription, voice interfaces, subtitles, accessibility |
| **Lyria** | Music/audio | Music and audio generation | Jingles, background audio, creative tooling |

**Selection pattern you can reuse (and the exam tests):**

1. **Modality** — match input/output types to the task (text, image, audio, video, code).
2. **Quality vs latency vs cost** — Pro → Flash → Flash-Lite, decided by the use case's
   tolerance for waiting and its unit economics.
3. **Context window** — how much data must be in view at once.
4. **Deployment surface** — cloud API, your own VPC, or on-device (Gemini Nano).
5. **Customisation** — prompt, ground, tune, or fine-tune.

---

## 8. Where gen AI creates business value: create, summarize, discover, automate

| Value verb | What it means | Example use cases |
| --- | --- | --- |
| **Create** | Generate net-new content | Marketing copy, product images, code scaffolds, video drafts, personalised offers |
| **Summarize** | Condense information | Meeting notes, long contracts, call transcripts, research digests, case files |
| **Discover** | Find the right information at the right time | Enterprise search over unstructured archives, knowledge assistants, trend and anomaly discovery |
| **Automate** | Remove previously manual work | Document processing and data capture, ticket triage, RFP drafting, agentic workflows |

The exam's scenario questions almost always resolve to one of these four verbs. Naming the
verb first makes the product choice much easier.

---

## Exam traps in this session

1. **Nesting errors.** Gen AI is a *subset of deep learning*, which is a subset of ML, which
   is a subset of AI. LLMs are a *type of foundation model*, not a synonym for AI.
2. **Diffusion vs LLM.** Imagen and Veo are diffusion-based (image/video). Gemini is the LLM
   family. Don't pick "Gemini" for a pure photorealistic-image-generation question if Imagen
   is on the list.
3. **Labeled ≠ structured.** Labeled/unlabeled describes *annotation*; structured/unstructured
   describes *shape*. A labeled dataset can still be unstructured (tagged call recordings).
4. **Foundation model ≠ fine-tuned model.** A foundation model is the general-purpose base;
   fine-tuning is an adaptation step.
5. **Lifecycle is not linear.** "Model management" includes versioning, performance
   tracking, and drift monitoring — and drifting performance sends you back to data prep.
6. **Data accessibility is a business problem, not a technical footnote.** Availability,
   format, cost, and permissions decide whether the value is realisable.
7. **A bigger context window is not automatically better.** It raises relevance risk and
   cost; the exam rewards the balanced answer.
8. **Open model ≠ lesser model.** Gemma's value is *control, locality, and cost
   predictability* — that's usually the reason to choose it in a scenario.

## Rapid self-check

Answer these out loud. Answers are below.

1. In one sentence each, define AI, ML, deep learning, a foundation model, and an LLM.
2. What kind of model powers high-quality image generation, and what technique does it use?
3. Give one business example of structured data and one of unstructured data — and say why
   gen AI changes the value of the unstructured one.
4. Name the four stages of the ML lifecycle and one Google Cloud tool for each.
5. Which three approaches describe how ML models learn, and which one explains foundation
   model pretraining?
6. Why would a regulated business choose Gemma over a hosted Gemini API?

### Answers

1. **AI** = machines doing tasks that need human intelligence. **ML** = systems that learn
   patterns from data instead of following hand-written rules. **Deep learning** = ML using
   many-layered neural networks to extract complex patterns. **Foundation model** = a very
   large model pre-trained on broad, mostly unlabeled data and adaptable to many tasks.
   **LLM** = a foundation model specialised for understanding and generating language.
2. **Diffusion models** (Google's Imagen family): start from noise and iteratively denoise
   into an image guided by the text prompt.
3. Structured: transaction records in a data warehouse. Unstructured: contracts, emails, call
   recordings. Gen AI can now read/summarise/search that unstructured content, unlocking the
   majority of enterprise data that analytics could never touch.
4. **Data ingestion and preparation** (Cloud Storage / BigQuery / Dataflow), **model training**
   (Agent Platform training, AutoML, Model Garden), **model deployment** (Agent Platform
   endpoints, Cloud Run, Model Registry), **model management** (Model Monitoring, Feature
   Store, Pipelines, Model Registry).
5. **Supervised, unsupervised, reinforcement.** Foundation-model pretraining is
   **self-supervised** (the model generates its own learning signal from raw data), which is
   often grouped with unsupervised learning in the exam's wording.
6. Data residency/sovereignty and the ability to run locally (or air-gapped), full control of
   weights and customisation, no per-call API dependency, and predictable cost on owned
   infrastructure — Gemma is an **open** model family you can host yourself.

---

**Next:** [Session 2 — Google Cloud gen AI offerings → task matching](session-2-google-cloud-offerings.md)
