import os
import shutil

root_directory = "/Users/cyberton/Documents/svgscrape/Data/logos copy/"
destination_directory = "/Users/cyberton/Documents/svgscrape/Test Folder/logo-cleaned/"

# Loop through each subfolder in the root directory
for folder_name in [d for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d))]:
    folder_path = os.path.join(root_directory, folder_name)
    
    # Check if the folder contains an SVG file
    if any(file.endswith(".svg") for file in os.listdir(folder_path)):
        # Move the whole folder to the destination directory
        destination_path = os.path.join(destination_directory, folder_name)
        shutil.move(folder_path, destination_path)
        print(f"Moved '{folder_name}' to '{destination_path}'")
