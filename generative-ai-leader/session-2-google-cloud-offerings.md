# Session 2 — Google Cloud Offerings: Matching Models, Platforms, Agent Capabilities, and APIs to the Task

**Exam domain:** 2. Google Cloud's gen AI offerings (~35% of the exam — the single biggest block)
**Covers objectives:** 2.1 through 2.5
**Goal of this session:** given a business need on the left, name the right Google Cloud
thing on the right — *without* notes. If you can do that, you have banked roughly a third
of the exam.

---

## 1. Why Google Cloud is positioned for gen AI (objective 2.1)

The exam asks this as "which Google Cloud strength does this scenario illustrate?" Learn
each strength with its evidence.

| Strength | What it means | Evidence to quote |
| --- | --- | --- |
| **AI-first company** | AI is integrated across Google's own products and services, not bolted on; Google researches, builds silicon, and ships models | Gemini in Search, Workspace, Android, Cloud; DeepMind research feeding products |
| **Enterprise-ready AI platform** | **Responsible, secure, private, reliable, scalable** — built for regulated production use | Data residency controls, VPC Service Controls, CMEK, IAM, SLAs, global regions |
| **Comprehensive AI ecosystem** | One vendor across infrastructure → models → platform → agents → applications, so integration effort is lower | Gemini models usable from the Gemini app through Workspace and Agent Platform with consistent governance |
| **Open approach** | Flexibility and choice: open models and open frameworks, not a single locked-in model | **Gemma** open models, Model Garden's large catalogue of first-party, third-party, and open-source models; open protocols such as **A2A** (agent-to-agent) and **MCP**; open-source **Agent Development Kit** |
| **AI-optimised infrastructure** | Purpose-built compute at scale | Google's custom **TPUs**, **GPUs**, **Hypercomputer** (a purpose-built AI supercomputing architecture), global data centres and networking, cloud computing on demand |
| **Control over your data** | You decide where data lives, who can reach it, and how it's used; models and outputs stay yours | Security, privacy, governance controls; data residency; IAM; customer-managed encryption |
| **Democratised AI development** | Low-code and no-code tools, pre-trained models, and simple APIs mean business teams can build without deep ML expertise | Agent Studio for production apps and agents, Apps Script and AppSheet for low-code, pre-built APIs, AutoML |

> **Exam cue:** if the question is about *choice, portability, or avoiding lock-in*, the
> answer is almost always the **open approach** (Gemma, Model Garden, open frameworks).
> If it's about *speed of building without ML specialists*, the answer is
> **low-code/no-code + pre-trained models + APIs**.

---

## 2. Prebuilt offerings that enable AI-powered work (objective 2.2)

| Offering | What it is | Best for | Exam cue |
| --- | --- | --- | --- |
| **Gemini app** | Google's consumer/prosumer generative AI assistant: writing, summarising, translating, image creation, research, "ask about your files" | Individual productivity, drafting, brainstorming, quick research | The *user-facing chat assistant* |
| **Gemini Advanced** | The paid tier of the Gemini app with extra features and **enterprise-grade protections**, plus access to the most capable models and longer context | Professionals who need frontier capability, longer documents, and stronger data protections | "Extra features + enterprise-grade protections" is the distinguishing phrase |
| **Gems** | Personalised AI assistants inside Gemini, created from your own instructions and knowledge — reusable, tailored behaviour | Standardising a recurring workflow: brand-voice writer, code reviewer, onboarding coach, style guide | Custom assistants *without* building anything |
| **Gemini for Google Workspace** | Gemini embedded in the apps people already use — Gmail, Docs, Sheets, Slides, Meet | Everyday work in place: draft an email, summarise a Meet recording, generate slide imagery, analyse a Sheet | The value is *no new tool to adopt* — it meets users where they work |
| **Gemini Enterprise** | Organisation-wide entry point for AI: customised **search and conversation agents** over internal data sources, surfaced in your internal sites and dashboards, with enterprise governance | Enterprise knowledge discovery, internal assistants, surfacing many agents and data sources to employees under one governed roof | "Internal, organisation-wide, multiple data sources, governed." (Formerly **Agentspace**.) |
| **Gemini Notebook** | A research assistant built around *your* sources: upload documents/links and it summarises, answers questions, and generates study aids from that material **(formerly NotebookLM)** | Document understanding and grounded research over a curated source set — including audio overviews and Q&A | "Grounded in the sources *you* upload" |
| **Gemini for Google Cloud** | AI assistant for Google Cloud itself: helps write and debug code, optimise cloud applications, analyse data in BigQuery, and strengthen security posture | Cloud engineers and data teams working in the console | "It helps you use Google Cloud" |
| **Gemini Enterprise for Customer Experience** | Suite for customer engagement, built on **Contact Center as a Service (CCaaS)**: CX Agent Studio (customer-facing virtual agents), Agent Assist (help for live human agents), CX Insights (analytics over every customer conversation) | Contact centres, self-service, agent productivity, voice-of-customer analytics | "External customers + contact centre" (formerly Customer Engagement Suite) |

