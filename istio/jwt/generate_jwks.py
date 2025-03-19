import os
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PUBLIC_KEY_FILE = "public.key"
JWKS_DIR = ".well-known"
JWKS_FILE = f"{JWKS_DIR}/jwks.json"

# Assicuriamoci che la cartella JWKS esista
if not os.path.exists(JWKS_DIR):
    os.makedirs(JWKS_DIR)

# Funzione per caricare la chiave pubblica
def load_public_key():
    if not os.path.exists(PUBLIC_KEY_FILE):
        print("❌ Public key not found! Make sure to run generate_keys.py first.")
        exit(1)

    with open(PUBLIC_KEY_FILE, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

# Converte in base64 url-safe senza padding
def b64_encode(data):
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

# Funzione per generare il JWKS
def generate_jwks():
    public_key = load_public_key()
    numbers = public_key.public_numbers()
    
    jwk = {
        "kty": "RSA",
        "kid": "my-key-id",
        "use": "sig",
        "alg": "RS256",
        "n": b64_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, byteorder="big")),
        "e": b64_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, byteorder="big")),
    }

    jwks = {"keys": [jwk]}

    with open(JWKS_FILE, "w") as f:
        json.dump(jwks, f, indent=4)

    print(f"✅ JWKS file generated at {JWKS_FILE}")

if __name__ == "__main__":
    generate_jwks()
