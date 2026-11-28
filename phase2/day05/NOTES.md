# Day 5 — Chunking (where retrieval quality is won or lost)

## Why chunk at all
- Real docs are long. Can't embed a whole doc as one vector:
  1. **Meaning dilutes** — one vector averaging 50 pages drowns the specific fact.
  2. Retrieved text wouldn't fit/focus (context wall).
- So split docs into **chunks**; embed each chunk; the **chunk becomes the unit of retrieval**.
- Chunking quality **caps the whole system's accuracy** — it's upstream of everything. Good prompting can't fix a retrieval that hands over half a fact.

## Naive fixed-size chunking (the trap)
- Cut every N characters → breaks badly:
  - **Mid-word cuts** ("Financial C" | "rimes...") → garbled text → bad embeddings.
  - **Facts split across chunks** → neither chunk fully answers → forces incomplete answers / guessing.

## Better: natural boundaries + overlap
- **Fix 1 — split on natural boundaries** (paragraphs via `\n\n`, or sentences) so each chunk is a coherent idea.
  - Pure paragraph split breaks when paragraphs are huge / tiny / absent → need size bounding too.
- **Fix 2 — overlap**: each chunk shares a bit (e.g. the last sentence) with the next, so a fact on a boundary survives whole in ≥1 chunk.
- [pro] The two tuning knobs: **chunk size** and **overlap**.
  - Too small → loses context ("it must be filed in 30 days" — what is "it"?).
  - Too big → dilutes meaning, retrieves irrelevant text, costs more.
  - More overlap → fewer split facts, but more storage/duplicate retrieval.
  - No universal "right" size — **choose it by measuring (evals), not guessing.**

## The practical chunker (sentence-packing + overlap)
1. Split text into sentences.
2. Pack sentences into a chunk until the next would exceed `max_chars`.
3. Close the chunk; **seed the next chunk with the last sentence** (overlap); continue.
```python
for sentence in sentences:
    if current_len + len(sentence) > max_chars and current:
        chunks.append(" ".join(current))
        current = [current[-1]]          # overlap seed
        current_len = len(current[-1])
    current.append(sentence); current_len += len(sentence)
if current: chunks.append(" ".join(current))
```
- [pro] `max_chars` is a **soft target, not a hard cap** — the overflow check runs after appending, so a chunk can run slightly over. Production splitters (e.g. LangChain `RecursiveCharacterTextSplitter`) handle this + fall back paragraph→sentence→word by size. We built the core by hand.

## Plugged into RAG — same pipeline, real document
- Only change from Day 4: `documents = chunk_text(load_document(path))` instead of hand-typed list. The chunk IS the document. Everything downstream (embed→retrieve→ground→cite→generate) unchanged.
- Verified: "What does FinCEN stand for?" → intact FinCEN chunk → "Financial Crimes Enforcement Network [1]". (Naive chunking had split "Financial Crimes" — would have failed.)
- **Overlap seen live:** the registered-agent requirement sentence appeared in BOTH retrieved chunks 1 and 2 → model cited `[1][2]`.

## Citations = the trust feature
- Number retrieved chunks `[1][2][3]` in the context; prompt tells the model to cite the source after each fact.
- `[1]` in the answer = "this fact came from retrieved chunk 1" → human can verify → essential for compliance/regulated work.

## Modules & imports (project structure)
- Any `.py` file is a **module**; `from smart_chunking import load_document, chunk_text` reuses its functions (DRY — don't duplicate).
- **Importing runs the whole file** → wrap demo/run code in `if __name__ == "__main__":` so it runs only when executed directly, not on import.
- Python finds imports in the same folder as the script being run.
- [pro] First step from "pile of scripts" → "codebase": one function, one home, imported where needed. Scales to chunking.py / retrieval.py / rag.py modules.

## In my own words
-
-
-