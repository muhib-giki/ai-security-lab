import time
import os
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- knowledge base ---
documents = [
    "An LLC provides limited liability protection, separating personal and business assets.",
    "To form an LLC, file Articles of Organization with the state and pay a filing fee.",
    "LLCs are usually taxed as pass-through entities, so profits are reported on the owners' personal tax returns.",
    "A registered agent is a person or company designated to receive legal documents for an LLC.",
    "Most LLCs must file a Beneficial Ownership Information (BOI) report with FinCEN.",
    "An EIN (Employer Identification Number) is issued by the IRS and identifies a business for tax purposes.",
]

doc_embeddings = embed_model.encode(documents)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=3):
    query_embedding = embed_model.encode(query)
    scored = []
    for doc, emb in zip(documents, doc_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        scored.append((sim, doc))
    
    scored.sort(reverse=True) # highest similarity first
    return scored[:top_k]

def call_llm(messages, retries=3):
    for attempt in range(1, retries + 1):
        try: 
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"  [LLM call attempt {attempt} failed: {e}]")
            if attempt < retries:
                time.sleep(2)   # wait 2 seconds before retrying
    raise RuntimeError("LLM call failed after all retries")

def answer(query):
    # 1. RETRIEVE
    results = retrieve(query)

    # 2. AUGMENT — build a context block from the retrieved docs
    lines = []
    for sim, doc in results:        # each result is a (score, doc) pair — unpack it
        lines.append(f"- {doc}")    # make a bullet line, ignore the score here
    context = "\n".join(lines)      # glue the lines together with newlines between

    system_prompt = (
        "You are a helpful assistant for business formation questions. "
        "Answer the user's question using ONLY the context provided. "
        "If the answer is not in the context, say you don't have that information."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    # 3. GENERATE
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
        print("\n--- (retrieved context) ---")
        for sim, doc in used:
            print(f"  {sim:.3f}  {doc}")
    except Exception as e:
        print(f"Something went wrong: {e}")