from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt_file(file_path, key):
    print(key)
    # Define the AES cipher object
    # Generate a random nonce and counter
    nonce = get_random_bytes(16)

    # Create the AES cipher in EAX mode
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # Read the entire file into memory
    with open(file_path, "rb") as f:
        data = f.read()

    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # Write the encrypted data and tag to the output file
    with open(file_path, "wb") as f:
        f.write(nonce)
        f.write(ciphertext)
        f.write(tag)

