from bs4 import BeautifulSoup

from .extensions import db
from .models import Note, Tag, Link

import requests
import re

def fetch_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('title').text if soup.find('title') else None
    description = None
    image = None

    # Find description
    if soup.find("meta", property="og:description"):
        description = soup.find("meta", property="og:description")["content"]
    elif soup.find("meta", attrs={"name": "description"}):
        description = soup.find("meta", attrs={"name": "description"})["content"]

    # Find image
    if soup.find("meta", property="og:image"):
        image = soup.find("meta", property="og:image")["content"]

    return title, description, image

def save_data_to_db(text_blob):
    # Save the original text to the notes table
    note = Note(text=text_blob)
    db.session.add(note)
    db.session.commit()

    # Extract the link (assuming it starts with "http" or "https")
    link_match = re.search(r'https?://\S+', text_blob)
    if link_match:
        link_url = link_match.group(0)
        title, description, image = fetch_metadata(link_url)
        link = Link(url=link_url, title=title, description=description, image=image, note_id=note.id)

        db.session.add(link)
        db.session.commit()
    else:
        raise ValueError("No link found in the text blob")

    # Extract hashtags
    tags = re.findall(r'#\w+', text_blob)
    for tag in tags:
        new_tag = Tag(tag=tag, note_id=note.id)
        db.session.add(new_tag)

    db.session.commit()
