import hashlib


def digest(to_digest: bytes) -> bytes:
    """Creates a sha256 hash."""
    return hashlib.sha256(to_digest).digest()
