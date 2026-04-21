# 🚀 AI Reflection System

An evolving AI system that **generates, evaluates, and improves its own answers** — step by step.

---

## 🧠 Project Overview

This project explores how to build **smarter AI pipelines** instead of just calling an API.

Each day adds a new capability:

* From simple responses → to reasoning → to self-evaluation → to safety control

---

## 📅 Progress Breakdown

### 🔹 Day 1 — Basic AI Response

* Simple LLM call using OpenRouter API
* Takes a question → returns an answer

---

### 🔹 Day 2 — Writer → Critic → Improver

* AI generates an answer
* AI reviews its own answer
* AI improves based on feedback

👉 Introduced **multi-step reasoning pipeline**

---

### 🔹 Day 3 — Confidence Score

* AI now returns:

  * answer
  * confidence (0–100)
  * reason

👉 Added **self-awareness layer**

---

### 🔹 Day 4 — Hallucination Control 🛡️

* System checks AI confidence before trusting it

#### Logic:

* If confidence < 60 → ❌ "I don't know"
* If confidence ≥ 60 → ✅ Show answer

👉 Prevents unreliable or hallucinated responses
👉 Introduces **AI safety + guardrails**

---

## ⚙️ How It Works

```text
User Question
     ↓
Prompt Engineering (rules + format)
     ↓
LLM Response (answer + confidence + reason)
     ↓
JSON Parsing
     ↓
Control Logic (confidence check)
     ↓
Final Answer (safe output)
```

---

## 🛠️ Tech Stack

* Python
* OpenRouter API (LLMs)
* Requests
* JSON parsing
* dotenv

---

## 🔐 Environment Setup

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```bash
cd day4_hallucination_control
python main.py
```

---

## 📌 Example

**Input:**

```
Who is the king of Mars?
```

**Output:**

```
"I don't know"
```

---

**Input:**

```
What is machine learning?
```

**Output:**

```
Machine learning is a type of artificial intelligence...
```

---

## 🎯 Key Learnings

* Prompt engineering is critical
* AI outputs are not always reliable
* Systems must **validate AI responses**
* Confidence-based filtering improves safety

---

## 🚀 Next Steps

* 🔁 Day 5 — Self-improving loop
* 🔍 Better validation strategies
* 📊 Confidence calibration

---

## 👨‍💻 Author

Pranav Agarwal

---

⭐ If you found this interesting, consider giving a star!
