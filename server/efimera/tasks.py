from playwright.sync_api import sync_playwright
from celery import shared_task, chain

from .extensions import db
from .models import Tag, Link, Note

import re


@shared_task(bind=True, max_retries=3)
def save_metadata(self, link_id, metadata):
    Link.query.filter_by(id=link_id).update(metadata)

    db.session.commit()


@shared_task(bind=True, max_retries=3)
def fetch_content(self, url, link_id):
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

        save_metadata.delay(link_id, metadata)


@shared_task(bind=True, max_retries=3)
def process_assets(self, note_id):
    note = Note.query.get(note_id)

    # Extract links
    link_matches = re.finditer(r'https?://\S+', note.text)
    for match in link_matches:
        link_url = match.group(0)

        link = Link(url=link_url, note_id=note_id)

        db.session.add(link)
        db.session.commit()

        fetch_content.delay(link_url, link.id)

    # Extract hashtags
    tags = re.findall(r'#\w+', note.text)
    for tag in tags:
        new_tag = Tag(tag=tag, note_id=note.id)
        db.session.add(new_tag)

    db.session.commit()
