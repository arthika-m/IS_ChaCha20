
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

key = get_random_bytes(32)
nonce = get_random_bytes(12)

plaintext = input("Enter the message: ")

cipher = ChaCha20.new(key=key, nonce=nonce)
ciphertext = cipher.encrypt(plaintext.encode())

print("\n--- Encryption ---")
print("Original Message:", plaintext)
print("Key:", key.hex())
print("Nonce:", nonce.hex())
print("Encrypted Message:", ciphertext.hex())

decipher = ChaCha20.new(key=key, nonce=nonce)
decrypted = decipher.decrypt(ciphertext)

print("\n--- Decryption ---")
print("Decrypted Message:", decrypted.decode())

if decrypted.decode() == plaintext:
    print("\nResult: SUCCESS")
else:
    print("\nResult: FAILED")
