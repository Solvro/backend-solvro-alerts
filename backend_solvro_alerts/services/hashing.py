import hashlib


def hash_string(value: str):
    """
    Default hashing function.\n
    Hashes string value using SHA-256.
    """
    return hashlib.sha256(value.encode()).hexdigest()
