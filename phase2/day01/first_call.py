import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads your .env file and loads the key into the environment

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Keep answers short."},
        {"role": "user", "content": "In one sentence, what is an LLC?"},
        # {"role": "user", "content": "What did I just ask you?"},
    ],
)

print(response.choices[0].message.content)