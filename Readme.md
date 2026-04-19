# 🚀 AI Reflection System

A multi-step AI pipeline that **generates, critiques, and improves its own responses** using LLMs.

---

## 📌 Overview

This project demonstrates how to build **self-improving AI systems** by structuring multiple reasoning steps instead of relying on a single response.

---

## 🧠 Key Idea

Instead of asking AI for a single answer:

```text
User → AI → Final Answer ❌
```

We build a smarter system:

```text
User → Writer → Critic → Improved Answer ✅
```

---

## 📅 Project Progress

### 🔹 Day 1 — Reflection System

* Built a basic AI pipeline
* AI generates → reviews → improves
* Single model handles all steps

---

### 🔹 Day 2 — Writer + Critic System

* Introduced **multi-agent architecture**
* Separated roles:

  * ✍️ Writer → generates answer
  * 🧠 Critic → analyzes and finds issues
  * 🔁 Improver → refines the answer
* Used **LangChain chains** for modular design

---

## ⚙️ Tech Stack

* 🐍 Python
* 🔗 LangChain
* 🌐 OpenRouter API
* ⚡ Requests

---

## 🧩 Project Structure

```
ai-reflection-system/
 ├── day1_reflection_system/
 │    └── main.py
 ├── day2_writer_critic/
 │    └── day2.py
 ├── README.md
 ├── requirements.txt
```

---

## 🚀 How to Run

### 1. Clone the repo

```
git clone https://github.com/agarwalpranav0711/ai-reflection-system.git
cd ai-reflection-system
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Add API Key

Create a `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

---

### 4. Run

#### Day 1:

```
python day1_reflection_system/main.py
```

#### Day 2:

```
python day2_writer_critic/day2.py
```

---

## 🔥 Example Flow

```
Question → Writer → Critic → Improved Answer
```

---

## 🧠 What You Learn From This Project

* How to structure **AI pipelines**
* Difference between **single-call vs multi-agent systems**
* Using **LangChain for chaining logic**
* Building **self-improving AI systems**

---

## 🚀 Next Steps

* 🔁 Add iterative improvement loop (Day 3)
* 📊 Add scoring system for answers
* 🌐 Build API interface using FastAPI
* 🧠 Add memory to AI agents

---

## ⭐ If you found this useful, give it a star!
