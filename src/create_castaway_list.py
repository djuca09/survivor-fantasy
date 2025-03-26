import requests
from bs4 import BeautifulSoup
import json
import os
import re

URL = "https://www.globaltv.com/survivor-47-fantasy-tribe/#results"

# Fetch the webpage
response = requests.get(URL)
response.raise_for_status()  # Raise an error if the request fails

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find the image tag containing the points
img_tag = soup.find("img", class_="wp-image-127848")

# Extract alt text and process names
alt_text = img_tag.get("alt", "")
castaways = []



for entry in re.split(r"[;,]", alt_text):
                entry = entry.strip()
                if "total points" in entry:
                    # Regex to match both formats and extract name + points
                    match = re.match(r"([\w\s]+?)(?: episode \d+)? total points: (\d+)", entry)
                    
                    if match:
                        name = match.group(1).strip()  # Extract name
                        castaways.append(name)

# Ensure the directory exists before saving
output_path = "data/s47/s47_castaway_list.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to JSON file
with open(output_path, "w") as file:
    json.dump(castaways, file, indent=4)

print(f"✅ Castaway list saved to {output_path}")
