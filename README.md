# 🤖 **AI Customer Support Agent — Multi-Agent, Tool-Oriented Architecture**

This repository contains an **AI-powered customer support system** designed for realistic e-commerce scenarios.  
The system uses a **multi-agent, multi-tool architecture** to support **product discovery, recommendations, comparisons, and preference-aware interactions** over a real electronics dataset.

---

## 🧱 **System Overview**

The system is composed of two main agents:

- **Customer Support Agent**  
  Responsible for **user interaction, intent routing, session memory, and dialogue management**.

- **Product Catalog Agent**  
  A **tool-specialized agent** that provides structured access to a real electronics product catalog via **A2A (agent-to-agent) communication**.

The agents communicate over a **REST-based A2A interface**, implemented with **FastAPI**.

---

## 🧩 **Framework & Agent Runtime (Google ADK)**

The system is built using **Google Agent Development Kit (ADK)**, which provides the core abstractions for:
- Defining LLM-based agents
- Managing tools and sub-agents
- Handling **agent-to-agent (A2A)** communication
- Maintaining **session-state memory**

ADK is used to orchestrate both the **Customer Support Agent** and the **Product Catalog Agent**, enabling controlled delegation, tool invocation, and stateful interactions.

---

## 📊 **Dataset Layer**

- Based on a real **Amazon electronics dataset (CSV)**

### Categories include (83 Categories):
- Headphones, TVs, Audio Systems  
- Computers, Mobile Devices  
- Accessories, Home Entertainment
- etc  

---

### **Column Detection**

The dataset loader automatically detects relevant columns:
- **Product name**
- **Brand**
- **Category**
- **Price (min / max)**
- **Availability**
- **Store**
- **Weight**
- **URLs (product & image)**

This makes the system robust to **dataset schema variations**.

---

## 🔤 **Tokenization & Category Matching**

To support flexible discovery queries, lightweight normalization and tokenization are applied:
- Case normalization  
- Punctuation stripping  
- Token overlap matching between user intent and dataset categories  

This enables partial matches such as:
- `"headphones"` → `"Bluetooth & Wireless Headphones"`
- `"home audio"` → `"Home Audio & Theater"`

No embedding models are used; matching is **deterministic and explainable**.

---

## 🧠 **Agents**

### 1️⃣ **Customer Support Agent**
- Powered by **Google Gemini (gemini-2.5-flash-lite)** for low-latency conversational reasoning.

#### **Responsibilities**
- Natural language interaction  
- Intent classification (**discovery vs. product lookup**)  
- Preference memory (**product & brand**)  
- Follow-up resolution  
- Delegation to catalog agent via **A2A**

#### **Prompt Engineering Techniques**
- **Policy-driven prompting** (explicit behavioral rules)  
- **Constraint-based prompting** (hard MUST / MUST NOT rules)  
- **Tool-oriented prompting** (forced delegation for factual data)  
- **Ordered-execution prompting** (memory before A2A transfer)

The agent **never invents product data** and always delegates catalog operations.

---

### 2️⃣ **Product Catalog Agent**
- Uses **Google Gemini (gemini-2.5-flash-lite)** for deterministic tool-oriented responses.


#### **Responsibilities**
- Product discovery (categories, brands, product lists)  
- Detailed product lookup  
- **Dataset-grounded responses only**

#### **Design Characteristics**
- **Tool-specialist agent** (no memory, no orchestration)  
- Deterministic tool routing via prompt policies  
- Explicit hallucination prevention  
- **Final-speaker guarantee** per A2A turn  

---

## 🛠️ **Tools**

### **Catalog Tools**
- `list_categories`
- `list_brands`
- `list_products`
- `get_product_info`

Each tool operates directly on the dataset using **Pandas**.

---

## 💾 **Memory Engineering**

The system uses **explicit session-state memory**, not implicit LLM memory.

### Stored state includes:
- `last_product`
- `second_last_product` (for comparisons)
- `preferred_brand`

#### **Memory Capabilities**
- Follow-up resolution (e.g. *“How much does it weigh?”*)  
- Product comparison without re-specifying names  
- Preference-aware recommendations  

---

## 🧩 **Context Engineering**

The system implements **state-driven context resolution**:

> Pronouns like *“this one”* or *“that one”* are resolved via **session state**, not guessing.

This avoids hallucination and ensures **deterministic behavior**.

---

## 🌐 **REST API & Server**

- **FastAPI** is used to expose the catalog agent as a service  
- **Uvicorn** runs the A2A server  
- Stateless, **request–response architecture**

---

## 📊 **Observability, Evaluation & Monitoring**

The system supports **observability and evaluation** using **adk web**, enabling:
- Inspection of agent decisions and tool calls
- Debugging multi-agent interactions
- Monitoring request flows and failures
- Qualitative evaluation of conversational behavior

This setup allows iterative improvement of prompts, policies, and agent coordination during development and deployment.

---

## 🔌 **Agent-to-Agent (A2A) Communication**

- The catalog agent is exposed as an **A2A REST service**
- Communication uses **HTTP via FastAPI**
- The customer support agent delegates catalog queries through **A2A calls**

This cleanly separates:
- **Reasoning & dialogue** (customer agent)
- **Data access & retrieval** (catalog agent)

---

## 🖥️ **User Interface (Gradio)**

A lightweight **Gradio-based chat interface** is provided for interactive testing and demonstration.

The UI allows users to:
- Chat with the customer support agent
- Trigger product discovery and comparisons
- Observe memory-aware follow-ups in real time

The Gradio UI connects to the customer-facing agent endpoint and is intended for development, demos, and qualitative evaluation.

---

## 🐳 **Docker & Deployment**

The project is **container-ready** and structured for:
- Local development  
- Containerized deployment  
- Future cloud migration (**Cloud Run / Kubernetes**)

Dockerization isolates:
- Dataset loading  
- A2A service  
- Agent runtime
- Containers are used for both local development and cloud deployment on **GCP Cloud Run**.

---

## ☁️ **Cloud Deployment (GCP)**

- Deployed on **Google Cloud Platform (GCP)**
- **Customer Support Agent** runs on **GCP Cloud Run**
- Exposes a **public HTTP endpoint** for user interaction
- Stateless, **request-driven architecture** suitable for scalable conversational AI workloads

---

## 🧪 **Key Capabilities Demonstrated**

- Product suggestion & recommendation  
- Brand discovery  
- Detailed product lookup (**price, availability, URLs**)  
- Product comparison  
- Preference memory  
- Multi-agent delegation  
- **Deterministic, hallucination-safe behavior**

---


## 📁 **Project Structure**
```text
product-support-bot/
├── src/
│   ├── agents/          # Multi-agent system (customer support, product catalog)
│   ├── server/          # FastAPI servers for each agent
│   ├── ui/              # Gradio UI
│   ├── tests/           # Test and debug scripts
│   ├── data/            # Non-sensitive datasets
│   └── main.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── .gcloudignore


## 🧠 **Summary of Techniques Used**
- **REST-based A2A communication**
- **Policy-driven prompt engineering**
- **Tool-oriented agent design**
- **State-aware prompting**
- **Session-state memory engineering**
- **State-driven context resolution**
