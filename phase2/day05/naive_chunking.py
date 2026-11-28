def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def naive_chunk(text, size=200):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i : i + size])
    return chunks

text = load_document("phase2/day05/llc_guide.txt")
print(f"Document length: {len(text)} characters\n")

chunks = naive_chunk(text, size=200)
print(f"Split into {len(chunks)} chunks:\n")

for i, chunk in enumerate(chunks, start=1):
    print(f"--- chunk {i} ---")
    print(repr(chunk))      # repr shows the raw text including where it cuts
    print()



