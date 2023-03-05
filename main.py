from tkinter import *
from tkinter import filedialog

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from hash_file import *
from split_file import *

win = Tk()
win.title("Client")
win.config(bg="white")
win.geometry("400x400")


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


def fun():
    # Asking User for file input
    file_path = filedialog.askopenfile().name

    block_size = 1024 * 1024

    # Splitting the file into blocks and storing the paths to the same
    block_paths = split_file(file_path, block_size)

    # Hashing the blocks of the file
    hashes = []

    for block_path in block_paths:
        hash_value = hashFile(block_path)
        hashes.append(hash_value)

    # Encrypting Blocks with Hash

    for block_path, hash in zip(block_paths, hashes):
        encrypt_file(block_path, hash)

    # Decrypting the blocks

    for block_path, hash in zip(block_paths, hashes):
        decrypt_file(block_path, hash)

    pass


btn = Button(win, text="Select File", command=fun)
btn.grid(row=0, column=0)

win.mainloop()
