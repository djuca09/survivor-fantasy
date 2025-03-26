import requests
from bs4 import BeautifulSoup
import src.castaway
import re

def update_castaway_points(URL : str , castaways : list[src.castaway.Castaway]):
    """Scrapes the latest Survivor Fantasy points from the website."""
    
    # Fetch the webpage
    response = requests.get(URL)
    response.raise_for_status()  # Raise an error if the request fails
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the image tag containing the points
    img_tags = soup.find_all("img", class_=lambda c: c and "wp-image-" in c)  # Class specific to the points image
 
    points_by_week = []

    for img in img_tags:
        alt_text = img.get("alt", "")
        
        if alt_text:
            points_data = {}
            # Extract castaway names and points from alt text
            for entry in re.split(r"[;,]", alt_text):
                entry = entry.strip()
                if "total points" in entry:
                    # Regex to match both formats and extract name + points
                    match = re.match(r"([\w\s]+?)(?: episode \d+)? total points: (\d+)", entry)
                    
                    if match:
                        name = match.group(1).strip()  # Extract name
                        points = int(match.group(2))   # Extract points
                        points_data[name] = int(points)
        
        points_by_week.append(points_data)

    points_by_week.sort(key=len)

    for castaway in castaways:

        latest_week_number = len(points_by_week)+1

        for week in points_by_week:
            castaway.set_weekly_points(latest_week_number,week.get(castaway.name(),0))
            latest_week_number -= 1

    # Search for the text pattern (using regex)
    tip_pattern = re.compile(r"Tip: Don’t forget to add an additional 30 bonus points to your total score if you chose (.+?) as your MVP.*", re.IGNORECASE)

    winner = None
    # Search all text in the page for winner
    for text in soup.stripped_strings:
        match = tip_pattern.search(text)
        if match:
            winner = match.group(1)  # winner's name

            for castaway in castaways: #update castaway
                if castaway.name() == winner:
                    castaway.won()       