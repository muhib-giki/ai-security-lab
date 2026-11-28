import re


def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_sentences(text):
    # flatten all whitespace/newlines into single spaces first
    text = " ".join(text.split())
    # split at whitespace that follows a . ! or ?  (i.e. sentence ends)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return sentences


def chunk_text(text, max_chars=350):
    sentences = split_sentences(text)
    chunks = []
    current = []            # sentences in the chunk being built
    current_len = 0

    for sentence in sentences:
        # if adding this sentence would overflow, close the current chunk
        if current_len + len(sentence) > max_chars and current:
            chunks.append(" ".join(current))
            # OVERLAP: start the next chunk with the last sentence of this one
            current = [current[-1]]
            current_len = len(current[-1])
        current.append(sentence)
        current_len += len(sentence)

    if current:                         # don't forget the final chunk
        chunks.append(" ".join(current))

    return chunks

if __name__ == "__main__":
    text = load_document("phase2/day05/llc_guide.txt")
    chunks = chunk_text(text, max_chars=350)
    print(f"Split into {len(chunks)} chunks:\n")
    for i, chunk in enumerate(chunks, start=1):
        print(f"--- chunk {i} ({len(chunk)} chars) ---")
        print(chunk)
        print()