from datetime import time
# import datetime as dt
import datetime
from constants import *
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


# Padding function
def pad(data):
    length = 16 - (len(data) % 16)
    return data + bytes([length] * length)


def encrypt_file(file_path, key):
    start_time = datetime.datetime.now()

    # Define the AES cipher object
    # Generate a random nonce and counter
    nonce = get_random_bytes(16)

    # Create the AES cipher in EAX mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Read the entire file into memory
    with open(file_path, "rb") as f:
        data = f.read()

    data = pad(data)

    # Encrypt the data
    ciphertext = cipher.encrypt(data)

    # Write the encrypted data and tag to the output file
    with open(file_path, "wb") as f:
        # f.write(nonce)
        f.write(ciphertext)
        # f.write(tag)

    # end_time = datetime.datetime.now()

    # execution_time = end_time - start_time

    # time_diff_sec = round(float(execution_time.total_seconds()) * 1000)

    # return time_diff_sec
