import os
import json

def add_svg_data():
    folder_path = "/Data/logo-cleaned-copy/"
    # Loop through each subfolder in the folder
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        print(f"Processing subfolder: {subfolder_path}")
        
        # Check if the current item is a directory before listing files
        if os.path.isdir(subfolder_path):
            # Check if the subfolder contains a json file
            if any(file.endswith(".json") for file in os.listdir(subfolder_path)):
                json_file_path = os.path.join(subfolder_path, "index.json")
                print(f"Processing json file: {json_file_path}")
                with open(json_file_path, "r") as f:
                    json_obj = json.load(f)
                    print(f"JSON object: {json_obj}")

                # Loop through each svg file in the subfolder
                for file in os.listdir(subfolder_path):
                    if file.endswith(".svg"):
                        svg_file_path = os.path.join(subfolder_path, file)
                        print(f"Processing svg file: {svg_file_path}")

                        # Read the contents of the svg file
                        with open(svg_file_path, "r") as f:
                            svg_content = f.read()
                            print(f"SVG content: {svg_content}")

                        # Extract the meta data from the svg file
                        meta = {
                            "filename": file,
                            "path": svg_file_path
                        }

                        # Add the svg data to the json object
                        json_obj["svg"].append({
                            "meta": meta,
                            "data": svg_content
                        })

                        # Print the meta data and svg content for the current file
                        print(f"Processing file: {file}")
                        print(f"Meta data: {meta}")
                        print(f"SVG content: {svg_content}")

                # Write the updated json object back to the file
                with open(json_file_path, "w") as f:
                    json.dump(json_obj, f, indent=4)
                    print(f"Updated JSON object: {json_obj}")