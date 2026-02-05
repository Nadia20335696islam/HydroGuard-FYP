import hashlib
import os


def hash_password(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    """
    Returns (password_hash_hex, salt_hex)
    Uses PBKDF2-HMAC-SHA256 via Python stdlib.
    """
    if salt_hex is None:
        salt = os.urandom(16)
        salt_hex = salt.hex()
    else:
        salt = bytes.fromhex(salt_hex)

    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return dk.hex(), salt_hex
def verify_password(password: str, salt_hex: str, expected_hash_hex: str) -> bool:
    test_hash, _ = hash_password(password, salt_hex=salt_hex)
    return test_hash == expected_hash_hex
