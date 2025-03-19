import os
import json
import base64
import jwt
import datetime
from flask import Flask, jsonify, request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

app = Flask(__name__)

# Percorsi dei file
PRIVATE_KEY_FILE = "private.key"
PUBLIC_KEY_FILE = "public.key"
JWKS_DIR = ".well-known"
JWKS_FILE = f"{JWKS_DIR}/jwks.json"

# Assicuriamoci che la cartella JWKS esista
if not os.path.exists(JWKS_DIR):
    os.makedirs(JWKS_DIR)

# Funzione per generare una coppia di chiavi RSA se non esistono
def generate_rsa_keys():
    if not os.path.exists(PRIVATE_KEY_FILE) or not os.path.exists(PUBLIC_KEY_FILE):
        print("🔑 Generating new RSA key pair...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Salva la chiave privata
        with open(PRIVATE_KEY_FILE, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Salva la chiave pubblica
        with open(PUBLIC_KEY_FILE, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        print("✅ RSA keys generated successfully!")
    else:
        print("🔑 RSA keys already exist.")

# Converte in base64 url-safe senza padding
def b64_encode(data):
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

# Funzione per generare il file JWKS
def generate_jwks():
    generate_rsa_keys()  # Assicura che le chiavi esistano
    with open(PUBLIC_KEY_FILE, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

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

# Generiamo JWKS all'avvio del server
if not os.path.exists(JWKS_FILE):
    generate_jwks()

# Endpoint per servire JWKS
@app.route('/.well-known/jwks.json')
def get_jwks():
    with open(JWKS_FILE, "r") as f:
        return jsonify(json.load(f))

# Endpoint per generare un token JWT
@app.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.json
    user = data.get("user", "guest")

    # Controlla che la chiave privata esista
    if not os.path.exists(PRIVATE_KEY_FILE):
        return jsonify({"error": "Private key not found"}), 500

    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = f.read()

    payload = {
        "sub": user,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token valido 1 ora
        "iat": datetime.datetime.utcnow(),
        "iss": "jwt-issuer.default.svc.cluster.local"
    }

    token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "my-key-id"})
    return jsonify({"token": token})

# Endpoint per verificare un token JWT
@app.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token missing"}), 400

    # Controlla che la chiave pubblica esista
    if not os.path.exists(PUBLIC_KEY_FILE):
        return jsonify({"error": "Public key not found"}), 500

    with open(PUBLIC_KEY_FILE, "rb") as f:
        public_key = f.read()

    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"], issuer="jwt-issuer.default.svc.cluster.local")
        return jsonify({"message": "Token is valid", "data": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
