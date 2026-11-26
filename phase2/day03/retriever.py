import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# --- the knowledge base (our "documents") ---
documents = [
    "An LLC provides limited liability protection, separating personal and business assets.",
    "To form an LLC, file Articles of Organization with the state and pay a filing fee.",
    "LLCs are usually taxed as pass-through entities, so profits are reported on the owners' personal tax returns.",
    "A registered agent is a person or company designated to receive legal documents for an LLC.",
    "Most LLCs must file a Beneficial Ownership Information (BOI) report with FinCEN.",
    "An EIN (Employer Identification Number) is issued by the IRS and identifies a business for tax purposes.",
]

# --- INDEXING: embed the whole knowledge base ONCE ---
doc_embeddings = model.encode(documents)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# --- QUERYING: find the top_k documents closest to the query
def search(query, top_k=3):
    query_embedding = model.encode(query)
    scored = []
    for doc, emb in zip(documents, doc_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        scored.append((sim, doc))

    scored.sort(reverse=True)          # highest similarity first
    return scored[:top_k]

while True:
    q = input("\nAsk something ('quit' to exit): ")
    if q == "quit":
        break
    print(f"\nTop matches for {q!r}:")
    for sim, doc in search(q):
        print(f"  {sim:.3f}  {doc}")