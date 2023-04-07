import os


def join_files(file_paths, output_file_path):
    # Open the output file for writing
    with open(output_file_path, 'wb') as output_file:
        # Iterate over the input files
        for file_path in file_paths:
            # Open the input file
            with open(file_path, 'rb') as input_file:
                # Read the file contents and write them to the output file
                file_contents = input_file.read()
                output_file.write(file_contents)

            # Delete the input file
            # os.remove(file_path)

            print(f"Deleted file {file_path}")

    print(f"Finished joining files into {output_file_path}")
