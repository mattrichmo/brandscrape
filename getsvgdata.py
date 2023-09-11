import os
import csv
import json
import time
import xml.etree.ElementTree as ET
import shutil

def create_svgdata():
    project = './svgscrape'
    directory = './Data/logo-cleaned'  # Replace with your directory path
    project_directory = os.path.abspath(os.path.join(directory, os.pardir))  # Get the parent directory of the Data folder
    svg_data_list = []
    csv_file_path = None  # Variable to store the CSV file path
    for dir_root, dirs, files in os.walk(directory):
        subfolder_svg_data_list = []  # List to hold SVG data for each subfolder
        for file in files:
            if file.endswith('.svg'):
                file_path = os.path.join(dir_root, file)
                print(f'Reading file: {file_path}')
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    svg_data = f.read()
                    tree = ET.ElementTree(ET.fromstring(svg_data))
                    xml_root = tree.getroot()
                    meta = {key: xml_root.attrib.get(key, '') for key in xml_root.keys()}
                    width = meta.get('width', '')
                    height = meta.get('height', '')
                    viewbox = meta.get('viewBox', '')
                    fill = meta.get('fill', '')
                    svg_data_list.append({
                        'fileName': file,
                        'svgPath': os.path.relpath(file_path, project),
                        'svgData': {
                            'meta': meta,
                            'svgRaw': svg_data
                        },
                        'width': width,
                        'height': height,
                        'viewbox': viewbox,
                        'fill': fill
                    })
                    subfolder_svg_data_list.append({
                        'fileName': file,
                        'svgPath': os.path.relpath(file_path, project),  # Use the relative path to the Data folder
                        'svgData': {
                            'meta': meta,
                            'svgRaw': svg_data
                        },
                        'width': width,
                        'height': height,
                        'viewbox': viewbox,
                        'fill': fill
                    })
        # Create SVG data JSON file for each subfolder
        if subfolder_svg_data_list:
            subfolder_name = os.path.basename(dir_root)
            subfolder_svgdata_file = os.path.join(dir_root, f'{subfolder_name}_svgdata.json')  # Save the file in the same subfolder
            with open(subfolder_svgdata_file, 'w') as subfolder_json_file:
                json.dump(subfolder_svg_data_list, subfolder_json_file, indent=4)

    # Create master SVG data JSON file
    timestamp = int(time.time())
    master_svgdata_file = os.path.join(directory, f'master_svgdata_{timestamp}.json')
    if svg_data_list:
        with open(master_svgdata_file, 'w') as json_file:
            json.dump(svg_data_list, json_file, indent=4)
    elif os.path.exists(master_svgdata_file):
        os.remove(master_svgdata_file)
        print(f'Removed empty file: {master_svgdata_file}')

    # Move master SVG data JSON file to parent folder
    parent_directory = os.path.join(directory, '../master')
    os.makedirs(parent_directory, exist_ok=True)
    master_svgdata_newpath = os.path.join(parent_directory, f'master_svgdata_{timestamp}.json')
    shutil.move(master_svgdata_file, master_svgdata_newpath)

    # Create CSV file in the same folder as the master SVG data JSON file
    csv_file_path = os.path.join(parent_directory, f'master_svgdata_{timestamp}.csv')
    headers = ['fileName', 'svgPath', 'width', 'height', 'viewbox', 'fill', 'meta', 'svgRaw']
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for svg_data in svg_data_list:
            row = [
                svg_data['fileName'],
                os.path.join(project_directory, svg_data['svgPath']),  # Use the full path to the SVG file
                svg_data['width'],
                svg_data['height'],
                svg_data['viewbox'],
                svg_data['fill'],
                json.dumps(svg_data['svgData']['meta']),
                svg_data['svgData']['svgRaw']
            ]
            writer.writerow(row)

    print(f'CSV file saved: {csv_file_path}')

# Example usage
create_svgdata()