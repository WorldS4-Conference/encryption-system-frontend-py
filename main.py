from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from decrypt_file import *
from encrypt_file import *
from hash_file import *
from split_file import *
from utils import *


class Client:
    def __init__(self, win):
        win.title("Client")
        win.config(bg="white")
        win.geometry("670x400")

        self.title = Label(win, text='Sash Client', bg="light yellow", fg="blue", borderwidth=0,
                           font=("Helvetica", 18, "italic", "bold"), anchor='center')

        self.btn = Button(win, text="Select File", command=self.fun)

        self.process_status_listbox = Listbox(win, bg="white", fg="black", font=("Helvetica", 13), width=65,
                                              selectmode="multiple")

        # Vertical scrollbar for the listbox
        self.yscrollbar = ttk.Scrollbar(win, orient="vertical", command=self.process_status_listbox.yview)
        self.process_status_listbox.configure(yscrollcommand=self.yscrollbar.set)

        # Horizontal scrollbar for the listbox
        self.xscrollbar = ttk.Scrollbar(win, orient="horizontal", command=self.process_status_listbox.xview)
        self.process_status_listbox.configure(xscrollcommand=self.xscrollbar.set)

        # Pack the widgets
        self.title.pack(side=TOP, fill=X, pady=10)
        self.btn.pack(side=TOP, pady=5)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        self.process_status_listbox.pack(side=TOP, fill=BOTH, expand=1)

        win.mainloop()

    def fun(self):

        # Asking User for file input
        file_path = filedialog.askopenfile()

        if file_path is None:
            return

        file_path = file_path.name

        print(file_path)

        self.process_status_listbox.insert(tkinter.END, "***** Block size  = " + str(block_size) + "bytes");

        # Splitting the file into blocks and storing the paths to the same
        self.process_status_listbox.insert(tkinter.END, "***** Splitting the file")
        block_paths = split_file(file_path, block_size, self.process_status_listbox)

        # Hashing the blocks of the file
        self.process_status_listbox.insert(tkinter.END, "***** Hashing the chunks")

        hashes = []

        for block_path in block_paths:
            hash_value = hashFile(block_path)
            self.process_status_listbox.insert(tkinter.END, hash_value.hex())

            hashes.append(hash_value)

        # print("Hashes : ")
        # print(hashes)

        # Encrypting Blocks with Hash
        self.process_status_listbox.insert(tkinter.END, "***** Encrypting the blocks with their respective hash")

        for block_path, hash_value in zip(block_paths, hashes):
            encrypt_file(block_path, hash_value)

        # Hashing the blocks of the file

        self.process_status_listbox.insert(tkinter.END, "***** Hashing the Encrypted chunks")

        encrypted_hashes = []

        for block_path in block_paths:
            hash_value = hashFile(block_path)
            encrypted_hashes.append(hash_value)

        # print("Encrypted Hashes : ")
        # print(encrypted_hashes)

        hash_label_text = ""
        for i in range(len(encrypted_hashes)):
            self.process_status_listbox.insert(tkinter.END, str(i) + encrypted_hashes[i].hex())

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


if __name__ == '__main__':
    root = Tk()
    app = Client(root)
    root.mainloop()
