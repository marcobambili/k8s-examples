from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Access Denied"}), 401

    # Istio si occupa della validazione del JWT, quindi qui basta controllare che il token sia presente
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
