import json
import os
from typing import Optional

VAULT_FILE = os.path.expanduser("~/.password_vault.json")


def vault_exists() -> bool:
    return os.path.exists(VAULT_FILE)


def load_vault() -> dict:
    if not vault_exists():
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_vault(data: dict) -> None:
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    # Restrict file permissions to owner only (Unix)
    os.chmod(VAULT_FILE, 0o600)


def get_entry(site: str) -> Optional[dict]:
    vault = load_vault()
    return vault.get("entries", {}).get(site.lower())


def save_entry(site: str, entry: dict) -> None:
    vault = load_vault()
    vault.setdefault("entries", {})[site.lower()] = entry
    save_vault(vault)


def delete_entry(site: str) -> bool:
    vault = load_vault()
    entries = vault.get("entries", {})
    if site.lower() in entries:
        del entries[site.lower()]
        save_vault(vault)
        return True
    return False


def list_entries() -> list[str]:
    vault = load_vault()
    return list(vault.get("entries", {}).keys())