**Choosing among the Gemini surfaces — the exam's favourite four-way:**

- **Gemini app / Advanced** → personal productivity, one person, general knowledge.
- **Gemini for Google Workspace** → productivity *inside* Gmail/Docs/Meet/Sheets.
- **Gemini Enterprise** → organisation-wide internal search and agents over company data.
- **Gemini Notebook** → deep research grounded in a specific set of *your* documents.

---

## 3. Improving the customer experience (objective 2.3)

| Offering | What it is | Best for |
| --- | --- | --- |
| **Agent Search on Gemini Enterprise Agent Platform** | Google's enterprise search and recommendation capability, with **prebuilt RAG** over your content — websites, documents, structured sources | Site search, product discovery, knowledge base search, "answer over our own content" |
| **Grounding with Google Search** | Connects a model to Google Search so answers reflect current, *world* knowledge | Freshness and factual recency for public information |
| **Google Search** (as a surface) | The world's largest consumer search surface | Consumer discovery and reach |
| **Gemini Enterprise for Customer Experience** | See the table above: CX Agent Studio, Agent Assist, CX Insights on CCaaS | Contact-centre transformation |

**The critical distinction:** *Agent Search* grounds on **your** content (first-party data);
*Grounding with Google Search* grounds on **world** knowledge. Session 3 makes this a
first-class topic — the exam tests it repeatedly.

---

## 4. Empowering developers and builders (objective 2.4)

### 4.1 Gemini Enterprise Agent Platform — the unified platform

Formerly **Vertex AI**, now the umbrella product name the exam uses. It is Google Cloud's
unified ML and gen AI platform: infrastructure, tools, and pre-trained models to **build,
train, tune, deploy, and manage** models and agents, with the enterprise controls
(security, governance, monitoring) that make production possible.

| Component | What it gives you | When it's the answer |
| --- | --- | --- |
| **Model Garden** | A catalogue to discover, try, and use foundation models — Google first-party (Gemini, Imagen, Veo, Gemma), third-party (partner models), and open-source | "We want choice / the right model for the job / to compare models" |
| **Agent Studio** | Build, tune, and deploy **production-ready** gen AI apps and agents at scale; prototype prompts; evaluate and manage them (formerly Vertex AI Studio) | Enterprise build-out with governance and scale |
| **Agent Search** | Search, recommendation, and prebuilt RAG over your own content | Enterprise search or grounded answers over first-party data |
| **Agent Platform AutoML** | Train models with minimal technical knowledge and effort — bring data, get a model | "Limited ML expertise, need a custom model" |
| **Model Builder / custom training** | Train and use your own models fully custom at scale with ML frameworks | "We have ML experts, unique models, full control needed" |
| **Agent Platform Pipelines** | Automate and orchestrate ML tasks (MLOps) | Repeatable training, retraining, and deployment workflows |
| **Model Registry** | Version and organise models | Versioning, governance, rollback |
| **Model Monitoring** | Track performance and detect **drift** in production | "Accuracy degraded over time" |
| **Agent Platform Feature Store** | Manage and serve the data features models use, consistently between training and serving | Feature reuse, training/serving consistency, data management |
| **Agent Runtime** | Managed runtime to deploy and operate agents (formerly Agent Engine) with scale, identity, and observability | Deploying agents to production |

