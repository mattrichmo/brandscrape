import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define the root folder where your thousands of folders are located
root_folder = '/Users/cyberton/Documents/svgscrape/Test Folder'

# Define the destination folder where you want to save the SVG files
destination_folder = './Data/'

# Define a function to download SVG files
def download_svg(src_url, dest_path):
    response = requests.get(src_url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as svg_file:
            svg_file.write(response.content)
        return True
    else:
        return False

# Iterate through all folders and subfolders
for root, _, files in os.walk(root_folder):
    for file in files:
        if file == 'index.htm' or file == 'index.html':
            # Construct the full path to the HTML file
            html_file_path = os.path.join(root, file)

            # Parse the HTML file using BeautifulSoup
            with open(html_file_path, 'r', encoding='utf-8') as html_file:
                soup = BeautifulSoup(html_file, 'html.parser')

            # Find all <a> tags with download attribute and href ending in .svg
            svg_links = soup.find_all('a', {'download': True, 'href': re.compile(r'.*\.svg$')})

            for svg_link in svg_links:
                # Get the href attribute value
                src_url = svg_link['href']

                # Get the folder name from the original folder structure
                folder_name = os.path.basename(root)

                # Construct the destination folder path
                folder_path = os.path.join(destination_folder, folder_name)

                # Create the destination folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Parse the URL to extract the SVG file name
                parsed_url = urlparse(src_url)
                svg_file_name = os.path.basename(parsed_url.path)

                # Construct the destination path for the SVG file
                dest_path = os.path.join(folder_path, svg_file_name)

                # Print the SVG file name
                print(f"SVG file found: {svg_file_name}")

                # Download the SVG file and save it to the destination folder
                if download_svg(src_url, dest_path):
                    print(f"Downloaded: {src_url} to {dest_path}")
                else:
                    print(f"Failed to download: {src_url}")

print("Task completed. All SVG files have been downloaded.")
