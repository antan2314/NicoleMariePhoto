from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Shared hasher using argon2-cffi's default parameters (Argon2id, and the
# library's recommended time/memory/parallelism cost settings). Reused across
# calls so every password is hashed and verified with identical parameters.
ph = PasswordHasher()


def hash_password(password: str) -> str:
    # Generates a fresh random salt per call, so hashing the same password
    # twice produces different output. The salt and the cost parameters are
    # encoded inside the returned string, so nothing else needs to be stored.
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        # verify() takes the stored hash first and the plaintext candidate
        # second; it reads the parameters back out of the hash string and
        # raises rather than returning False on a mismatch.
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        # Wrong password: the only failure treated as a normal negative result.
        # Other argon2 errors (e.g. a malformed or corrupted stored hash)
        # deliberately propagate, since those indicate a bug or bad data
        # rather than a failed login attempt.
        return False
