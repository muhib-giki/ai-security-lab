# Day 2 — Tokens, cost, and the context window

## Tokens
- The model never sees words. Text → **tokens** (sub-word chunks) → integer IDs. Everything is measured/billed in tokens.
- Rough rule: **1 token ≈ 4 chars ≈ ¾ word** (English).
- Every response has a `usage` report:
  | field | meaning |
  |---|---|
  | `prompt_tokens` | tokens you SENT (the whole folder) |
  | `completion_tokens` | tokens the model REPLIED |
  | `total_tokens` | billed total |

## [pro] Hidden overhead — why "Hi" = 13 prompt tokens
- Your text isn't the only thing sent. The provider wraps messages in a **chat template** with special role-marker tokens (`<|im_start|>user … <|im_end|>`). Those are real billed tokens.
- So every message carries ~10–13 tokens of fixed overhead. Short turns are proportionally expensive.

## [pro] Output is where cost explodes
- Sent 30 tokens, got 607-token answer → billed 637. The REPLY was 95% of cost.
- On real providers, **output tokens cost 2–5× input tokens.** Biggest cost lever = controlling output length (`max_tokens`, "be concise"), not trimming the prompt.

## The full input→output pipeline (what actually happens)
1. messages list → one flat **string** via the chat template (role markers added)
2. string → **token IDs** (integers) via the tokenizer + a fixed vocabulary (~50k–150k)
3. token IDs → **vectors/embeddings** (each ID → a ~thousands-long list of numbers). **Similar meaning = nearby vectors.** ← this IS the basis of RAG
4. vectors transformed through many layers via **attention** (each token "looks at" relevant others)
5. model outputs a **probability over the next token** (across the whole vocab)
6. **sample** one token → append → run the whole thing again → repeat (**autoregressive**, one token per pass)
7. token IDs → text back
- The model receives integers, "thinks" in vectors, speaks in probabilities.
- [pro] One token per forward pass explains: output cost scales with length, streaming works, longer = slower, no native look-ahead (hence chain-of-thought).

## Cost grows across a conversation
- Each turn resends the ENTIRE growing folder → `prompt_tokens` climbs every turn even if your messages stay short. The "memory illusion" shows up as a rising bill.

## The context window = the wall
- Max tokens the model handles in ONE call, counting **input + output together**. Finite (8k / 32k / 128k / 1M).
- [pro] Finite because attention cost grows ~quadratically with length, and the model was trained up to a max length.
- **Hit it:** sent ~450k tokens → `400 invalid_request_error: reduce the length`. Rejected before the model even ran.

### Two problems the wall creates
1. **Conversations can't grow forever** → must trim/summarize old turns (and lose memory — the trade-off).
2. **Can't fit a real knowledge base in the prompt** (millions of tokens). Must select only the relevant passages → **that selection is RAG**. RAG exists *because* the window is finite and your knowledge isn't.
- [pro] "Lost in the middle": even within the window, models attend best to start/end. Retrieving 2k relevant tokens beats dumping 100k — cheaper AND more accurate. Kills the "just use long context" argument.
- [pro] Providers handle overflow differently (reject vs silently truncate) — never rely on them; count tokens and manage the budget yourself.

## Why RAG when the model has web search?
- **Web search IS retrieval** — RAG with the internet as the corpus. Not RAG-vs-search.
- Three knowledge sources: (1) training data — frozen, no sources, hallucinates; (2) web search — public, uncontrolled sources; (3) **RAG over YOUR corpus** — private, curated, authoritative, cited, current.
- Need #3 for: **private data** (web/model can't see it), **control + trust** over the source (regulated work needs the exact right doc + citation), **security/confidentiality**, freshness without retraining.
- Great systems use all three, with an **agent** choosing per question (agentic retrieval — later).

## In my own words
-
-
-