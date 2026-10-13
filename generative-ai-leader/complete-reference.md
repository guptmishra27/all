# Complete Reference — Consolidated Revision Sheet

Everything in one place: glossary, master mapping tables, cheat sheets, and the exam facts.
Use this for the final pass, and as the thing you skim the morning of the exam.

**Contents**
[Exam facts](#exam-facts) · [Domain weights](#domain-weights) · [Glossary](#glossary) ·
[Models](#model-families) · [Offerings to task](#master-offerings-to-task-table) ·
[Prompting](#prompting-techniques) · [Sampling parameters](#sampling-parameters) ·
[Grounding & RAG](#grounding-and-rag) · [Limitations](#foundation-model-limitations-and-mitigations) ·
[Monitoring](#monitoring-and-evaluation) · [HITL](#human-in-the-loop-hitl) ·
[Responsible AI](#responsible-ai) · [Secure AI & SAIF](#secure-ai-and-saif) ·
[Security controls](#security-controls-map) · [Cloud AI APIs](#cloud-ai-apis) ·
[ML lifecycle](#ml-lifecycle-and-google-cloud-tools) · [Model selection](#model-selection-factors) ·
[Business value](#measuring-business-value) · [Naming changes](#naming-changes) ·
[Acronyms](#acronyms) · [High-frequency topics](#high-frequency-topics)

---

## Exam facts

| Item | Detail |
| --- | --- |
| Certification | Google Cloud Certified Generative AI Leader |
| Length | 90 minutes |
| Format | 50–60 multiple-choice questions |
| Delivery | Online-proctored or onsite-proctored |
| Fee / validity | $99 (plus tax) / 3 years |
| Languages | English, Japanese, Spanish, Portuguese |
| Prerequisites | None |
| Audience | Business and technical professionals who *influence* gen AI adoption; conceptual, not implementation-level |

## Domain weights

| # | Domain | Weight |
| --- | --- | --- |
| 1 | Fundamentals of gen AI | ~30% |
| 2 | Google Cloud's gen AI offerings | ~35% |
| 3 | Techniques to improve gen AI model output | ~20% |
| 4 | Business strategies for a successful gen AI solution | ~15% |

**Implication:** Domains 1 + 2 ≈ 65% of the exam. Concepts and product-tasking dominate; the
rest is scenario judgement.

---

## Glossary

### A

| Term | Definition |
| --- | --- |
| **A2A (Agent2Agent) protocol** | Open protocol that lets agents built on different platforms communicate and delegate tasks |
| **Agent** | Software that pursues a **goal** by **observing** its environment and **acting** on it using available **tools**. Components: model (reasoning), tools (action), reasoning loop (iteration) |
| **Agent Assist** | Real-time assistance for live human contact-centre agents |
| **Agent Development Kit (ADK)** | Open-source, code-first framework for building tool-using, multi-agent systems |
| **Agent Garden** | Library of prebuilt agent templates |
| **Agent Platform** | **Gemini Enterprise Agent Platform** — Google Cloud's unified ML/gen AI platform (formerly **Vertex AI**): Model Garden, Agent Studio, Agent Search, AutoML, Pipelines, Model Registry/Monitoring, Feature Store, Agent Runtime |
| **Agent Runtime** | Managed runtime to deploy, scale, and observe agents (formerly Agent Engine) |
| **Agent Search** | Enterprise search and recommendation with **prebuilt RAG** over your content |
| **Agent Studio** | Build and deploy **production-ready** gen AI apps and agents at scale (formerly Vertex AI Studio) |
| **AI (artificial intelligence)** | Building machines that perform tasks normally requiring human intelligence — learning, problem-solving, decision-making |
| **AI Principles** | Google's seven published principles for AI development (see [Responsible AI](#responsible-ai)) |
| **Anonymisation** | Irreversibly removing identifying information from data |
| **AutoML** | Training custom models with minimal technical knowledge and effort (Agent Platform AutoML) |
| **Automatic model upgrades** | Managed, continuous model updates for quality/security without manual migration |
| **Augmentation (RAG step)** | Inserting retrieved content into the prompt so generation is grounded |

### B

| Term | Definition |
| --- | --- |
| **Bias** | Systematic skew learned from data; subtle bias in training data can be amplified in outputs |
| **BigQuery** | Google Cloud's analytics data warehouse; a common data source for gen AI pipelines and grounding |

### C

| Term | Definition |
| --- | --- |
| **CCaaS (Contact Center as a Service)** | Cloud-native contact-centre platform that customer-experience AI is built on |
| **Chain-of-thought (CoT)** | Prompting technique that guides the model through intermediate reasoning steps |
| **Chirp** | Google's speech model family (speech-to-text, text-to-speech) |
| **Cloud Video Intelligence API** | Analyses video content to extract meaningful information |
| **Cloud Vision API** | Analyses images: labels, objects, faces, landmarks, moderation, OCR-style tasks |
| **CMEK (Customer-Managed Encryption Keys)** | You control the encryption keys protecting your data |
| **Context window** | How much text the model can consider at once; larger costs more and can dilute relevance |
| **Create / Summarize / Discover / Automate** | The four value verbs of gen AI use cases |
| **Customer Experience (CX) Agent Studio** | Customer-facing virtual agents/chatbots in the Customer Experience suite |
| **Customer Experience Insights** | Analytics over all customer conversations (formerly Conversational Insights) |

### D

| Term | Definition |
| --- | --- |
| **Data dependency** | Model performance relies heavily on the data it was trained on |
| **Data quality** | Accuracy, completeness, consistency, relevance, timeliness — the prerequisite for useful AI |
| **Data residency** | Keeping data stored/processed in approved geographies for legal/sovereignty reasons |
| **Data store (agent tool)** | Gives the agent access to information it can retrieve and reason over |
| **Deep learning** | ML subset using artificial neural networks with many layers to extract complex patterns |
| **Deployment** | Making a trained model available for use (endpoint, app, batch, or edge) |
| **Diffusion model** | Generates images/video by denoising random noise toward a prompt (Imagen, Veo) |
| **Document AI API** | Extracts structured data from documents; automates data capture and can summarise documents |
| **Document Translation API** | Translates formatted documents while preserving layout |
| **Drift monitoring** | Detecting changes in data/behaviour that degrade model accuracy over time |

### E

| Term | Definition |
| --- | --- |
| **Edge AI** | Running models on devices or local servers close to where the action happens (Gemini Nano, LiteRT, Gemma) |
| **Embeddings / vector search** | Numeric representations of content used to find semantically similar items — the retrieval backbone of RAG |
| **Explainability** | Making AI decisions understandable to affected people, auditors, and operators |
| **Extensions (agent tool)** | Connect the agent to external services via APIs |

### F

| Term | Definition |
| --- | --- |
| **Fairness** | Assessing whether AI outcomes are equitable across groups — a core responsibility, not a feature |
| **Feature Store (Agent Platform)** | Manages and serves model features consistently across training and serving |
| **Few-shot prompting** | Providing multiple examples so the model infers the pattern/format |
| **Fine-tuning** | Further training a pre-trained model to improve performance on a specific task or domain; changes behaviour, not factual freshness |
| **Foundation model** | Very large model pre-trained on massive, broad, mostly unlabeled data; adaptable to many tasks |
| **Function (agent tool)** | A specific action or task the agent can perform in your own code |

### G

| Term | Definition |
| --- | --- |
| **Gemini** | Google's flagship multimodal foundation model family (Pro = deepest reasoning; Flash = balanced workhorse; Flash-Lite = cheapest at volume; Nano = on-device) |
| **Gemini Advanced** | Paid tier of the Gemini app with extra features and enterprise-grade protections |
| **Gemini app** | Google's consumer/prosumer gen AI assistant for writing, summarising, translating, image creation |
| **Gemini Enterprise** | Organisation-wide governed entry point for internal search and conversation agents over company data (formerly **Agentspace**) |
| **Gemini Enterprise for Customer Experience** | Customer engagement suite: CX Agent Studio, Agent Assist, CX Insights, built on CCaaS (formerly Customer Engagement Suite) |
| **Gemini for Google Cloud** | Assistant for building, coding, debugging, and securing on Google Cloud |
| **Gemini for Google Workspace** | Gemini embedded in Gmail, Docs, Sheets, Slides, Meet |
| **Gemini Nano** | Google's most compact model, designed to run on devices |
| **Gemini Notebook** | Research assistant grounded in the sources you upload (formerly **NotebookLM**) |
| **Gemma** | Google's **open** model family — user-friendly, customisable, suited to local/self-hosted and specialised deployments |
| **Gems** | Personalised, reusable AI assistants inside Gemini defined by your instructions |
| **Generative AI (gen AI)** | ML application that creates new content (text, images, audio, video, code); can be multimodal |
| **Google AI Studio** | Free, fast **prototyping** with the Gemini API |
| **Grounding** | Connecting model output to verifiable sources of information (first-party, third-party, or world data) |
| **Grounding with Google Search** | Grounding responses in current public/world knowledge |

### H

| Term | Definition |
| --- | --- |
| **Hallucination** | Output that isn't accurate or isn't based on real information — stated confidently |
| **HITL (human in the loop)** | Human input and feedback integrated directly into ML workflows |
| **Human in/on/over the loop** | In: human approves before action. On/over: humans monitor samples, dashboards, and escalations while the system runs |
| **Hybrid agent** | Agent combining deterministic (predefined) and generative capabilities |
| **Hypercomputer** | Google Cloud's purpose-built AI supercomputing architecture for large-scale training/serving |

### I–L

| Term | Definition |
| --- | --- |
| **IAM (Identity and Access Management)** | Controls who can access which resources; least privilege, roles, service and agent identities |
| **Imagen** | Text-to-image diffusion model family for generating/editing high-quality images |
| **Infrastructure layer** | Core compute and storage — GPUs, TPUs, data centres, networking — that gen AI runs on |
| **Iteration (RAG step)** | Optional refinement where the model retrieves again to improve the answer |
| **KPI** | Key performance indicator — the business metric you manage the solution against |
| **Labeled data** | Data with tags/annotations (a name, class, or number) |
| **Latency** | Response time; a primary driver of model-tier and architecture choice |
| **LiteRT** | Runtime that deploys AI models to edge devices |
| **LLM (large language model)** | A foundation model specialised for understanding and generating human language |
| **Lyria** | Google's music/audio generation model |

### M

| Term | Definition |
| --- | --- |
| **MCP (Model Context Protocol)** | Open standard for connecting models/agents to data sources and tools |
| **Metaprompting** | Using prompts to have the model generate, modify, or interpret other prompts |
| **Model Armor** | Google Cloud security layer that screens prompts and responses for injection/jailbreak attempts and sensitive-data disclosure |
| **Model Garden** | Catalogue to discover and use first-party, third-party, and open-source models |
| **Model Monitoring** | Tracks production model performance and detects drift |
| **Model Registry** | Stores, organises, and **versions** models |
| **Multimodal** | Handling more than one data type (text, image, audio, video, code) |

### N–P

| Term | Definition |
| --- | --- |
| **Natural Language API** | Derives insight from unstructured text: sentiment, classification, entity extraction |
| **NLP (natural language processing)** | The field of getting computers to work with human language |
| **One-shot prompting** | Providing a single example of the desired input→output |
| **Open approach** | Google's strategy of offering choice: open models (Gemma), open frameworks, open protocols (A2A, MCP) |
| **Output length** | Sampling parameter limiting the maximum generated text |
| **Pipelines (Agent Platform)** | Automating/orchestrating ML workflows (MLOps) |
| **Platform layer** | APIs, data management, and deployment tooling that remove infrastructure complexity |
| **Plugins (agent tool)** | Add new skills and integrations to the agent |
| **Post-generation review** | Continuous human review after deployment to improve and adapt the model |
| **Pre-generation review** | Human experts validate outputs before deployment, catching errors/bias before user impact |
| **Prompt** | The instruction or input given to a model |
| **Prompt chaining** | Breaking a task into a sequence of prompts, each feeding the next |
| **Prompt engineering** | The art and science of crafting inputs to maximise output value and tailor responses |
| **Prompt tuning / templates** | Adapting model parameters (tuning) or reusing saved prompt patterns (templates) for consistency |
| **Pseudonymisation** | Replacing identifiers with tokens while keeping a separate mapping key — reversible, so data usually remains personal data |

### R

| Term | Definition |
| --- | --- |
| **RAG (retrieval-augmented generation)** | Retrieving relevant external content, augmenting the prompt with it, and generating a grounded answer (plus optional iteration) |
| **ReAct (reason and act)** | Prompting/agent technique where the model reasons and takes actions with tools on a user query |
| **Reasoning loop** | The agent's iterative observe → interpret → reason → act cycle |
| **Reinforcement learning** | Learning through interaction and feedback to maximise reward and minimise penalty |
| **Responsible AI** | Ensuring AI applications don't cause harm and are used ethically across the entire lifecycle |
| **Retrieval (RAG step)** | Searching external sources for content relevant to the query |
| **Role prompting** | Assigning a persona to influence style, tone, and focus |

### S

| Term | Definition |
| --- | --- |
| **Safety settings** | Controls that filter potentially harmful or inappropriate content from model output |
| **SAIF (Secure AI Framework)** | Google's framework for securing AI systems — six core elements, mapped across data, infrastructure, model, and application components |
| **Scale** | How many users/interactions the solution must handle; drives tier, infrastructure, and cost design |
| **Secure AI** | Protecting AI applications from malicious attacks and misuse throughout the ML lifecycle |
| **Security Command Center** | Visibility into security posture, findings, misconfigurations, and threats |
| **Self-supervised learning** | Model generates its own training signal from raw data — how foundation models learn from unlabeled text |
| **Speech-to-Text API** | Converts speech to text; transcribes audio and video content |
| **Structured data** | Organised, easily searchable data (rows/columns, relational databases) |
| **Supervised learning** | Learning from labeled data to predict outputs for new inputs |

### T–V

| Term | Definition |
| --- | --- |
| **Temperature** | Controls creativity/randomness of token selection; lower for factual/deterministic work |
| **Text-to-Speech API** | Converts text into natural-sounding speech; voice interfaces and personalised communication |
| **Third-party data** | Data sourced/licensed externally or federated from connected systems |
| **Token** | A meaningful chunk of text (roughly a word-piece or punctuation) — the unit of cost, latency, and limits |
| **Top-p (nucleus sampling)** | The cumulative probability pool of most-likely tokens considered during generation |
| **TPU (Tensor Processing Unit)** | Google's custom-designed AI accelerator chip |
| **Training** | Creating the model from data (from prompting/fine-tuning, to AutoML, to fully custom) |
| **Translation API** | Translates text, documents, websites, audio, and video files |
| **Transparency** | Disclosing when AI is in use, what it can do, and how it is governed |
| **Unlabeled data** | Raw, untagged information that lacks meaning by itself |
| **Unstructured data** | Data without a predefined structure — text, images, audio, video — requiring sophisticated analysis |
| **Unsupervised learning** | Finding natural groupings and patterns in unlabeled data |
| **Veo** | Google's video generation model (text or image → video) |
| **Versioning** | Tracking model versions for audit and rollback (Model Registry) |

### W–Z

| Term | Definition |
| --- | --- |
| **Workload monitoring** | Observing running workloads for anomalies and policy violations to maintain secure AI systems |
| **World data** | Public, current information from the open web (Google Search grounding) |
| **Zero-shot prompting** | Asking the model to perform a task with no examples |

---

## Model families

| Family | Modality | Strength | Choose it when |
| --- | --- | --- | --- |
| **Gemini Pro** | Multimodal | Deepest reasoning, long-context understanding, hardest problems | Quality is the priority and cost/latency can absorb it |
| **Gemini Flash** | Multimodal | Pro-grade reasoning at lower latency/cost; agentic and coding workhorse; the app default | High-volume production, interactive apps, agents |
| **Gemini Flash-Lite** | Multimodal | Cheapest at scale | Classification, extraction, routing, massive throughput |
| **Gemini Nano** | Multimodal (small) | Runs **on-device** | Privacy, offline, low latency at the edge (with LiteRT) |
| **Gemma** | Text/multimodal (open) | Open weights, local/self-hosted, customisable | Control, residency, offline, cost predictability, customisation |
| **Imagen** | Text → image | High-quality image generation and editing | Marketing assets, product imagery, design |
| **Veo** | Text/image → video | Video generation | Campaigns, previsualisation, training content |
| **Chirp** | Speech | Speech recognition and synthesis at scale | Contact centres, voice interfaces, accessibility |
| **Lyria** | Music/audio | Music and audio generation | Creative audio |

**Tier-selection rule:** flagship for the hardest reasoning; Flash-tier for production scale and
agents; Flash-Lite for simple, high-volume tasks; Nano/open models for device, offline, or
sovereignty needs.

---

## Master offerings to task table

| Offering | Intended task |
| --- | --- |
| Gemini app | Everyday personal assistance: write, summarise, translate, generate images |
| Gemini Advanced | Same plus frontier capability and enterprise-grade protections |
| Gems | Reusable personalised assistants with fixed instructions |
| Gemini for Google Workspace | Gen AI inside Gmail, Docs, Sheets, Slides, Meet |
| Gemini Enterprise | Organisation-wide governed internal search + conversation agents (formerly Agentspace) |
| Gemini Notebook | Research/Q&A grounded in your own uploaded sources (formerly NotebookLM) |
| Gemini for Google Cloud | Build, code, debug, and secure on Google Cloud |
| Gemini Enterprise for Customer Experience | Contact-centre AI: CX Agent Studio, Agent Assist, CX Insights on CCaaS |
| Agent Platform (Gemini Enterprise Agent Platform) | Unified platform to build, train, tune, deploy, manage ML/gen AI (formerly Vertex AI) |
| Model Garden | Discover/use first-party, third-party, open-source models |
| Model Builder / custom training | Train fully custom models with ML frameworks |
| Agent Platform AutoML | Train custom models with minimal technical expertise |
| Agent Studio | Build/deploy production-grade gen AI apps and agents (formerly Vertex AI Studio) |
| Google AI Studio | Free, fast prototyping with the Gemini API |
| Agent Search | Enterprise search/recommendation + prebuilt RAG over your content |
| RAG APIs | Custom retrieval-augmented generation pipelines |
| Grounding with Google Search | Ground answers in current public world knowledge |
| Agent Runtime | Managed agent deployment, scaling, observability (formerly Agent Engine) |
| Agent Garden | Prebuilt agent templates |
| Agent Development Kit (ADK) | Code-first multi-agent development framework |
| A2A protocol | Cross-platform agent communication |
| MCP | Connect models/agents to tools and data sources |
| Model Armor | Screen prompts/responses for injection, jailbreak, data leakage |
| Model Registry | Version and organise models |
| Model Monitoring | Track performance, detect drift |
| Feature Store | Manage/serve features consistently |
| Pipelines | Automate MLOps workflows |
| Speech-to-Text | Transcribe speech, audio, video |
| Text-to-Speech | Generate natural speech |
| Translation API | Translate text, sites, audio, video |
| Document Translation API | Translate documents, preserve layout |
| Document AI | Extract data from documents, automate capture, summarise |
| Cloud Vision | Analyse image content |
| Cloud Video Intelligence | Analyse video content |
| Natural Language API | Sentiment, classification, entities |
| Customer Experience Agent Studio | Customer-facing virtual agents |
| Agent Assist | Real-time help for live human agents |
| Customer Experience Insights | Analytics across customer conversations |
| IAM | Control who can access which resources |
| Security Command Center | Security posture visibility and findings |
| VPC Service Controls | Prevent data exfiltration with service perimeters |
| Cloud KMS / CMEK | Customer-managed encryption keys |
| Gemini Nano + LiteRT | On-device/edge gen AI |

---

## Prompting techniques

| Technique | What it is | Use when |
| --- | --- | --- |
| **Zero-shot** | No examples; rely on model capability | Simple, common tasks |
| **One-shot** | One example | Format/style needs a nudge |
| **Few-shot** | Several examples (3–5) | Consistent taxonomy, formatting, tone, edge cases |
| **Role prompting** | Assign a persona | Audience, expertise, or voice matters |
| **Prompt chaining** | Sequence of prompts, each feeding the next | Multi-stage work; intermediate checks; different data per step |
| **Chain-of-thought** | Reason through intermediate steps | Maths, logic, planning, multi-constraint problems |
| **ReAct** | Reason **and** act with tools | Agents, live lookups, system interaction |
| **Metaprompting** | Model generates/modifies/interpret prompts | Scaling prompt creation and standardisation |
| **Templates & saved info** | Reusable prompts and stored context | Consistency across teams and turns |
| **Gems** | Packaged assistants with fixed instructions | Turn a good prompt into a reusable colleague |

---

## Sampling parameters

| Parameter | Controls | Lower it for | Raise it for |
| --- | --- | --- | --- |
| **Token count** | Unit of text consumed/produced; drives cost and limits | Cost/latency control | Longer inputs/outputs (watch cost) |
| **Temperature** | Creativity/randomness | Facts, extraction, support, compliance, code | Brainstorming, copywriting, ideation |
| **Top-p** | Cumulative probability pool of likely tokens | Precision tasks | Creative exploration |
| **Output length** | Maximum generated text | Terse answers, cheaper responses | Reports, long documents |
| **Safety settings** | Block/reduce harmful content | Never removed in governed deployments | Only tuned with approval and testing |

---

## Grounding and RAG

**Grounding data types**

| Type | Meaning | Google mechanism |
| --- | --- | --- |
| First-party (enterprise) | Your private content | Agent Search / prebuilt RAG, RAG APIs, data stores |
| Third-party | Licensed/external or connected systems | Connectors in your RAG pipeline |
| World | Public, current information | Grounding with Google Search |

**RAG steps:** 1) **Retrieval** from external sources → 2) **Augmentation** of the prompt →
3) **Generation** from that context → 4) optional **Iteration**.

**What RAG changes:** reduces hallucination, adds post-cutoff freshness, enables citations and
auditability, supports access control. It does **not** replace prompt engineering, and it is not
the same as a large context window.

**Grounding vs fine-tuning vs prompting**

| Approach | Changes | Fixes | Doesn't fix |
| --- | --- | --- | --- |
| Prompt engineering | Input | Format, tone, reliability | Missing knowledge |
| Grounding / RAG | Context | Hallucination, freshness, citations | Deep behaviour change |
| Fine-tuning | Model | Style, format, domain conventions | Current facts (still hallucinates) |

---

## Foundation model limitations and mitigations

| Limitation | Mitigation | Control |
| --- | --- | --- |
| Data dependency | Representative, high-quality, complete data | Data governance, quality checks |
| Knowledge cutoff | Grounding (Google Search), refreshed RAG index | Freshness SLAs, disclosure |
| Hallucination | Grounding/RAG with citations, lower temperature | HITL on high-stakes output, evaluation |
| Bias | Bias testing, representative data, prompt design | Fairness review, disaggregated metrics, AI Principles |
| Fairness | Deliberate assessment across groups | Governance sign-off, monitoring |
| Edge cases | Real-world edge-case testing, red teaming | HITL, escalation paths, fallbacks |

**Also nameable:** context-window limits, cost/latency at scale, and non-determinism (the same
prompt can produce different outputs).

## Monitoring and evaluation

| Practice | Mechanism |
| --- | --- |
| Automatic model upgrades | Managed lifecycle on Agent Platform |
| KPIs | Business + model metrics with baselines |
| Security patches and updates | Managed platform patching; SAIF-aligned controls |
| Versioning | **Model Registry** |
| Performance tracking | Model metrics + **Model Monitoring** |
| Drift monitoring | **Model Monitoring** (data drift, concept drift, skew) |
| Data/feature management | **Agent Platform Feature Store** |
| Pipeline automation | **Agent Platform Pipelines** |

## Human in the loop (HITL)

| Pattern | Applies to |
| --- | --- |
| Content moderation | User-generated content, marketplaces |
| Sensitive applications | Healthcare, finance, legal |
| High-risk decision-making | Credit, hiring, eligibility, medical guidance |
| Pre-generation review | Validation before deployment (catch errors/bias pre-impact) |
| Post-generation review | Continuous review after launch (improve and adapt) |

---

## Responsible AI

**Definition:** ensuring AI applications don't cause harm and are used ethically — throughout
the entire lifecycle, from data preparation and training to deployment and monitoring.

| Dimension | Controls |
| --- | --- |
| Transparency | Disclosures, provenance labelling, documentation, model cards |
| Privacy | Minimisation, consent, retention limits, **anonymisation/pseudonymisation**, access control |
| Data quality, bias, fairness | Representative data, bias testing, disaggregated evaluation, HITL |
| Accountability | Named owners, governance, approvals, logging, escalation, incident response |
| Explainability | Citations from grounding, reasoning summaries, plain-language explanations |
| Safety & security | Safety settings, red teaming, SAIF controls, Model Armor |

**Google's seven AI Principles:** 1) Be socially beneficial. 2) Avoid creating or reinforcing
unfair bias. 3) Be built and tested for safety. 4) Be accountable to people. 5) Incorporate
privacy design principles. 6) Uphold high standards of scientific excellence. 7) Be made
available for uses that accord with these principles.
Google also names applications it will **not** pursue (overall harm, weapons, abusive
surveillance) — a template for your own "we will not build this" list.

**Anonymisation vs pseudonymisation:** anonymisation is irreversible; pseudonymisation keeps a
mapping key, so the data generally remains personal data and needs protection.

---

## Secure AI and SAIF

**Secure AI** = protecting AI applications from malicious attacks and misuse, across the ML
lifecycle. **SAIF** = Google's Secure AI Framework: a technology-agnostic, conceptual framework
to help organisations manage AI/ML model risks and security.

**The six core elements**

1. Expand strong security foundations to the AI ecosystem.
2. Extend detection and response to bring AI into an organisation's threat universe.
3. Automate defences to keep pace with existing and new threats.
4. Harmonise platform-level controls for consistent security across the organisation.
5. Adapt controls to adjust mitigations and create faster feedback loops for AI deployment.
6. Contextualise AI system risks in surrounding business processes.

**SAIF components (where controls are mapped):** **Data · Infrastructure · Model ·
Application**, with assurance and governance controls (red teaming, vulnerability management,
threat detection, incident response, policy and education) spanning all.

**Threats to name:** prompt injection, jailbreak, data poisoning, training-data extraction,
model theft, data exfiltration, insecure output handling, denial of service/resource abuse.

**Security across the lifecycle:** data (provenance, sanitisation, privacy controls) → training
(secure tooling, access/integrity, model inventory) → deployment (least privilege, perimeters,
encryption) → operations (monitoring, red teaming, patching, incident response, agent
observability).

## Security controls map

| Control | Purpose | Memory hook |
| --- | --- | --- |
| Secure-by-design infrastructure | Hardened foundations you inherit | The vault is already built |
| IAM | Who can access which resources | Who can do what |
| Security Command Center | Posture visibility, findings, threats | The dashboard that tells you what's wrong |
| Workload monitoring | Detect anomalies in running workloads | Watch it while it runs |
| Model Armor | Screen prompts/responses for injection and leakage | The bouncer |
| VPC Service Controls | Prevent exfiltration with perimeters | Fence the data |
| Cloud KMS / CMEK | Customer-managed encryption keys | Bring your own keys |
| Cloud Logging / audit logs | Evidence and traceability | Evidence |
| Data residency controls | Keep data in approved regions | Data stays home |

---

## Cloud AI APIs

| API | Converts / does | Typical task |
| --- | --- | --- |
| Speech-to-Text | Audio/video → text | Transcribe calls, subtitles, voice input |
| Text-to-Speech | Text → speech | Voice UIs, accessibility, IVR |
| Translation | Text/site/audio/video → another language | Localisation, multilingual support |
| Document Translation | Formatted documents → translated, layout preserved | Manuals, contracts, filings |
| Document AI | Documents → structured data | Invoice/form processing, data capture, summarisation |
| Cloud Vision | Images → insights | Moderation, tagging, visual search, OCR |
| Cloud Video Intelligence | Video → insights | Video search, recommendation, media analysis |
| Natural Language | Unstructured text → insight | Sentiment, classification, entity extraction |
| Gemini API (Agent Platform / AI Studio) | Prompts → generated content | Anything generative: chat, summarise, extract, reason, agents |

---

## ML lifecycle and Google Cloud tools

| Stage | What happens | Example Google Cloud tools |
| --- | --- | --- |
| Data ingestion and preparation | Collect, clean, transform, govern data | Cloud Storage, BigQuery, Pub/Sub, Dataflow, Dataproc, Dataplex |
| Model training | Create the model from data | Agent Platform training, AutoML, Model Garden, Colab Enterprise, GPUs/TPUs |
| Model deployment | Make the model usable | Agent Platform endpoints, Model Registry, Cloud Run, GKE, LiteRT for edge |
| Model management | Version, monitor, retrain, govern | Model Registry, Model Monitoring, Feature Store, Pipelines |

---

## Model selection factors

1. **Modality** — do input/output types match the task?
2. **Context window** — how much must be in view, at what cost?
3. **Security** — residency, access, encryption, compliance.
4. **Availability and reliability** — uptime, redundancy, DR, regional coverage.
5. **Cost** — tokens, serving, retrieval, human review, total cost of ownership.
6. **Performance** — accuracy, speed, efficiency on *your* evaluation set.
7. **Fine-tuning and customisation** — adapt behaviour only when justified.

**Path order:** prebuilt app → API + prompting/grounding → AutoML/prebuilt RAG → custom
training/fine-tuning. Always choose the **lightest solution that satisfies the constraints**.

**Planning factors:** needs — **scale, customisation, user interaction, privacy, latency,
connectivity**; resources — **people, money, time**.

**Strategy formula:** top-down vision + bottom-up experimentation; prioritise focused use cases;
invest in data, capabilities, and talent; manage change; measure impact; champion responsible AI;
improve continuously.

---

## Measuring business value

| Category | Example metrics |
| --- | --- |
| Revenue growth | Conversion, upsell, faster quoting |
| Cost reduction | Cost per document/interaction, error remediation |
| Productivity | Time per task, throughput, handling time |
| Customer experience | CSAT, NPS, first-contact resolution, response time |
| Risk & compliance | Incident rate, audit findings, control coverage |
| Speed / innovation | Time to market, asset turnaround |

**Measurement discipline:** baseline first → KPI in business terms → evaluation set with edge
cases → adoption tracked → unit economics modelled → honest attribution → continuous reporting.

---

## Naming changes

| Older name | Current name |
| --- | --- |
| Vertex AI | Gemini Enterprise Agent Platform (Agent Platform) |
| Vertex AI Studio | Agent Studio |
| Vertex AI Search / Search and Conversation | Agent Search |
| Agentspace | Gemini Enterprise |
| NotebookLM | Gemini Notebook |
| Vertex AI Agent Engine | Agent Runtime |
| Customer Engagement Suite, Conversational Agents, Conversational Insights | Gemini Enterprise for Customer Experience: CX Agent Studio, Agent Assist, Customer Experience Insights |

Both forms may appear; translate silently and answer the current concept.

---

## Acronyms

| Acronym | Meaning |
| --- | --- |
| ADK | Agent Development Kit |
| AI / ML / DL | Artificial intelligence / machine learning / deep learning |
| API | Application programming interface |
| A2A | Agent2Agent protocol |
| CCaaS | Contact Center as a Service |
| CMEK | Customer-managed encryption keys |
| CoT | Chain-of-thought |
| FM | Foundation model |
| HITL | Human in the loop |
| IAM | Identity and Access Management |
| KPI | Key performance indicator |
| LLM | Large language model |
| MCP | Model Context Protocol |
| MLOps | Machine learning operations |
| NLP | Natural language processing |
| RAG | Retrieval-augmented generation |
| ReAct | Reason and act |
| SAIF | Secure AI Framework |
| SCC | Security Command Center |
| TPU | Tensor Processing Unit |
| VPC-SC | VPC Service Controls |

---

## High-frequency topics

Ranked by how often they drive correct answers in practice — master these first:

1. **Grounding vs RAG vs fine-tuning** — facts vs behaviour.
2. **Google AI Studio vs Agent Studio** — prototype vs production.
3. **Agent Search (your data) vs Grounding with Google Search (world data).**
4. **Gemini app vs Gemini for Workspace vs Gemini Enterprise vs Gemini Notebook.**
5. **Prompting techniques and when to use each.**
6. **Sampling parameters** — temperature and top-p direction.
7. **The eight Cloud AI APIs and their tasks.**
8. **HITL pre- vs post-generation.**
9. **Model Monitoring, Model Registry, Feature Store, Pipelines.**
10. **Responsible AI vs secure AI; SAIF's six elements; IAM vs Security Command Center vs Model Armor.**
11. **Model selection factors and tier choice (Pro vs Flash vs Flash-Lite vs Nano vs Gemma).**
12. **Value measurement: baseline → KPI → business metric.**
13. **The 2026 naming changes.**
14. **The five layers of the gen AI landscape** and one product per layer.
15. **The four value verbs** — create, summarize, discover, automate.

---

**Back to:** [Study plan and index](README.md) ·
[Final exam mindset](final-exam-mindset.md) ·
[Recall quiz](session-6-recall-quiz.md) ·
[Answer key](answer-key.md)
