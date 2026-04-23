# 🚀 AI Reflection System

An evolving AI system that **generates, evaluates, improves, and remembers its own answers** — step by step.

---

## 🧠 Project Overview

This project focuses on building **intelligent AI pipelines**, not just basic API calls.

Each day introduces a new capability:

* From simple responses
* → to reasoning
* → to self-evaluation
* → to safety control
* → to memory-based conversations

---

## 📅 Progress Breakdown

### 🔹 Day 1 — Basic AI Response

* Simple LLM call using OpenRouter API
* Input → Question
* Output → Answer

---

### 🔹 Day 2 — Writer → Critic → Improver

* AI generates an answer
* AI reviews its own answer
* AI improves based on feedback

👉 Introduced **multi-step AI pipeline**

---

### 🔹 Day 3 — Confidence Score

* AI returns:

  * answer
  * confidence (0–100)
  * reason

👉 Added **self-awareness layer**

---

### 🔹 Day 4 — Hallucination Control 🛡️

* System checks confidence before trusting AI

#### Logic:

* If confidence < 60 → ❌ "I don't know"
* If confidence ≥ 60 → ✅ Show answer

👉 Introduced **AI safety + guardrails**

---

### 🔹 Day 5 — Step-by-Step Reasoning 🧠

* Compared:

  * normal answers
  * step-by-step reasoning answers

👉 Forces AI to **think before answering**

---

### 🔹 Day 6 — Memory System 🗂️

* Stores past Q&A in a JSON file
* Uses previous conversations in new responses

👉 Introduced **stateful AI (memory-based system)**

---

## ⚙️ System Flow

```text
User Question
     ↓
Prompt Engineering (rules + memory)
     ↓
LLM Response
     ↓
JSON Parsing
     ↓
Control Logic (confidence / safety)
     ↓
Memory Storage (Day 6)
     ↓
Final Answer
```

---

## 🛠️ Tech Stack

* Python
* OpenRouter API (LLMs)
* Requests
* JSON
* dotenv
* LangChain (Day 2)

---

## 🔐 Environment Setup

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

### Example (Day 6 Memory System):

```bash
cd day6_memory
python main.py
```

---

## 📌 Example

**Input:**

```
My name is Pranav
```

**Next Input:**

```
What is my name?
```

**Output:**

```
Your name is Pranav.
```

👉 Shows memory working

---

## 🎯 Key Learnings

* Prompt engineering is powerful
* AI needs validation layers
* Confidence helps control hallucination
* Memory makes AI conversational
* Systems > single API calls

---

## 🚀 Future Improvements

* 🔍 Smart memory (vector search / FAISS)
* 🧠 Better reasoning control
* 📊 Confidence calibration
* 🤖 Multi-agent systems

---

## 👨‍💻 Author

Pranav Agarwal

---

⭐ If you found this useful, consider giving a star!
