from sentence_transformers import SentenceTransformer

# load the embedding model (downloads once on first run, then cached)
model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "How do I form an LLC?",
    "What's the process to start a limited liability company?",
    "What is the capital of France?",
]

# turn each sentence into a vector
embeddings = model.encode(sentences)

print("Embeddings array shape:", embeddings.shape)   # (3 sentences, 384 numbers each)

for sentence, vector in zip(sentences, embeddings):
    print(f"\n{sentence!r}")
    print(f"  vector length: {len(vector)}")
    print(f"  first 8 numbers: {vector[:8]}")