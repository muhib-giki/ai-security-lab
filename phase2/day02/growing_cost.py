import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"

messages = [{"role": "system", "content": "You are a helpful assistant. Keep answers short."}]

# simulate a 5-turn conversation
turns = [
    "My name is Muhibullah.",
    "I run a software agency.",
    "I'm learning AI engineering.",
    "What's my name?",
    "What do you know about me so far?",
]

running_total = 0

for i, user_text in enumerate(turns, start=1):
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(model=MODEL, messages=messages)
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    u = response.usage
    running_total += u.total_tokens
    print(f"Turn {i}: prompt={u.prompt_tokens:4}  completion={u.completion_tokens:4}  " f"total={u.total_tokens:4}  running={running_total}")