### 4.2 The two Studios — a guaranteed exam question

| | **Google AI Studio** | **Agent Studio** |
| --- | --- | --- |
| Purpose | **Quick prototyping** with the Gemini API | Building and deploying **production-ready** AI applications and agents at scale |
| Cost/effort | Free of charge, minimal setup | Enterprise platform with governance, security, monitoring |
| Audience | Developers and business technologists experimenting | Teams shipping governed, scalable workloads |
| Exam cue | "Try it out fast", "prototype", "experiment with prompts" | "Production", "at scale", "enterprise controls", "deploy" |

### 4.3 RAG offerings on Google Cloud (objective 2.4 + 3.3)

| Option | What it is | Choose it when |
| --- | --- | --- |
| **Prebuilt RAG with Agent Search** | Turn-key retrieval + grounding over your content, with enterprise search quality, connectors, and ranking handled for you | You want grounded answers **fast, with low engineering effort**, over enterprise content |
| **RAG APIs** | Building blocks (e.g., grounding/check-grounding style APIs and embedding models) to assemble a custom RAG pipeline in your own application | You need **control** over chunking, ranking, retrieval logic, or custom orchestration |
| **Grounding with Google Search** | Grounds responses in current world knowledge from Google Search | The question needs **public, fresh** information rather than your private data |
| **Vector search / embeddings** | Store and retrieve semantically similar content for retrieval steps | Custom pipelines, semantic similarity, recommendation |

**The classic exam scenario:** *"Employees can't find answers buried across documents, and
the model keeps making things up."* → **Prebuilt RAG with Agent Search** (fast, governed) or
**RAG APIs** (if they need custom control); then measure groundedness.

---

## 5. Agents and their tooling (objective 2.5)

### 5.1 What an agent is, and its three components

**Definition to memorise:** *A gen AI agent is an application that tries to achieve a
**goal** by **observing** the world and **acting** upon it, using the **tools** at its
disposal.*

| Component | Role | Plain-language |
| --- | --- | --- |
| **Model** | The "brains": the LLM that reasons, plans, and decides | It thinks |
| **Tools** | Functionalities that let the agent interact with its environment — read/write data, call APIs, use hardware | It acts |
| **Reasoning loop** | The iterative cycle of observe → interpret → reason → act, repeated until the goal is met | It keeps going until done |

### 5.2 Tool types — learn the four

| Tool type | What it does | Example |
| --- | --- | --- |
| **Extensions** | Connect the agent to **external services via APIs** | Query a CRM, book a slot, hit a weather API |
| **Functions** | Define **specific actions or tasks** the agent can perform in your code | "calculate_shipping_cost", "create_ticket" |
| **Data stores** | Provide **access to information** the agent can retrieve and ground on | Product catalogue, policy documents, knowledge base |
| **Plugins** | Add **new skills and integrations** to the agent | Enterprise connectors, third-party service integrations |

> **Mnemonic:** **E**xtensions connect, **F**unctions act, **D**ata stores inform,
> **P**lugins extend.

### 5.3 Types of agents

| Type | How it works | Strength |
| --- | --- | --- |
| **Deterministic (traditional)** | Predefined paths and actions — rules and flows | Predictable, auditable, compliant |
| **Generative** | Defined in natural language, LLM-driven reasoning gives a genuinely conversational feel | Flexible, handles ambiguity, natural interaction |
| **Hybrid** | Combines deterministic control with generative flexibility | The powerful default for enterprise: creative handling *inside* governed guardrails |

**Agent use-case families:** customer service agents, employee productivity agents, creative
agents, code agents, data agents, security agents.

### 5.4 Building and running agents

