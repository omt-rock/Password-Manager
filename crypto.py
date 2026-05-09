import os
import hashlib
import base64
from cryptography.fernet import Fernet


def generate_salt() -> bytes:
    return os.urandom(16)


def hash_master_password(password: str, salt: bytes) -> str:
    """Hash master password using PBKDF2. Only used for verification."""
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(),
        salt=salt,
        iterations=390_000,   # NIST recommended minimum (2023)
    )
    return key.hex()


def verify_master_password(password: str, salt_hex: str, stored_hash: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    return hash_master_password(password, salt) == stored_hash


def derive_fernet_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key from the master password for Fernet encryption."""
    raw = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(),
        salt=salt,
        iterations=390_000,
    )
    return base64.urlsafe_b64encode(raw)


def encrypt(plaintext: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()