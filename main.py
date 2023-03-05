from tkinter import *
from tkinter import filedialog

from decrypt_file import *
from encrypt_file import *
from hash_file import *
from split_file import *

win = Tk()
win.title("Client")
win.config(bg="white")
win.geometry("400x400")


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
