from playwright.sync_api import sync_playwright
from celery import shared_task

from .extensions import db
from .models import Tag, Link

import re


@shared_task(bind=True, max_retries=3)
def fetch_metadata(url):
    """
    Fetch metadata from a URL using Playwright.
    Returns tuple of (title, description, image)
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # Evaluate JavaScript to get metadata
        metadata = page.evaluate("""() => {
            const getContent = (selector) => {
                const element = document.querySelector(selector);
                return element ? element.content : null;
            };

            return {
                title: document.title,
                description: getContent('meta[property="og:description"]') || 
                            getContent('meta[name="description"]'),
                image: getContent('meta[property="og:image"]')
            };
        }""")

        browser.close()

        return (
            metadata.get('title'),
            metadata.get('description'),
            metadata.get('image')
        )


@shared_task(bind=True, max_retries=3)
def process_assets(note):

    # Extract links
    link_matches = re.search(r'https?://\S+', note.text)
    for match in link_matches:
        link_url = match.group(0)
        title, description, image = fetch_metadata.delay(link_url).get()
        link = Link(url=link_url, title=title, description=description, image=image, note_id=note.id)

        db.session.add(link)

    db.session.commit()

    # Extract hashtags
    tags = re.findall(r'#\w+', note.text)
    for tag in tags:
        new_tag = Tag(tag=tag, note_id=note.id)
        db.session.add(new_tag)

    db.session.commit()
