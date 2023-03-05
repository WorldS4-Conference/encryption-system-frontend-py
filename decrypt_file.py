from Crypto.Cipher import AES


def decrypt_file(file_path, key):
    # Read the nonce, ciphertext, and tag from the encrypted file
    with open(file_path, 'rb') as file:
        nonce = file.read(16)
        ciphertext = file.read()
        tag = ciphertext[-16:]
        ciphertext = ciphertext[:-16]

    # Create the AES cipher object with a 256-bit key and GCM mode
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # Decrypt the ciphertext and verify the authentication tag
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    # Write the decrypted data to the output file
    with open(file_path, 'wb') as file:
        file.write(plaintext)
