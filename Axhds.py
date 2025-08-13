
import hashlib, time, math

rounds = [
    {"id":"7219035", "seed":"wDm4Ck3MEzhzk8D2n8Dlx2Fpwbhk8r", "result":"6.15", "cipher":"ac9a86fe499d8a7c9ce04587b55213b8f8ae8c7471baef2c04fb82b645a7088b"},
    {"id":"7219088", "seed":"2VpAP4A7M28ZFclq4w1nhQDHQSdh5D", "result":"3.71", "cipher":"685c9cfebccdb90ec926967319c2b21f462aa06726e24b3e103c72d572bd3bd3"},
    {"id":"7219112", "seed":"R4NbwovjhRibfFeywIQ3jOEaWT7ddV", "result":"20.37", "cipher":"75098a67648676ef6d0ee07d9044783696e3c17bbd95fb4fd5aed501e3dc248b"},
    {"id":"7219198", "seed":"OrUm9EJxovCTW7L7IpGKK95VJGxbIC", "result":"534.59", "cipher":"add1823d5c30c09110b078d9d0036e55a31bc064d019c680c72a33a6ce5a11b2"}
]

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

results = []
for r in rounds:
    rec = {"id": r["id"]}
    # verify given seed+result -> cipher
    computed = sha256_hex(r["seed"] + r["result"])
    rec["given_match"] = (computed == r["cipher"])
    rec["computed_hash"] = computed
    # brute-force multipliers
    start = time.time()
    found = None
    # range 1.00 .. 2000.00 inclusive step 0.01
    # we'll iterate integers 100..200000 inclusive to represent hundredths
    for i in range(100, 200001):
        m = f"{i/100:.2f}"
        if sha256_hex(r["seed"] + m) == r["cipher"]:
            found = m
            break
    end = time.time()
    rec["bruteforce_found"] = found
    rec["bruteforce_time_s"] = end - start
    results.append(rec)

results