| Capability | Purpose |
| --- | --- |
| **Agent Development Kit (ADK)** | Open-source, code-first framework for building multi-step, tool-using, multi-agent systems |
| **Agent Studio** | Lower-code visual building of agents and apps |
| **Agent Garden** | Library of prebuilt agent templates and samples to start from |
| **Agent Runtime** | Managed deployment, scaling, identity, and observability for agents |
| **A2A (Agent2Agent) protocol** | Open protocol so agents built on different platforms can communicate and delegate |
| **MCP (Model Context Protocol)** | Open standard for connecting models/agents to data sources and tools |
| **Model Armor** | Screens prompts and responses for malicious input (e.g., jailbreak/prompt-injection attempts) and sensitive-data leakage |
| **Agent identity, permissions, and observability** | Agents act with scoped identity and leave an audit trail of decisions, tool calls, and escalations |

> **Exam cue:** *"An agent needs to do X across systems"* → the mechanism is a **tool**
> (extension/function/data store/plugin). *"Different vendor agents must work together"* →
> **A2A**. *"The agent must be prevented from leaking data or being hijacked"* → **Model
> Armor + scoped identity + logging**, all under **SAIF**.

---

## 6. Pre-built AI APIs — match API to task (objective 2.5)

These are the "boring but certain" marks. Learn the table cold.

| API | Turns… into… | Typical business task | Exam keywords |
| --- | --- | --- | --- |
| **Speech-to-Text API** | Speech → text | Transcribe calls and meetings, subtitles, voice input, compliance recording review | "audio/video → transcript" |
| **Text-to-Speech API** | Text → natural-sounding speech | Voice user interfaces, accessibility (read-aloud), personalised audio messages, IVR | "make it speak" |
| **Translation API** | Text (and more) → another language | Localisation, multilingual customer support, translating websites and audio/video files | "translate text/site/media" |
| **Document Translation API** | Formatted documents → translated documents, **layout preserved** | Localising contracts, manuals, regulatory filings, brochures | "keep the original layout/format" |
| **Document AI API** | Documents → structured data | Automated data capture, invoice/receipt/ID processing, form parsing, document summarisation | "extract data from documents / automate document processing" |
| **Cloud Vision API** | Images → labels/insights | Content moderation, tagging, visual search, OCR of images, face/landmark detection | "analyse an image" |
| **Cloud Video Intelligence API** | Video → insights | Video content recommendation, video search, media analysis, moderation | "analyse a video" |
| **Natural Language API** | Unstructured text → insight | Sentiment analysis, content classification, entity extraction | "understand sentiment/entities" |
| **Gemini API via Vertex/Agent Platform** | Prompts → generated content/agents | Anything generative: chat, summarisation, extraction, reasoning, agent brains | "generate, converse, reason" |

**Where you build with them:**

| Build surface | Use it for |
| --- | --- |
| **Cloud Run / Cloud Run functions (Cloud Functions)** | Serverless glue and endpoints that call Gemini or AI APIs as part of an app |
| **Cloud Storage and databases** | Stores for documents, media, embeddings, and application data |
| **Apps Script / AppSheet** | Low-code/no-code automation that brings gen AI into Workspace and business apps |
| **Agent Platform / Agent Studio** | Governed, scalable production deployments with monitoring |

---

## 7. Master matching table — offering → intended task

Cover the right column and test yourself. This table is the heart of Domain 2.

