# AI Reflection System 🚀

This project implements a multi-step AI pipeline where the model:

1. Generates an answer
2. Reviews its own response
3. Improves the answer based on feedback

## Tech Stack

* FastAPI
* OpenRouter API
* Python

## How it works

User → AI Answer → AI Review → Improved Answer

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoint

```
/ask?question=your_question_here
```

## Example

Input:
What is Machine Learning?

Output:

* Answer
* Review
* Improved Answer

## Future Improvements

* Iterative improvement loop
* Score-based refinement
* Memory system
