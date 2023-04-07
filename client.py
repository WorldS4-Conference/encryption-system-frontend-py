import base64
import json
import re
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
import datetime

from PIL import Image, ImageTk

from decrypt_file import decrypt_file
from encrypt_file import *
from hash_file import *
from join_file import join_files
from split_file import *
from utils import *


class Client:
    def __init__(self, win, username="Soham Shinde", email="soham2019@iiitkottayam.ac.in"):
        win.title("Client")
        self.email = email
        self.username = username
        win.config(bg="white")
        win.geometry("670x700")
        self.downloaded_file_paths = []

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

        self.policy_entry = Entry(win)

        self.download_label = Label(win, text='Download', bg="white", borderwidth=0,
                                    font=("Helvetica", 12, "bold"), anchor='center')
        self.frame = Frame(win, background="white")

        self.download_path_label = Label(self.frame, state='disabled', anchor='w', background='white',
                                         foreground="blue")
        self.accessId_entry = Entry(self.frame)
        self.attributes_entry = Entry(self.frame)
        self.hash_entry = Text(self.frame, height=5)
        self.hash_entry_scroll = Scrollbar(self.frame, command=self.hash_entry.yview)
        self.hash_entry.configure(yscrollcommand=self.hash_entry_scroll.set)
        self.encrypt_btn = Button(self.frame, text="   Encrypt  ", command=self.encrypt)

        self.download_path_btn = Button(self.frame, text="Select Path", command=self.select_directory)
        self.download_btn = Button(self.frame, text=" Download ", command=self.downloadFile)

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
        self.policy_entry.pack(side=TOP, fill=X)
        self.btn.pack(side=TOP, pady=5)

        ttk.Separator(win, orient=HORIZONTAL).pack(fill=X)
        self.download_label.pack(side=TOP, padx=10, anchor='w')
        self.frame.pack(side=TOP, fill=X)
        # self.input_box1.pack(side=LEFT, fill=X, expand=1)
        # self.download_btn.pack(side=LEFT)
        # self.input_box2.pack(side=LEFT, fill=X, expand=1)
        self.download_path_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.accessId_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.attributes_entry.grid(row=2, column=0, columnspan=1, sticky="ew", padx=5, pady=5)
        self.hash_entry.grid(row=3, sticky=W + E, column=0, padx=5, pady=5)
        self.hash_entry_scroll.grid(row=3, sticky=E + N + S, column=0, padx=5, pady=5)
        self.encrypt_btn.grid(row=3, sticky=N, column=1, padx=0, pady=5)

        self.download_path_btn.grid(row=0, column=1, rowspan=1, sticky="ns", padx=5, pady=5)
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

        self.process_status_listbox.insert(tkinter.END, "***** Block size  = " + str(block_size) + "bytes")

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

        response = checkTags(encrypted_hashes, self.email)
        policy = self.policy_entry.get()
        # return
        print(type(response['exists']))
        if not response['exists']:
            print("hi")
            self.process_status_listbox.insert(tkinter.END, "***** ERROR : File not present in the server")
            self.process_status_listbox.insert(tkinter.END, "***** Uploading File to the server")
            result = uploadFile(block_paths, encrypted_hashes, self.process_status_listbox, response['accessId'],
                                policy)

            if result == 0:
                self.process_status_listbox.insert(tkinter.END, "***** AccessID for the file = " + response['accessId'])
        else:
            self.process_status_listbox.insert(tkinter.END, "File present in the server")

    def downloadFile(self):
        accessId = self.accessId_entry.get()
        print(accessId)
        url = base_url + 'api/download/'
        attributes = self.attributes_entry.get()
        self.process_status_listbox.insert(tkinter.END, "***** Requesting files to the server")

        start_time = datetime.datetime.now()
        response = requests.post(url, data={'accessId': accessId, 'attributes': attributes})
        end_time = datetime.datetime.now()

        if response.status_code == 200:
            # self.process_status_listbox.insert(tkinter.END, "***** SUCCESS : Downloading files successful")
            time_taken = end_time - start_time
            size_in_bytes = float(len(response.content))
            speed_in_bytes_per_sec = size_in_bytes / time_taken.total_seconds()
            speed_in_bytes_per_sec = ((speed_in_bytes_per_sec/1024)/1024)
            speed_in_bytes_per_sec = round(speed_in_bytes_per_sec, 2)
            json_data = response.json()
            json_data = json.loads(json_data)
            # print(json_data)

            # decode base64 string back into bytes
            data = {}
            for key, value in json_data.items():
                data[key] = base64.b64decode(value.encode('utf-8'))

            # Write binary data to files
            for key, value in data.items():
                self.downloaded_file_paths.append("downloaded_chunks/" + key)
                with open("downloaded_chunks/" + key, 'wb') as file:
                    file.write(value)

            self.process_status_listbox.insert(tkinter.END, "***** SUCCESS : Downloaded files successfully at " + str(speed_in_bytes_per_sec) + " MB/S")
            self.process_status_listbox.insert(tkinter.END, "***** Enter the hashes to decrypt the file : ")

        else:
            json_data = response.json()
            # json_data = json.loads(json_data)
            print(json_data)
            self.process_status_listbox.insert(tkinter.END, "***** Message from server : " + json_data['error'])

        # print(data)

        # for file_name, file_content in data:
        #     print(file_name)
        #     print(file_content)

        # file_name = response.headers.get('Content-Disposition').split('filename=')[1]
        # block_path = 'chunks/' + file_name.strip('"')
        # with open(block_path, 'wb') as f:
        #     f.write(response.content)

        # Convert a hexadecimal string to its corresponding hash value
        # accessId = self.attributes_entry.get()  # "793ba7ea3565921d5550ee5a9c16fe4ed71564635361b610ad64234c08365c45"
        # accessId = bytes.fromhex(accessId)
        #
        # decrypt_file(block_path, accessId)

    def encrypt(self):
        if str(self.hash_entry.get(1.0, END)).isspace():
            self.process_status_listbox.insert(tkinter.END, "***** ERROR : Enter the hashes")
        elif self.download_path_label.cget('text') == '':
            self.process_status_listbox.insert(tkinter.END, "***** ERROR : Select the destination path")
        else:
            self.process_status_listbox.insert(tkinter.END, "***** Decrypting the chunks")
            try:
                hash_content = self.hash_entry.get('1.0', END)
                print(hash_content)
                destination_path = self.download_path_label.cget('text')
                print(destination_path)
                hash_list = hash_content.split('\n')

                for hash in hash_list:
                    hash = hash.strip()

                for hash, file_path in zip(hash_list, self.downloaded_file_paths):
                    key = bytes.fromhex(hash)
                    decrypt_file(file_path, key)
                self.process_status_listbox.insert(tkinter.END, "***** SUCCESS: " + "Decryption Successful")
                print(self.downloaded_file_paths)

                self.process_status_listbox.insert(tkinter.END, "***** Joining the chunks")
                file_name = re.sub('_part_\d+', '', self.downloaded_file_paths[0])
                file_name = os.path.basename(file_name)

                join_files(self.downloaded_file_paths, destination_path + "/" + file_name)
                self.process_status_listbox.insert(tkinter.END, "***** SUCCESS: " + "Joining Successful")

            except Exception as e:
                self.process_status_listbox.insert(tkinter.END, "***** ERROR: " + str(e.args[0]))


if __name__ == '__main__':
    root = Tk()
    app = Client(root)
    root.mainloop()
