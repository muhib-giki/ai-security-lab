# Day 4 — RAG end to end + grounding

## The RAG pipeline (3 steps)
```
question → 1. RETRIEVE (embed q, find top-k docs)  [Day 3]
         → 2. AUGMENT  (paste those docs into the prompt as "context")
         → 3. GENERATE (LLM answers FROM the context) [Day 1]
```
- "Augmented" = you put retrieved docs INTO the folder right before the question. The model reads them fresh each call.
- This is why RAG beats frozen training knowledge: current/private/specific docs supplied at question time.
- [pro] The context block is just more `messages`. The model can't tell who put text in the folder → this is also the Phase 3 security hole (a poisoned retrieved doc becomes trusted context).

## Grounding — what makes it trustworthy
- "Answer only from context" as an instruction is NOT guaranteed. The model's training priors can leak in or it can hallucinate.
- In compliance/tax, a confident wrong answer is worse than no tool. Trust rests on three behaviors:
  1. Answer ONLY from retrieved sources.
  2. **Cite** which source each claim came from (verifiable).
  3. Say **"I don't know"** when the answer isn't in the sources — the most important and hardest behavior.
- Technique: number the retrieved docs `[1] [2] [3]`, strict system prompt (use only context, cite sources, exact refusal if absent).
- `temperature=0` for factual/RAG tasks (deterministic, least "creative"). [pro] Factual → low temp; creative → high temp. Temp 0 reduces but doesn't eliminate hallucination.
- [pro] Models don't obey exact-output instructions perfectly (mine paraphrased the required refusal phrase). For strict control you need **structured output + code validation**, not just a prompt. (later)
- Verified: off-KB question ("Wyoming filing fee" — no amounts in KB) → it REFUSED and explained the boundary, instead of inventing a number. That's the product-grade behavior.

## Resilience — LLM calls fail, assume it
- Hit a real transient failure (crashed once, worked on restart = network blip / rate limit / timeout).
- **Principle: API calls are unreliable; production code must retry.** Wrap every model call in try/except + retries.
```python
def call_llm(messages, retries=3):
    for attempt in range(1, retries + 1):
        try:
            r = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
            return r.choices[0].message.content
        except Exception as e:
            if attempt < retries: time.sleep(2)
    raise RuntimeError("LLM call failed after retries")
```
- Also wrap the main loop so one failure doesn't end the session.
- [pro] Real retry logic: **exponential backoff** (1s, 2s, 4s) and retry only **transient** errors (rate limit, timeout), not permanent ones (bad key, invalid request).

## Python
- List comprehension `[expr for x in items]` = a compressed `for` loop that builds a list. Expand it mentally if unclear.
- `"\n".join(list_of_strings)` glues strings with newlines between.
- `enumerate(items, start=1)` loops with a counter → number sources `[1] [2]`.
- `return a, b` returns a pair; caller unpacks `x, y = f()`.
- `time.sleep(seconds)` pauses.

## What's still missing (→ next)
- [pro] Docs are one-sentence facts. **Real documents are long (pages)** → can't embed a whole doc as one vector, can't fit in context. Must **chunk**: split into passages, embed each. (Day 5 — where retrieval quality is won/lost)
- [pro] In-memory brute-force search → needs a vector store / ANN for scale. (later)
- [pro] No way yet to MEASURE if retrieval/answers are actually good → evals (the real differentiator, later).

## In my own words
-
-
-