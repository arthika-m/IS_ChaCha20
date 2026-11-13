
from flask import Flask, request, jsonify, send_from_directory
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Enter a plaintext message."}), 400

        key = get_random_bytes(32)
        nonce = get_random_bytes(12)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        ciphertext = cipher.encrypt(message.encode("utf-8"))

        return jsonify({
            "success": True,
            "original": message,
            "key": key.hex(),
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        data = request.get_json()

        key = bytes.fromhex(data.get("key", "").strip())
        nonce = bytes.fromhex(data.get("nonce", "").strip())
        ciphertext = bytes.fromhex(data.get("ciphertext", "").strip())

        if len(key) != 32:
            return jsonify({
                "error": "Invalid key. Enter exactly 64 hexadecimal characters."
            }), 400

        if len(nonce) != 12:
            return jsonify({
                "error": "Invalid nonce. Enter exactly 24 hexadecimal characters."
            }), 400

        if not ciphertext:
            return jsonify({"error": "Enter encrypted ciphertext."}), 400

        cipher = ChaCha20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)

        return jsonify({
            "success": True,
            "decrypted": plaintext.decode("utf-8")
        })

    except ValueError:
        return jsonify({
            "error": "Invalid hexadecimal input or decrypted data is not valid UTF-8."
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("ChaCha20 Encryption System")
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
