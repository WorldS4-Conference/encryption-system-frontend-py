import os
import tkinter

import requests

from constants import base_url


def checkTags(tags, email, block_paths):
    url = base_url + 'api/check_tags/'

    hexed_tags = []

    for tag in tags:
        hexed_tags.append(tag.hex())

    filenames = [os.path.basename(path) for path in block_paths]

    response = requests.post(url, data=[("tags", hexed_tags), ('email', email), ('filenames', filenames)])
    print(response.json())
    return response.json()
    # print(response)


def uploadFile(block_paths, encrypted_hashes, process_status_listbox, accessId, policy='(((FINANCE and (SENIOR or MANAGER)) or (HR and MANAGER)))'):
    # Define the URL endpoint for the file upload
    url = base_url + 'api/upload/'

    # Open the files and upload them
    for block_path, encrypted_hash in zip(block_paths, encrypted_hashes):
        with open(block_path, 'rb') as file:
            # Create a dictionary of any additional form data to be sent
            data = {'tag': encrypted_hash.hex(), 'accessId': accessId,
                    'policy': policy}

            # Create the HTTP request with the file and form data
            response = requests.post(url, data=data, files={'file': file})
            print(response)

    # Check the response from the server
    if response.status_code == requests.codes.ok:
        process_status_listbox.insert(tkinter.END, '***** File uploaded successfully.')
        return 0
    else:
        process_status_listbox.insert(tkinter.END, '***** Error uploading file:', response.text)
        return 1
    pass
