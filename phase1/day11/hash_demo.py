import hashlib

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

print("pass123  ->", sha256("pass123"))
print("pass123  ->", sha256("pass123"))     # same input, same hash
print("pass124  ->", sha256("pass124"))     # one char different, totally different hash
print("hello    ->", sha256("hello"))