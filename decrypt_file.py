from Crypto.Cipher import AES
import datetime

from constants import *


# Unpadding function
def unpad(data):
    return data[:-data[-1]]


def decrypt_file(file_path, key):
    print("decrypting")
    # start_time = datetime.datetime.now()
    # Read the nonce, ciphertext, and tag from the encrypted file
    with open(file_path, 'rb') as file:
        # nonce = file.read(16)
        ciphertext = file.read()
        # tag = ciphertext[-16:]
        # ciphertext = ciphertext[:-16]


    # Create the AES cipher object with a 256-bit key and GCM mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext and verify the authentication tag
    # plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext)

    # Write the decrypted data to the output file
    with open(file_path, 'wb') as file:
        file.write(plaintext)


    # end_time = datetime.datetime.now()

    # execution_time = end_time - start_time

    # time_diff_sec = round(float(execution_time.total_seconds()) * 1000)

    # return time_diff_sec
