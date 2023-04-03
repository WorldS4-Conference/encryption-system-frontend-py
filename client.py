import binascii
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

from decrypt_file import *
from encrypt_file import *
from hash_file import *
from split_file import *
from utils import *


class Client:
    def __init__(self, win, username="Soham Shinde", email="soham2019@iiitkottayam.ac.in"):
        win.title("Client")
        win.config(bg="white")
        win.geometry("670x700")

        # Load and resize the avatar image
        avatar_image = Image.open("assets/icons/avatar.png").resize((50, 50), Image.LANCZOS)
        self.avatar = ImageTk.PhotoImage(avatar_image)

        # self.avatar_label = Label(win, image=avatar_image)

        self.user_info_name = Label(win, text=f'User: {username}', bg="white", fg="black", borderwidth=0,
                                    font=("Helvetica", 12), anchor='w')
        self.user_info_email = Label(win, text=f'Email: {email}', bg="white", fg="black",
                                     borderwidth=0,
                                     font=("Helvetica", 12), anchor='w')

        self.title = Label(win, text='CipherHorizon', bg="light yellow", fg="blue", borderwidth=0,
                           font=("Helvetica", 18, "italic", "bold"), anchor='center')

        self.upload_label = Label(win, text='Upload', bg="white", borderwidth=0,
                                  font=("Helvetica", 12, "bold"), anchor='center')

        self.download_label = Label(win, text='Download', bg="white", borderwidth=0,
                                    font=("Helvetica", 12, "bold"), anchor='center')
        self.frame = Frame(win, background="white")

        self.download_path_label = Label(self.frame, state='disabled', anchor='w', background='white',
                                         foreground="blue")
        self.input_box2 = Entry(self.frame)
        self.input_box3 = Entry(self.frame)


        self.download_path_btn = Button(self.frame, text="Select Path", command=self.select_directory)
        self.download_btn = Button(self.frame, text="Download", command=self.downloadFile)

        self.btn = Button(win, text="Select File", command=self.uploadFile)

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
        # self.avatar_label.pack(side=LEFT, padx=10, pady=10)
        self.user_info_name.pack(side=TOP, padx=10, anchor='w')
        self.user_info_email.pack(side=TOP, padx=10, anchor='w')
        ttk.Separator(win, orient=HORIZONTAL).pack(fill=X)

        self.upload_label.pack(side=TOP, padx=10, anchor='w')
        self.btn.pack(side=TOP, pady=5)

        ttk.Separator(win, orient=HORIZONTAL).pack(fill=X)
        self.download_label.pack(side=TOP, padx=10, anchor='w')
        self.frame.pack(side=TOP, fill=X)
        # self.input_box1.pack(side=LEFT, fill=X, expand=1)
        # self.download_btn.pack(side=LEFT)
        # self.input_box2.pack(side=LEFT, fill=X, expand=1)
        self.download_path_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.input_box2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.input_box3.grid(row=2, column=0, columnspan=1, sticky="ew", padx=5, pady=5)

        self.download_path_btn.grid(row=0, column=1, rowspan=1, sticky="ns", padx=0, pady=5)
        self.download_btn.grid(row=1, column=1, rowspan=1, sticky="ns", padx=0, pady=5)

        # Configure the columns and rows to resize properly
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.frame.pack(side=TOP, fill=X)

        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        self.process_status_listbox.pack(side=TOP, fill=BOTH, expand=1)

        win.mainloop()

    def select_directory(self):
        # Show the file dialog and get the selected directory
        directory = filedialog.askdirectory()

        # Set the text of the label to the selected directory
        self.download_path_label.config(text=directory)

    def uploadFile(self):

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

        # for block_path, hash in zip(block_paths, hashes):
        #     decrypt_file(block_path, hash)

        # return

        if checkTags(encrypted_hashes) == 'False':
            self.process_status_listbox.insert(tkinter.END, "File not present in the server")
            uploadFile(block_paths, encrypted_hashes, self.process_status_listbox)
        else:
            self.process_status_listbox.insert(tkinter.END, "File present in the server")

    def downloadFile(self):
        hash_value = self.input_box2.get()

        print(hash_value)
        url = base_url + 'api/download/'
        response = requests.post(url, data={'tag': hash_value})
        file_name = response.headers.get('Content-Disposition').split('filename=')[1]
        block_path = 'chunks/' + file_name.strip('"')
        with open(block_path, 'wb') as f:
            f.write(response.content)

        # Convert a hexadecimal string to its corresponding hash value
        hash_value = self.input_box3.get() # "793ba7ea3565921d5550ee5a9c16fe4ed71564635361b610ad64234c08365c45"
        hash_value = bytes.fromhex(hash_value)

        decrypt_file(block_path, hash_value)


if __name__ == '__main__':
    root = Tk()
    app = Client(root)
    root.mainloop()
