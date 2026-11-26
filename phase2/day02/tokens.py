import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"

def ask(text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": text}]
    )

    usage = response.usage
    print(f"Input: {text!r}")
    print(f"  prompt_tokens:     {usage.prompt_tokens}")
    print(f"  completion_tokens: {usage.completion_tokens}")
    print(f"  total_tokens:      {usage.total_tokens}")
    print()

ask("Hi")
ask("Explain what a limited liability company is in one sentence.")
ask("Write a detailed 3-paragraph explanation of how LLCs are taxed in the US.")