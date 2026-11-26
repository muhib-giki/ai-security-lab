import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"

# build a deliberately enormous input (~ hundreds of thousands of tokens)
huge_text = "The quick brown fox jumps over the lazy dog. " * 40000

print(f"Input length: {len(huge_text)} characters (~{len(huge_text)//4} tokens est.)")

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": huge_text + "\n\nSummarize the above."}],
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("REQUEST FAILED:")
    print(e)