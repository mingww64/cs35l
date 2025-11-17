import os
import zipfile

def create_archive(directory='.', output_filename='assign5_solution.zip'):
    """
    Zips all files and folders, including hidden ones like .git,
    in the specified directory into a single zip file.

    Args:
        directory (str): The path to the directory to archive (default is the current folder).
        output_filename (str): The name of the resulting zip file.
    """
    # Check if the output filename is the same as a file/folder we are trying to archive.
    if os.path.abspath(output_filename) == os.path.abspath(directory):
        print(f"Error: The output file '{output_filename}' cannot be the same as the input directory.")
        return

    print(f"Starting archival of '{directory}' into '{output_filename}'...")

    try:
        # Open the zip file in write mode
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # os.walk traverses the directory tree. It includes all subdirectories
            # and files by default, which correctly handles the .git folder.
            for foldername, subfolders, filenames in os.walk(directory):
                # We need to calculate the relative path to ensure the zip file
                # doesn't contain the full absolute path from your system's root.
                # For '.' (current directory), this removes the leading '.'
                archive_root = os.path.relpath(foldername, directory)

                # 1. Add the current folder itself (important for empty folders and root)
                if archive_root and archive_root != '.':
                     zipf.write(foldername, archive_root)

                # 2. Add all files in the current folder
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    # Create the path inside the zip, maintaining the relative structure
                    print(f"  Archiving: {file_path}")
                    archive_path = os.path.join(archive_root, filename)

                    # Do not archive the zip file itself if it's in the current directory
                    if file_path != output_filename:
                        zipf.write(file_path, archive_path)
                        # print(f"  Added: {archive_path}")

        print(f"\nSuccessfully created archive: '{output_filename}'")
        print("All files and subfolders (including .git) are included.")

    except Exception as e:
        print(f"\nAn error occurred during archival: {e}")

if __name__ == "__main__":
    create_archive()