| Offering | Intended task |
| --- | --- |
| **Gemini app** | Everyday personal assistance: write, summarise, translate, generate images |
| **Gemini Advanced** | Same, plus frontier capability, larger limits, and enterprise-grade protections |
| **Gems** | Packaged, reusable personalised assistants with fixed instructions |
| **Gemini for Google Workspace** | Gen AI inside Gmail, Docs, Sheets, Slides, Meet |
| **Gemini Enterprise** | Governed internal search + conversation agents across company data sources, at organisation scale |
| **Gemini Notebook** | Research and Q&A grounded in a curated set of your own uploaded sources |
| **Gemini for Google Cloud** | Help building, coding, debugging, and securing on Google Cloud |
| **Gemini Nano** | Gen AI running **on the device** (edge), private and low-latency |
| **LiteRT** | Runtime that deploys models to edge devices |
| **Gemini** | Multimodal reasoning, conversation, coding, long-context understanding |
| **Gemma** | Open, lightweight, customisable models for local/self-hosted deployments |
| **Imagen** | Text-to-image generation and editing |
| **Veo** | Video generation from text or images |
| **Chirp** | Speech generation and recognition models |
| **Agent Platform (Gemini Enterprise Agent Platform)** | The unified platform to build, train, tune, deploy, and manage ML/gen AI at enterprise scale |
| **Model Garden** | Discover and use first-party, third-party, and open-source models |
| **Model Builder / custom training** | Train fully custom models with ML frameworks |
| **Agent Platform AutoML** | Train custom models with minimal technical effort |
| **Agent Studio** | Build and deploy production-grade gen AI apps and agents |
| **Google AI Studio** | Free, fast prototyping with the Gemini API |
| **Agent Search** | Enterprise search + recommendation, and prebuilt RAG over your content |
| **RAG APIs** | Assemble custom retrieval-augmented generation pipelines |
| **Grounding with Google Search** | Ground answers in current world knowledge |
| **Agent Runtime** | Managed deployment, scaling, and operation of agents |
| **Agent Garden** | Prebuilt agent templates to accelerate development |
| **Agent Development Kit (ADK)** | Code-first framework for multi-agent, tool-using systems |
| **A2A protocol** | Let agents from different platforms communicate |
| **Model Armor** | Screen prompts/responses for injection, jailbreak, and data leakage |
| **Model Registry** | Version and organise models |
| **Model Monitoring** | Track production performance and detect drift |
| **Feature Store** | Manage/serve model features consistently |
| **Agent Platform Pipelines** | Automate MLOps workflows |
| **Speech-to-Text** | Transcribe speech/audio/video |
| **Text-to-Speech** | Generate natural speech |
| **Translation API** | Translate text, sites, audio, video |
| **Document Translation API** | Translate documents keeping layout |
| **Document AI** | Extract data from and summarise documents |
| **Cloud Vision** | Analyse image content |
| **Cloud Video Intelligence** | Analyse video content |
| **Natural Language API** | Sentiment, classification, entities from text |
| **Gemini Enterprise for Customer Experience** | Contact-centre and customer engagement: virtual agents, live-agent assist, conversation insights |
| **CCaaS (Contact Center as a Service)** | Cloud-native contact-centre foundation |
| **Customer Experience Agent Studio** | Customer-facing virtual agents/chatbots |
| **Agent Assist** | Real-time help for human agents |
| **Customer Experience Insights** | Analytics over all customer conversations |
| **Security Command Center** | Security posture visibility and threat findings across the estate |
| **IAM** | Control who can access which resources |
| **VPC Service Controls** | Prevent data exfiltration by defining service perimeters |
| **Cloud KMS / CMEK** | Manage your own encryption keys |

---

## 8. "Which one?" quick decisions

| If the scenario says… | Answer |
| --- | --- |
| "Prototype quickly, free, with the Gemini API" | **Google AI Studio** |
| "Build and deploy a production agent at scale" | **Agent Studio** on **Agent Platform** |
| "We want to choose among many models, including open and third-party" | **Model Garden** |
| "Train a custom model but we lack ML deep expertise" | **Agent Platform AutoML** |
| "Answers must reflect current public information" | **Grounding with Google Search** |
| "Answers must reflect our own documents" | **Agent Search / prebuilt RAG** or **RAG APIs** |
| "Employees can't find internal knowledge across many systems" | **Gemini Enterprise** (with **Agent Search**) |
| "Summarise a set of uploaded PDFs for research" | **Gemini Notebook** |
| "Gen AI inside Gmail/Docs/Meet with no new tool" | **Gemini for Google Workspace** |
| "Cut contact-centre handle time and improve self-service" | **Gemini Enterprise for Customer Experience** (CX Agent Studio, Agent Assist, CX Insights) |
| "Transcribe and then analyse thousands of support calls" | **Speech-to-Text** + **Natural Language / Gemini** |
| "Automate invoice data capture" | **Document AI** |
| "Moderate user-uploaded images" | **Cloud Vision** |
| "Localise manuals while preserving layout" | **Document Translation API** |
| "Prevent prompt injection and data leakage in a deployed agent" | **Model Armor** + scoped identity + logging (SAIF) |
| "Detect model quality degradation after launch" | **Model Monitoring** (drift) |
| "Run AI on a phone with no network" | **Gemini Nano** + **LiteRT** |

