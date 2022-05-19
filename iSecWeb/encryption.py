import hashlib
import random
def encrypt(password, key):
    if key == '':
        key = random.randint(100000, 999999)
        hash = password + str(key)
        hash = hashlib.sha3_224(hash.encode())
        hash = hash.hexdigest()
    else:
        hash = password + str(key)
        hash = hashlib.sha3_224(hash.encode())
        hash = hash.hexdigest()
    return hash


