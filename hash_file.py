import hashlib


def hashFile(file_path):
    # Open the file in binary mode and read its contents
    with open(file_path, "rb") as f:
        file_contents = f.read()

    # Compute the hash of the file contents
    hash_value = hashlib.sha256(file_contents).digest()
    # print(hash_value)
    return hash_value
