import tkinter

import requests

from constants import base_url


def checkTags(tags):
    url = base_url + 'api/check_tags/'

    hexed_tags = []

    for tag in tags:
        hexed_tags.append(tag.hex())

    response = requests.post(url, data=[("tags", hexed_tags)])
    print(response.text)
    return response.text
    # print(response)


def uploadFile(block_paths, encrypted_hashes, process_status_listbox):
    # Define the URL endpoint for the file upload
    url = base_url + 'api/upload/'

    # Open the files and upload them
    for block_path, encrypted_hash in zip(block_paths, encrypted_hashes):
        with open(block_path, 'rb') as file:
            # Create a dictionary of any additional form data to be sent
            data = {'tag': encrypted_hash.hex()}

            # Create the HTTP request with the file and form data
            response = requests.post(url, data=data, files={'file': file})
            print(response)

    # Check the response from the server
    if response.status_code == requests.codes.ok:
        process_status_listbox.insert(tkinter.END, 'File uploaded successfully.')
    else:
        process_status_listbox.insert(tkinter.END, 'Error uploading file:', response.text)
    pass
