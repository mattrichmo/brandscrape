import os
import yaml
import json

class Brand:
    def __init__(self, title, website, logo):
        self.brandName = title
        self.brandWebsite = website
        self.brandLogo = logo

root_directory = "/Users/cyberton/Documents/svgscrape/Test Folder/md"

def process_md_file(md_file_path):
    with open(md_file_path, 'r') as index_md_file:
        md_data_list = yaml.safe_load_all(index_md_file)

    for index, md_data in enumerate(md_data_list, start=1):
        title = md_data.get('title', '')
        website = md_data.get('website', '')

        logos = []
        for root, dirs, files in os.walk(os.path.dirname(md_file_path)):
            for svg_file in files:
                if svg_file.endswith('.svg'):
                    svg_path = os.path.join(root, svg_file)
                    with open(svg_path, 'r') as svg_file:
                        svg_data = svg_file.read()
                    logos.append({"path": svg_file, "svg data": svg_data})

        if title and website and logos:
            brand = Brand(title, website, logos)
            json_data = json.dumps(brand.__dict__, indent=4)
            json_filename = f"{title}_{index}.json"
            json_path = os.path.join(os.path.dirname(md_file_path), json_filename)

            with open(json_path, 'w') as json_file:
                json_file.write(json_data)

            print(f"Created {json_filename} in {os.path.dirname(md_file_path)}")

for root, dirs, files in os.walk(root_directory):
    for file in files:
        if file == "index.md":
            md_file_path = os.path.join(root, file)
            process_md_file(md_file_path)
