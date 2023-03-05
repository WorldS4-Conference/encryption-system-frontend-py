import os


def split_file(file_path, block_size):
    # List of the blocks
    block_paths = []

    # Get the size of the file
    file_size = os.path.getsize(file_path)

    # Calculate the number of chunks
    num_chunks = file_size // block_size
    if file_size % block_size != 0:
        num_chunks += 1

    # Open the input file
    with open(file_path, 'rb') as f:

        # Get file name and extension
        filename, extension = os.path.splitext(file_path)
        filename = filename.split('/')[-1]
        directory_path = os.path.split(file_path)[0]
        print(directory_path)

        for i in range(num_chunks + 1):

            # Create the chunk file name
            block_file_name = directory_path + "/" + filename + f"_part_{i + 1}" + extension
            block_paths.append(block_file_name)

            # Open the output chunk file
            with open(block_file_name, 'wb') as chunk_file:
                # Read and write the chunk data
                chunk_data = f.read(block_size)
                chunk_file.write(chunk_data)

                # Stop reading if we've reached the end of the file
                if not chunk_data:
                    break

                # Move the file pointer to the next chunk
                f.seek(block_size * (i + 1))

            print(f"Wrote chunk file {block_file_name} ({len(chunk_data)} bytes)")

    print("Finished splitting file into chunks")

    return block_paths
