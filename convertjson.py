import os
import json
import re

# Define the folder to search for subfolders with md files
folder_path = "/Users/cyberton/Documents/svgscrape/Data/logo-cleaned"

# Loop through each subfolder in the folder
for subfolder in os.listdir(folder_path):
    subfolder_path = os.path.join(folder_path, subfolder)
    
    # Check if the subfolder contains md files
    if any(file.endswith(".md") for file in os.listdir(subfolder_path)):
        print(f"Processing folder: {subfolder}")
        # Loop through each md file in the subfolder
        for file in os.listdir(subfolder_path):
            if file.endswith(".md"):
                file_path = os.path.join(subfolder_path, file)
                
                # Read the contents of the md file
                with open(file_path, "r") as f:
                    md_content = f.read()
                
                # Extract the title, website, and logo images from the md content
                title = re.search(r"title:\s*(.*)", md_content).group(1)
                website = re.search(r"website:\s*(.*)", md_content).group(1)
                logo_images = re.findall(r"images:\s*(-\s*.*)", md_content)
                
                # Extract all other links and properties from the md content
                links = {}
                other = {}
                for line in md_content.split("\n"):
                    match = re.search(r"(\w+):\s*(.*)", line)
                    if match:
                        key, value = match.groups()
                        if key not in ["title", "website", "images"]:
                            if key in ["facebook", "github", "linkedin", "twitter", "wikipedia"]:
                                links[key] = value
                            else:
                                other[key] = value
                
                # Create the JSON object
                json_obj = {
                    "title": title,
                    "website": website,
                    "links": links,
                    "logos": logo_images,
                    "other": other
                }
                
                # Write the JSON object to a file in the same folder as the md file
                json_file_path = os.path.splitext(file_path)[0] + ".json"
                with open(json_file_path, "w") as f:
                    json.dump(json_obj, f, indent=4)
                    
                print(f"Processed file: {file}")
                    
        print(f"Finished processing folder: {subfolder}")