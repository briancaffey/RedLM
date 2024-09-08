import os

# Specify the folder path
folder_path = "/home/brian/github/HLLM/hllm/data/paintings"

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    # Check if the file starts with "0" or "00"
    if filename.startswith("00"):
        new_filename = filename[2:]  # Remove first two characters
    elif filename.startswith("0"):
        new_filename = filename[1:]  # Remove first character
    else:
        continue  # Skip files that don't start with "0" or "00"

    # Get the full path of the old and new filenames
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)

    # Rename the file
    os.rename(old_file, new_file)
    print(f"Renamed: {filename} -> {new_filename}")
