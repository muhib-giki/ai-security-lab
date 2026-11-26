# Day 3 — Embeddings & retrieval (the core of RAG)

## Embeddings
- An **embedding** turns text into a fixed-length vector of numbers that captures **meaning**.
- The key property: **similar meaning → nearby vectors; different meaning → far-apart vectors.** Meaning becomes geometry.
- [pro] The embedding model is a **separate, dedicated model** from the chat LLM — trained specifically so semantic similarity = vector closeness. Don't reuse the chat model for this.
- `sentence-transformers` runs an embedding model **locally, free** (no API). Used `all-MiniLM-L6-v2` → **384-dim** vectors.
- Any text (short or long) → exactly the same vector length. The numbers are meaningless individually; meaning is in the pattern.
- [pro] More dimensions = more nuance capacity, more storage/compute. Production models ~384–3072+ dims; model choice (quality/size/domain) is a real decision.

## Cosine similarity (how to measure "close")
- Measures the **angle** between two vectors, ignoring length: 1 = same direction (same meaning), 0 = perpendicular (unrelated), −1 = opposite.
- Formula: `cos(A,B) = (A · B) / (|A| · |B|)`
  - `A · B` dot product = multiply element-wise, sum (big when arrows point similarly).
  - `|A|` magnitude = **√(sum of squares)** = length of the arrow (Pythagoras in N dimensions). NOT absolute value — for a vector, `|A|` means length; absolute value is the 1D case of the same "distance from zero" idea.
  - Dividing by both lengths cancels magnitude, leaving only the angle.
- [pro] Cosine (angle) not Euclidean (distance) because **direction encodes meaning; magnitude is mostly noise** (correlates with length). Cosine is the near-universal default for semantic search.
- numpy: `np.dot(a,b)`, `np.linalg.norm(a)`.

### Measured result
- Two LLC questions with almost NO shared words → **0.622** (high). Keyword search would score ~0. Embeddings caught the meaning.
- LLC ↔ "capital of France" → **~0.01** (unrelated).
- [pro] Absolute cosine values are **model-specific** — don't hardcode "related if > 0.7". Calibrate per model; the **ranking** matters more than the absolute number. Small model = lower scores; a stronger model would push related pairs to 0.8+.

## Retrieval = semantic search (the "R" in RAG)
Two phases:
1. **Indexing (once):** embed the whole knowledge base, store the vectors.
2. **Querying (each time):** embed just the query → compare to all doc vectors → return the closest top-k.
- Asymmetry: docs embedded once and reused; query embedded fresh every time.
```python
doc_embeddings = model.encode(documents)      # index once
# per query:
q_emb = model.encode(query)
scored = [(cosine(q_emb, e), doc) for doc, e in zip(documents, doc_embeddings)]
scored.sort(reverse=True)
top = scored[:top_k]
```
- Proven: queries worded differently from the docs still retrieved the right doc ("who receives legal papers" → registered agent doc). Meaning, not keywords.

## What this toy is still missing (→ next days)
- [pro] **No generation yet** — it only retrieves raw docs. RAG = **Retrieval + Generation**: feed retrieved docs to the LLM → grounded, cited answer. (Day 4)
- [pro] Docs here are one-sentence facts. Real documents are long → must be **chunked**. (later)
- [pro] **Brute-force search** (compare to every doc) is fine for small sets; millions of docs need a vector DB / approximate nearest neighbor index (FAISS, HNSW). Same math, made fast. (later)

## Python
- `zip(a, b)` pairs two lists by position; unpack in the loop (`for x, y in zip(...)`). Stops at the shorter list.
- `list.sort(reverse=True)` sorts descending; on a list of tuples, sorts by the first element.
- `scored[:top_k]` takes the first k after sorting.

## In my own words
-
-
-