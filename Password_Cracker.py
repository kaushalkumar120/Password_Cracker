import hashlib
import itertools
import string
import time

# -------- Strength Check --------
def check_strength(password):
    score = sum([
        len(password) >= 8,
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])
    return ["Very Weak", "Weak", "Moderate", "Strong"][score]

# -------- Hash Check --------
def match(pw, target_hash):
    return hashlib.sha256(pw.encode()).hexdigest() == target_hash

# -------- Dictionary Attack --------
def dictionary_attack(target_hash):
    words = ["password", "123456", "admin", "hello", "qwerty"]
    start = time.time()
    
    for w in words:
        if match(w, target_hash):
            return True, w, time.time() - start
    return False, None, time.time() - start

# -------- Brute Force --------
def brute_force(target_hash, max_len=3):
    chars = string.ascii_lowercase + string.digits
    start = time.time()
    
    for l in range(1, max_len+1):
        for guess in itertools.product(chars, repeat=l):
            pw = "".join(guess)
            if match(pw, target_hash):
                return True, pw, time.time() - start
    return False, None, time.time() - start

# -------- Main --------
password = input("Enter password: ")
target_hash = hashlib.sha256(password.encode()).hexdigest()

print("Strength:", check_strength(password))

# Dictionary
ok, pw, t = dictionary_attack(target_hash)
if ok:
    print(f"[✔] Dictionary cracked: {pw} in {t:.3f}s")
else:
    print("[✘] Dictionary failed")

    # Brute force
    ok, pw, t = brute_force(target_hash)
    if ok:
        print(f"[✔] Brute force cracked: {pw} in {t:.3f}s")
    else:
        print("[✘] Brute force failed")

print("⚠ Use strong passwords!")