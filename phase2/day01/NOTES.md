# Day 1 — Talking to an LLM

## What an LLM is
- It predicts the next chunk of text, over and over. "Chat", "reasoning", "coding" are all that one trick at scale.
- Just **text in, text out** — calling it is an ordinary web request to a model server.
- **Stateless:** the model remembers NOTHING between calls. Each call is the first time, from its point of view.

## The "folder" model (the key idea)
- A chatbot feels like it remembers only because the app **resends the entire conversation every time**.
- The conversation list (`messages`) = a folder you hand the model on every call. The model reads the folder, answers, forgets everything.
- **The folder remembers, not the model. You (the code) control the folder.**

## The messages format
- You send a **list of messages**, each with a role:
  | Role | Purpose |
  |---|---|
  | `system` | sets behaviour ("You are a helpful assistant. Be concise.") |
  | `user` | what the human says |
  | `assistant` | what the model previously replied (how you give it "memory") |
- Reply comes back at `response.choices[0].message.content`.

## Three consequences (matter later)
1. **You create memory** by keeping the list and resending it — the model contributes nothing.
2. **Cost grows over a conversation** — each turn resends everything before it. Turn 20 sends 20 turns of text.
3. **The model trusts whatever is in the folder** — it can't tell who put a line there. (→ Phase 3 security: an attacker who sneaks text into the folder gets it treated as real.)

## The chat loop (creates the illusion of memory)
Each turn, in order:
1. append the user message to `messages`
2. send the WHOLE list to the model
3. append the model's reply to `messages`  ← the step people forget; keep BOTH sides

```python
messages = [{"role": "system", "content": "..."}]
while True:
    messages.append({"role": "user", "content": user_input})
    r = client.chat.completions.create(model=MODEL, messages=messages)
    reply = r.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
```

## Setup / practical
- **Provider:** Groq (free API key at console.groq.com). OpenAI-style format → transfers everywhere.
- **Key handling:** put it in a `.env` file (`GROQ_API_KEY=...`), add `.env` to `.gitignore`, load with `python-dotenv`'s `load_dotenv()`. Never hardcode a key or commit it.
- `pip install groq python-dotenv`
- `load_dotenv()` looks for `.env` in the folder you RUN from (and parents) — run from the project root.
- **Model names are provider-specific and change** — list them with `client.models.list()` instead of memorizing. (Using `qwen/qwen3.8-27b`.)
- A `404 model_not_found` = bad/unavailable model name, NOT an auth problem.
- Groq's list also has special-purpose models: whisper (speech→text), orpheus (text→speech), **llama-prompt-guard** (prompt-injection classifier — a Phase 3 defense), gpt-oss-safeguard (moderation).

## In my own words
-
-
-