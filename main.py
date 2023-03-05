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
    # key = key.encode('utf-8')
    print(key)
    # Define the AES cipher object
    cipher = AES.new(key, AES.MODE_EAX)

    # Read the entire file into memory
    with open(file_path, "rb") as f:
        file_contents = f.read()

    # Encrypt the file contents
    encrypted_data, tag = cipher.encrypt_and_digest(file_contents)

    # Write the encrypted data and tag to the output file
    with open(file_path, "wb") as f:
        f.write(encrypted_data)
        # [f.write(x) for x in (cipher.nonce, tag, encrypted_data)]

    return cipher.nonce, tag
    # [f.write(x) for x in (cipher.nonce, tag, encrypted_data)]


def decrypt_file(file_path, key, nonce, tag):
    # Encode the key as bytes
    # key = key.encode('utf-8')
    # nonce = get_random_bytes(16)  # Generate a new nonce
    print("decrypting file ")

    # Read the nonce, ciphertext, and tag from the encrypted file
    with open(file_path, 'rb') as file:
        ciphertext = file.read()
        # nonce, ciphertext, tag = [file.read(x) for x in (12, -1, 28)]

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
    # print(file_path)

    # Splitting the file into blocks and storing the paths to the same
    block_paths = split_file(file_path, 1048576)
    # print(block_paths)
    # print(open(block_paths[0], 'r').read())

    # Hashing the blocks of the file
    hashes = []

    for block_path in block_paths:
        hash_value = hashFile(block_path)
        hashes.append(hash_value)

    # print(hashes)

    nouce_list = []
    tags_list = []

    for block_path, hash in zip(block_paths, hashes):
        nouce, tag = encrypt_file(block_path, hash)
        nouce_list.append(nouce);
        tags_list.append(tag)

    print(nouce_list)
    print(tags_list)

    for block_path, hash, nonce, tag in zip(block_paths, hashes, nouce_list, tags_list):
        decrypt_file(block_path, hash, nonce, tag)

    pass


btn = Button(win, text="Select File", command=fun)
btn.grid(row=0, column=0)

win.mainloop()
