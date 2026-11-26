import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROP_API_KEY"))

# THE FOLDER — starts with just the system instruction
messages = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers short."},
]

print("Chat started. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input == "quit":
        break

    # put the user's new message INTO the folder
    messages.append({"role":"user", "content":user_input})

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
    )

    reply = response.choices[0].message.content
    print("Assistant:", reply, "\n")

    # put the model's reply INTO the folder too, so next turn remembers it
    messages.append({"role": "assistant", "content": reply})