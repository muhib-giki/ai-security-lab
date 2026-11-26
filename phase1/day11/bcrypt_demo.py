import bcrypt

h1 = bcrypt.hashpw(b"pass123", bcrypt.gensalt())
h2 = bcrypt.hashpw(b"pass123", bcrypt.gensalt())

print("hash 1:", h1)
print("hash 2:", h2)
print("same password, same hash?", h1 == h2)

print("correct password check:", bcrypt.checkpw(b"pass123", h1))
print("wrong password check:  ", bcrypt.checkpw(b"wrongpw", h1))