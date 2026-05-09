import getpass
from datetime import datetime
from typing import Optional

import pyperclip

import crypto
import storage


def _prompt_master(prompt="Master password: ") -> str:
    return getpass.getpass(prompt)


def initialise_vault() -> None:
    """Run once on first use to set a master password."""
    if storage.vault_exists():
        print("Vault already exists.")
        return

    print("No vault found. Setting up a new vault.")
    password = _prompt_master("Choose a master password: ")
    confirm = _prompt_master("Confirm master password: ")

    if password != confirm:
        print("Passwords do not match. Aborting.")
        return

    salt = crypto.generate_salt()
    hashed = crypto.hash_master_password(password, salt)

    vault = {
        "salt": salt.hex(),
        "master_hash": hashed,
        "entries": {},
    }
    storage.save_vault(vault)
    print("Vault created successfully.")


def _authenticate() -> Optional[tuple[str, bytes]]:
    """Returns (password, fernet_key) if auth succeeds, else None."""
    vault = storage.load_vault()
    if not vault:
        print("No vault found. Run: python vault.py init")
        return None

    password = _prompt_master()
    salt_hex = vault["salt"]
    stored_hash = vault["master_hash"]

    if not crypto.verify_master_password(password, salt_hex, stored_hash):
        print("Wrong master password.")
        return None

    salt = bytes.fromhex(salt_hex)
    fernet_key = crypto.derive_fernet_key(password, salt)
    return password, fernet_key


def add_password(site: str, username: str) -> None:
    result = _authenticate()
    if not result:
        return
    _, fernet_key = result

    password = _prompt_master(f"Password for {site}: ")
    encrypted = crypto.encrypt(password, fernet_key)

    entry = {
        "username": username,
        "password": encrypted,
        "created_at": datetime.now().isoformat(),
    }
    storage.save_entry(site, entry)
    print(f"Saved password for '{site}'.")


def get_password(site: str, copy: bool = True) -> None:
    result = _authenticate()
    if not result:
        return
    _, fernet_key = result

    entry = storage.get_entry(site)
    if not entry:
        print(f"No entry found for '{site}'.")
        return

    decrypted = crypto.decrypt(entry["password"], fernet_key)

    print(f"Site:     {site}")
    print(f"Username: {entry['username']}")
    if copy:
        pyperclip.copy(decrypted)
        print("Password copied to clipboard.")
    else:
        print(f"Password: {decrypted}")


def delete_password(site: str) -> None:
    result = _authenticate()
    if not result:
        return

    if storage.delete_entry(site):
        print(f"Deleted entry for '{site}'.")
    else:
        print(f"No entry found for '{site}'.")


def list_passwords() -> None:
    result = _authenticate()
    if not result:
        return

    entries = storage.list_entries()
    if not entries:
        print("No saved passwords.")
        return

    print(f"\n{len(entries)} saved site(s):\n")
    for site in sorted(entries):
        entry = storage.get_entry(site)
        print(f"  {site:<25} {entry['username']}")