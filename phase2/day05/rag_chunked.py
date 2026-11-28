import os
import time
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

from smart_chunking import load_document, chunk_text

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# load + chunk using the imported functions
document_text = load_document("phase2/day05/llc_guide.txt")
documents = chunk_text(document_text, max_chars=350)
print(f"Indexed {len(documents)} chunks.\n")

# ---------- INDEX: embed the chunks once ----------
doc_embeddings = embed_model.encode(documents)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query, top_k=3):
    q_emb = embed_model.encode(query)
    scored = [(cosine_similarity(q_emb, e), doc) for doc, e in zip(documents, doc_embeddings)]
    scored.sort(reverse=True)
    return scored[:top_k]


def call_llm(messages, retries=3):
    for attempt in range(1, retries + 1):
        try:
            r = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
            return r.choices[0].message.content
        except Exception as e:
            print(f"  [LLM attempt {attempt} failed: {e}]")
            if attempt < retries:
                time.sleep(2)
    raise RuntimeError("LLM call failed after retries")


def answer(query):
    results = retrieve(query)

    context_lines = []
    for i, result in enumerate(results, start=1):
        sim, doc = result
        context_lines.append(f"[{i}] {doc}")
    context = "\n".join(context_lines)

    system_prompt = (
        "You are a compliance assistant. Follow these rules strictly:\n"
        "1. Answer ONLY using the numbered context below. Do not use outside knowledge.\n"
        "2. After each fact, cite its source number in brackets, e.g. [1] or [2].\n"
        "3. If the context does not contain the answer, reply EXACTLY: "
        "\"I don't have that information in my sources.\" Do not guess or invent.\n"
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    reply = call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    return reply, results


while True:
    q = input("\nAsk a question ('quit' to exit): ")
    if q == "quit":
        break
    try:
        reply, used = answer(q)
        print("\n--- ANSWER ---")
        print(reply)
        print("\n--- (retrieved chunks) ---")
        for sim, doc in used:
            print(f"  {sim:.3f}  {doc}\n")
    except Exception as e:
        print(f"Something went wrong: {e}")