---

## Exam traps in this session

1. **Google AI Studio ≠ Agent Studio.** Free prototyping vs production-grade build/deploy.
   The exam uses both names in the same question set.
2. **Gemini Enterprise ≠ the Gemini app.** One is org-wide governed internal search and
   agents; the other is a personal assistant.
3. **Agent Search (your data) vs Grounding with Google Search (world data).** Read the
   scenario's data source carefully.
4. **Model choice must follow the constraint.** Modality, latency, cost, privacy, and
   context window are usually stated in the stem — the distractor offering ignores one.
5. **AutoML is the "low expertise" path, Model Builder is the "full control" path.** Don't
   swap them.
6. **Low-code ≠ lower value.** When a scenario stresses scale of adoption and limited
   engineering capacity, prefer low-code/no-code, pre-trained models, and APIs.
7. **Agent component questions are about *tools*.** Extensions, functions, data stores, and
   plugins are different ways for the agent to reach outside itself.
8. **Old names appear.** If you see Vertex AI, Vertex AI Studio, Vertex AI Search,
   Agentspace, or NotebookLM, translate: Agent Platform, Agent Studio, Agent Search,
   Gemini Enterprise, Gemini Notebook.
9. **Enterprise ≠ consumer features.** Phrases like "data residency", "customer-managed
   encryption", "SLAs", and "audit" push you toward the enterprise platform, not the free
   prototyping surface.
10. **Contact centre questions belong to the Customer Experience suite**, not to Gemini
    Enterprise (internal) and not to Agent Platform (build).

## Rapid self-check

1. Which product do you use to prototype with the Gemini API for free, and which to deploy
   a governed production agent?
2. Name the four agent tool types and what each does.
3. Distinguish prebuilt RAG with Agent Search from RAG APIs in one sentence each.
4. A retailer wants product discovery search and grounded answers over its own catalogue.
   Which Google Cloud capability?
5. What is the difference between grounding with Google Search and grounding on enterprise
   data?
6. Which API preserves document layout when translating, and which extracts structured data
   from documents?
7. Which agent type combines predefined flows with LLM reasoning, and why does that matter
   in a regulated industry?

### Answers

1. **Google AI Studio** for free prototyping; **Agent Studio** on **Gemini Enterprise Agent
   Platform** for production deployment.
2. **Extensions** connect to external services via APIs; **functions** define specific
   actions/tasks; **data stores** provide access to information; **plugins** add new skills
   and integrations.
3. **Prebuilt RAG with Agent Search** = turn-key, low-effort grounded search over your
   content with enterprise search quality. **RAG APIs** = building blocks for a custom
   pipeline where you control chunking, ranking, and orchestration.
4. **Agent Search** (enterprise search/recommendation with prebuilt RAG) on **Agent
   Platform**.
5. Google Search grounding uses **public, current world knowledge**; enterprise grounding
   uses **your first-party data** (documents, databases, sites) — the latter is your private
   context, the former is freshness on public facts.
6. **Document Translation API** preserves layout; **Document AI API** extracts structured
   data (and can summarise documents).
7. **Hybrid agents** — deterministic guardrails plus generative flexibility, giving
   predictable, auditable control paths while still handling natural language.

---

**Next:** [Session 3 — Prompting, grounding, and RAG](session-3-prompting-and-rag.md)
