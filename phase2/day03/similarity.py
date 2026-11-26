import numpy as np 
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "How do I form an LLC?",
    "What's the process to start a limited liability company?",
    "What is the capital of France?",
]

embeddings = model.encode(sentences)
# print(embeddings)
def cosine_similarity(a, b):
    # cosine(a, b) = a*b/|a|*|b| 

    dot = np.dot(a, b)  # A · B
    norm_a = np.linalg.norm(a) # |A|
    norm_b = np.linalg.norm(b) # |B|

    return dot / (norm_a * norm_b)

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        print(f"{sim:.3f}  |  {sentences[i]!r}")
        print(f"         <->  {sentences[j]!r}\n")

    