import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import sqlite3

# Define the root folder where your thousands of folders are located
root_folder = '/Users/cyberton/Documents/svgscrape/Test Folder'

# Define the destination folder where you want to save the SVG files
destination_folder = './Data/'

# Load the existing data from data.json
with open('data.json', 'r', encoding='utf-8') as json_file:
    existing_data = json.load(json_file)

# Create an empty list to store brand names and logos
brand_data = []

# Create or connect to an SQLite database
db_path = 'brand_logos.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define a function to create the database table
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS brand_logos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       brand_name TEXT,
                       logo_path TEXT)''')

# Define a function to insert data into the database
def insert_data(brand_name, logo_path):
    cursor.execute("INSERT INTO brand_logos (brand_name, logo_path) VALUES (?, ?)", (brand_name, logo_path))
    conn.commit()

# Create the table in the database
create_table()

# Define a function to download SVG files
def download_svg(src_url, dest_path):
    response = requests.get(src_url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as svg_file:
            svg_file.write(response.content)
        
        # Print the SVG file being downloaded
        print(f"Downloaded: {src_url} to {dest_path}")
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

            # Find the H1 tag and set it as BrandName
            h1_tag = soup.find('h1')
            brand_name = h1_tag.get_text() if h1_tag else None

            # Find all <a> tags with download attribute and href ending in .svg
            svg_links = soup.find_all('a', {'download': True, 'href': re.compile(r'.*\.svg$')})

            # Create a list to store the logos
            logos = []

            for svg_link in svg_links:
                # Get the href attribute value
                src_url = svg_link['href']

                # Parse the URL to extract the SVG file name
                parsed_url = urlparse(src_url)
                svg_file_name = os.path.basename(parsed_url.path)

                # Construct the destination folder path
                folder_name = os.path.basename(root)
                folder_path = os.path.join(destination_folder, folder_name)

                # Create the destination folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Construct the destination path for the SVG file
                dest_path = os.path.join(folder_path, svg_file_name)

                # Download the SVG file and update the logos list
                if download_svg(src_url, dest_path):
                    logos.append({
                        "Logo": dest_path,
                        "LogoType": "svg"
                    })
                    # Insert data into the database
                    insert_data(brand_name, dest_path)

            # Add the brand name and logos to the brand_data list
            if brand_name and logos:
                brand_data.append({
                    "BrandName": brand_name,
                    "BrandLogo": logos
                })

# Update the existing_data dictionary with the extracted data
existing_data = {
    "BrandData": brand_data
}

# Write the updated data back to data.json
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

print("Data.json updated with extracted information.")
