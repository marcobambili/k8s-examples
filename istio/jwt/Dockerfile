FROM python:3.9

WORKDIR /app

# Copia i file necessari
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia i file Python
COPY . .

# Genera la coppia di chiavi prima di generare JWKS
RUN python generate_keys.py && python generate_jwks.py

# Avvia l'app Flask
CMD ["python", "jwt_issuer.py"]
