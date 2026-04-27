import requests
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# 🔹 LLM CALL
def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data, timeout=20)
    return response.json()["choices"][0]["message"]["content"]


# 🔹 NORMALIZE TEXT → NUMBER
def normalize_expression(expr):
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10"
    }

    expr = expr.lower()
    for word, num in mapping.items():
        expr = expr.replace(word, num)

    return expr


# 🔹 CALCULATOR TOOL
def calculator_tool(expression):
    try:
        expression = normalize_expression(expression)
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"


# 🔹 SEARCH TOOL
def search_tool(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" in results:
            top_results = results["organic_results"][:3]

            output = ""
            for r in top_results:
                output += f"{r.get('title')} - {r.get('snippet')}\n"

            return output

        return "No results found"

    except Exception as e:
        return f"Search error: {e}"


# 🔹 TOOL EXECUTOR
def execute_tool(action):
    action = action.replace("ACTION:", "").strip()

    if action.lower().startswith("calculator"):
        expr = action.split(":", 1)[-1].strip()
        return calculator_tool(expr)

    elif action.lower().startswith("search"):
        query = action.split(":", 1)[-1].strip()
        return search_tool(query)

    else:
        return "No valid tool used"


# 🔁 AGENT LOOP WITH RETRY
def run_agent(goal):
    print("\n🎯 Goal:", goal)

    observation = ""

    for step in range(5):
        print(f"\n🔁 Step {step+1}")

        prompt = f"""
You are an AI agent with tools.

Available tools (ONLY use these):
1. calculator
2. search

STRICT RULES:
- DO NOT invent new tools
- Use calculator ONLY for math
- Use search for information
- If tool fails → try again differently
- Stop ONLY when goal is fully solved

Goal:
{goal}

Previous observation:
{observation}

Return ONLY:
PLAN: ...
ACTION: tool_name: input
DONE: yes/no
"""

        output = call_llm(prompt)
        print("🧠 LLM OUTPUT:\n", output)

        # 🔹 Extract latest ACTION safely
        action_lines = [line for line in output.split("\n") if line.strip().startswith("ACTION")]
        action = action_lines[-1] if action_lines else ""

        result = execute_tool(action)
        print("⚙️ TOOL RESULT:", result)

        # 🔁 RETRY LOGIC
        if "error" in result.lower() or "no valid" in result.lower():
            print("⚠️ Tool failed, retrying...")

            retry_prompt = f"""
Previous action failed.

Goal:
{goal}

Bad action:
{action}

Error:
{result}

Fix the mistake and try again.

Return ONLY:
PLAN: ...
ACTION: tool_name: input
DONE: no
"""

            retry_output = call_llm(retry_prompt)
            print("🔁 RETRY OUTPUT:\n", retry_output)

            retry_lines = [line for line in retry_output.split("\n") if line.strip().startswith("ACTION")]
            retry_action = retry_lines[-1] if retry_lines else ""

            result = execute_tool(retry_action)
            print("⚙️ RETRY RESULT:", result)

            action = retry_action

        # 🔹 Update observation
        observation += f"\nAction: {action}\nResult: {result}"

        # 🔹 Stop condition (safe)
        if "done: yes" in output.lower() and "error" not in result.lower():
            print("\n✅ Goal Completed!")
            print("\n🎯 FINAL ANSWER:", result)
            break

    print("\n🏁 Final Observation:\n", observation)


# 🧪 RUN
if __name__ == "__main__":
    goal = input("Enter your goal: ")
    run_agent(goal)