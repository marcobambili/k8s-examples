


curl -X POST http://localhost:5000/generate-token -H "Content-Type: application/json" -d '{"user": "alice"}'


curl -X POST http://localhost:5000/verify-token -H "Content-Type: application/json" -d '{"token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Im15LWtleS1pZC..."}'


curl -X GET http://<ISTIO_INGRESS>/hello



curl -X GET http://<ISTIO_INGRESS>/hello -H "Authorization: Bearer <your-valid-jwt>"

podman login docker.io
podman build -t jwt-issuer:v6 .
podman tag jwt-issuer:v6 01bit/jwt-issuer:v6
podman push 01bit/jwt-issuer:v6


podman build -t jwt-service:v2 .
podman tag jwt-service:v2 01bit/jwt-service:v2
podman push 01bit/jwt-service:v2


curl -X GET http://jwt-issuer.default.svc.cluster.local/.well-known/jwks.json

http://jwt-issuer.default.svc.cluster.local/.well-known/jwks.json


//verificare issuer

curl -X POST http://jwt-issuer.default.svc.cluster.local/generate-token -H "Content-Type: application/json" -d '{"user": "alice"}'



restitisce token

curl -X POST http://jwt-issuer.default.svc.cluster.local/verify-token -H "Content-Type: application/json" -d '{"token": "<IL_TUO_TOKEN>"}'

curl -X POST http://jwt-issuer.default.svc.cluster.local/verify-token -H "Content-Type: application/json" -d '{"token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Im15LWtleS1pZCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsImV4cCI6MTczODIzODIwOSwiaWF0IjoxNzM4MjM0NjA5LCJpc3MiOiJqd3QtaXNzdWVyLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwifQ.yJIYRGx7aXBnoPiaqdD6ZQOJbQFjJZfZwTHxtbvkGfnpDYYogE_imfYrrVss-_NVtkP8UgQW6pm2h2dTZPulEvwTa-GYBEEOnp3tkfq2TCHaZLEIBtVkesl3VU6Y4HlA6zgBDX3Y4XwTrUAMl0GHujPRaUNJ18nBo6WjzJpGmOSlRs8ftFhldabWoYxykrHtD1uOBBl9Fpm3WFnzwZ63sbP7mIa89tslvTg__JDbg9DLZXWIZlRo7EO43M3WEcnkQii44d2itz8HTijR7IEVBOBwtI-ya021KIoiHfzLotR6l2B5b3nhhQdBouXeIJTMxhuWk9Hi0sfCngNMwMc1rg"}'

restituisce risp se valido



curl -X GET http://localhost:8080/hello 

curl -X GET http://localhost:8080/hello -H "Content-Type: application/json" -d '{"token": "<IL_TUO_TOKEN>"}'


curl -X GET http://<ISTIO_INGRESS>/hello -H "Authorization: Bearer <your-valid-jwt>"

curl -X GET http://localhost:8080/hello -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Im15LWtleS1pZCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsImV4cCI6MTczODI1NDI4OSwiaWF0IjoxNzM4MjUwNjg5LCJpc3MiOiJqd3QtaXNzdWVyLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwifQ.lgS21lTHcEORaJYPD0W_RwHwuNchNhMe5-Ld6S80rThf4zyy5RrMNV-Q7M5fW2M-XuconPXEXeQUOsGfaULO53SgCA48CJPzhoMfyl5wVzZHGgTp7nB98SFixuxW6U_fmHZveD_vTBpTLzerDAxW6N0BVw3CEdJ5QToIU6h3yghxYNg5LrJw4WJaAOSFbsziAEQrWt9tF-rpFWq9JoDVziz6cAitGgiGY2cb1Ti2kOLR9PQwR5893IJpTJM4L-ybw6LXK2suz489lpFDioqk9PiEALUN8UxEyHnHZ2hyI-gsqlU-irWoQ8h_VaQzr0F84n7x7YSgRpzVJTskZOkqLQ"



// in jws issuer
# Genera la chiave privata
openssl genpkey -algorithm RSA -out private.key -pkeyopt rsa_keygen_bits:2048

# Genera la chiave pubblica dalla chiave privata
openssl rsa -pubout -in private.key -out public.key

A questo punto, il contenuto della chiave pubblica (public.key) andrà nel file .well-known/jwks.json. Un esempio di file JWKS potrebbe essere:
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "my-key-id",
      "use": "sig",
      "n": "<modulus>",
      "e": "AQAB"
    }
  ]
}
