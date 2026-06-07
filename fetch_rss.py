#!/usr/bin/env python3
"""
Fetch and display the RSS feed from http://www.scholars4dev.com/feed/
"""
import requests
import xml.etree.ElementTree as ET
from html import unescape
import sys

def fetch_rss_feed(url):
    """Fetch the RSS feed from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return None

def parse_rss_feed(xml_content):
    """Parse the RSS feed XML and return a list of items."""
    try:
        root = ET.fromstring(xml_content)
        # Find the channel element
        channel = root.find('channel')
        if channel is None:
            print("No channel element found in RSS feed")
            return []

        items = []
        for item in channel.findall('item'):
            # Extract common fields
            title = item.findtext('title', default='').strip()
            link = item.findtext('link', default='').strip()
            pub_date = item.findtext('pubDate', default='').strip()
            description = item.findtext('description', default='').strip()

            # Also check for content:encoded (often used for full HTML content)
            content_encoded = item.find('./{http://purl.org/rss/1.0/modules/content/}encoded')
            if content_encoded is not None and content_encoded.text:
                description = content_encoded.text.strip()

            # Clean up HTML entities in description
            if description:
                description = unescape(description)
                # Truncate description for display
                if len(description) > 200:
                    description = description[:200] + "..."

            items.append({
                'title': title,
                'link': link,
                'pub_date': pub_date,
                'description': description
            })
        return items
    except ET.ParseError as e:
        print(f"Error parsing RSS feed: {e}")
        return []

def display_feed(items):
    """Display the RSS feed items in a readable format."""
    if not items:
        print("No items found in the RSS feed.")
        return

    print(f"\nFound {len(items)} scholarship listings from scholars4dev.com RSS feed:\n")
    print("=" * 80)

    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")
        print(f"   Link: {item['link']}")
        if item['pub_date']:
            print(f"   Published: {item['pub_date']}")
        if item['description']:
            print(f"   Description: {item['description']}")
        print("-" * 80)

def main():
    rss_url = "http://www.scholars4dev.com/feed/"
    print(f"Fetching RSS feed from {rss_url}...")

    xml_content = fetch_rss_feed(rss_url)
    if xml_content is None:
        sys.exit(1)

    items = parse_rss_feed(xml_content)
    display_feed(items)

if __name__ == "__main__":
    main()