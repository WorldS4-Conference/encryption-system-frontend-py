# from tkinter import *
# from tkinter import ttk
# from tkinter import filedialog
# from tkinter.filedialog import FileDialog
#
# import requests
# from tkinter import font as tkFont
#
# from decrypt_file import *
# from encrypt_file import *
# from hash_file import *
# from split_file import *
#
# win = Tk()
# win.title("Client")
# win.config(bg="white")
# win.geometry("400x400")
#
#
# def analyse(file_path, block_size):
#     # Splitting the file into blocks and storing the paths to the same
#     block_paths = split_file(file_path, block_size)
#
#     # Hashing the blocks of the file
#     hashes = []
#
#     for block_path in block_paths:
#         hash_value = hashFile(block_path)
#         hashes.append(hash_value)
#
#     # Hashing the blocks of the file
#     hashes = []
#
#     encryption_times = []
#
#     for block_path in block_paths:
#         hash_value = hashFile(block_path)
#         hashes.append(hash_value)
#
#     for block_path, hash in zip(block_paths, hashes):
#         encryption_times.append(encrypt_file(block_path, hash))
#
#     decryption_times = []
#
#     # Decrypting the blocks
#
#     for block_path, hash in zip(block_paths, hashes):
#         decryption_times.append(decrypt_file(block_path, hash))
#
#     # Hashing the blocks of the file
#     # encrypted_hashes = []
#     #
#     # for block_path in block_paths:
#     #     hash_value = hashFile(block_path)
#     #     encrypted_hashes.append(hash_value)
#     #
#     # print("Encrypted Hashes : ")
#     # print(encrypted_hashes)
#     #
#     # # Decrypting the blocks
#     #
#     # for block_path, hash in zip(block_paths, hashes):
#     #     decrypt_file(block_path, hash)
#
#     return encryption_times, decryption_times
#
#
# def fun():
#     # Asking User for file input
#     file_path = filedialog.askopenfile()
#
#     if file_path is None:
#         return
#
#     file_path = file_path.name
#
#     print(file_path)
#
#     mega = 1024 * 1024
#
#     block_sizes = [mega * 10, mega * 20, mega * 30]
#
#     # Encrypting Blocks with Hash
#
#     times = {}
#
#     for block_size in block_sizes:
#         print("BLOCK SIZE = ", block_size, " -------------------")
#         times[block_size] = analyse(file_path, block_size)
#
#     # print(times)
#     for block_size in times:
#         print("--------------------------------------------------------------------")
#
#         print("Block size (in bytes) : ", int(block_size / mega), "MB")
#         # print(times[block_size])
#         decryption_times = times[block_size][1]
#         encryption_times = times[block_size][0]
#
#         for e, d in zip(encryption_times, decryption_times):
#             print(e, d)
#
#         averageE = sum(encryption_times) / len(encryption_times)
#         averageD = sum(decryption_times) / len(decryption_times)
#
#         print("Average times : ")
#         print("Encryption : ", averageE)
#         print("Decryption : ", averageD)
#
#         # for encryption_time, decryption_time in zip(times[block_size[0]], times[block_size[1]]):
#         #     print(encryption_time, " ", decryption_time)
#
#     decryption_times = {}
#
#     pass
#
#
# btn = Button(win, text="Select File", command=fun)
# btn.grid(row=2, column=0)
# btn.place(anchor=CENTER, relx=0.5, rely=0.2)
#
# # sep = ttk.Separator(win, orient=HORIZONTAL)
# # sep.grid(row=1, column=0)
#
# title = Label(win, text='Sash Client', bg="light yellow", fg="blue", borderwidth=0,
#               font=("Helvetica", 18, "italic", "bold"), anchor='e')
# title.grid(row=0, column=0)
# title.place(anchor=CENTER, relx=0.5, rely=0.1)
# win.mainloop()
