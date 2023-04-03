from tkinter import *
from constants import base_url
from tkinter import ttk
from tkinter import filedialog
from utils import *

import requests

from decrypt_file import *
from encrypt_file import *
from hash_file import *
from split_file import *

win = Tk()
win.title("Client")
win.config(bg="white")
win.geometry("670x400")


# hash_label_text = StringVar()
# hash_label_text = ""


def fun():
    global hash_label_text

    # Asking User for file input
    file_path = filedialog.askopenfile()

    if file_path is None:
        return

    file_path = file_path.name

    print(file_path)

    block_size = 1024 * 1024 * 20
    process_status_listbox.insert(tkinter.END, "***** Block size  = " + str(block_size) + "bytes");

    # Splitting the file into blocks and storing the paths to the same
    process_status_listbox.insert(tkinter.END, "***** Splitting the file")
    block_paths = split_file(file_path, block_size, process_status_listbox)

    # Hashing the blocks of the file
    process_status_listbox.insert(tkinter.END, "***** Hashing the chunks")

    hashes = []

    for block_path in block_paths:
        hash_value = hashFile(block_path)
        process_status_listbox.insert(tkinter.END, hash_value.hex())

        hashes.append(hash_value)

    # print("Hashes : ")
    # print(hashes)

    # Encrypting Blocks with Hash
    process_status_listbox.insert(tkinter.END, "***** Encrypting the blocks with their respective hash")

    for block_path, hash in zip(block_paths, hashes):
        encrypt_file(block_path, hash)

    # Hashing the blocks of the file

    process_status_listbox.insert(tkinter.END, "***** Hashing the Encrypted chunks")

    encrypted_hashes = []

    for block_path in block_paths:
        hash_value = hashFile(block_path)
        encrypted_hashes.append(hash_value)

    # print("Encrypted Hashes : ")
    # print(encrypted_hashes)

    hash_label_text = ""
    for i in range(len(encrypted_hashes)):
        process_status_listbox.insert(tkinter.END, str(i) + encrypted_hashes[i].hex())


    # hash_file_path = filedialog.askopenfile()

    # if hash_file_path is None:
    #     return

    # hash_file_path = hash_file_path.name

    # f = FileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    # if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
    #     return

    # for hash in encrypted_hashes:
    #     f.write(hash)

    # f.close()  # `()` was missing.

    # Decrypting the blocks

    for block_path, hash in zip(block_paths, hashes):
        decrypt_file(block_path, hash)

    return


    if checkTags(encrypted_hashes) == 'False':
        uploadFile(block_paths, encrypted_hashes, process_status_listbox)


title = Label(win, text='Sash Client', bg="light yellow", fg="blue", borderwidth=0,
              font=("Helvetica", 18, "italic", "bold"), anchor='center')

btn = Button(win, text="Select File", command=fun)

# 15b1809952ed7518c12b919076ceadc6e763b757d217d0d0a66a85939b9c381e
process_status_listbox = Listbox(win, bg="white", fg="black", font=("Helvetica", 13), width=65, selectmode="multiple")

# Vertical scrollbar for the listbox
yscrollbar = ttk.Scrollbar(win, orient="vertical", command=process_status_listbox.yview)
process_status_listbox.configure(yscrollcommand=yscrollbar.set)

# Horizontal scrollbar for the listbox
xscrollbar = ttk.Scrollbar(win, orient="horizontal", command=process_status_listbox.xview)
process_status_listbox.configure(xscrollcommand=xscrollbar.set)

# Pack the widgets
title.pack(side=TOP, fill=X, pady=10)
btn.pack(side=TOP, pady=5)
yscrollbar.pack(side=RIGHT, fill=Y)
xscrollbar.pack(side=BOTTOM, fill=X)
process_status_listbox.pack(side=TOP, fill=BOTH, expand=1)

win.mainloop()
