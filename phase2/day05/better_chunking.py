def load_document(path):
    with open(path,"r", encoding="utf-8") as f:
        return f.read()

def chunk_by_paragraph(text):
    # split on blank lines, drop empties, trim whitespace
    raw_paragraphs = text.split("\n\n")
    chunks = []
    for p in raw_paragraphs:
        p = p.strip()
        if p:                   # skip empty pieces
            chunks.append(p)
    return chunks

text = load_document("phase2/day05/llc_guide.txt")
chunks = chunk_by_paragraph(text)
                            
print(f"Split into {len(chunks)} paragraph chunks:\n")
for i, chunk in enumerate(chunks, start=1):
    print(f"--- chunk {i} ({len(chunk)} chars) ---")
    print(chunk)
    print()