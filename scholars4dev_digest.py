#!/usr/bin/env python3
"""
Fetch scholarship listings from scholars4dev.com and send a digest via Telegram.
"""
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
sys.path.insert(0, '/root/scholarship_bot')

from telegram_notifier import TelegramNotifier
from models import Scholarship

def fetch_scholarships():
    """Fetch scholarship listings from scholars4dev.com."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    # We'll try several pages that likely list scholarships
    urls = [
        "https://www.scholars4dev.com/",
        "https://www.scholars4dev.com/international-scholarships/",
        "https://www.scholars4dev.com/scholarships-by-level/",
        "https://www.scholars4dev.com/scholarships-by-field/",
        "https://www.scholars4dev.com/scholarships-by-country/",
    ]

    scholarships = []  # each will be dict with title, link, excerpt

    for url in urls:
        try:
            print(f"Fetching {url}")
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                print(f"  Status {resp.status_code}, skipping")
                continue
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Look for articles/posts
            articles = soup.find_all('article')
            if not articles:
                # Fallback: look for divs with class containing post or entry
                articles = soup.find_all('div', class_=lambda c: c and ('post' in c.lower() or 'entry' in c.lower()))

            for article in articles:
                # Try to get title
                title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                if not title_elem:
                    # Sometimes title is in a link
                    title_elem = article.find('a')
                title = title_elem.get_text(strip=True) if title_elem else "No title"

                # Try to get link
                link_elem = article.find('a', href=True)
                if link_elem:
                    link = link_elem['href']
                    # Make absolute if needed
                    if not link.startswith('http'):
                        if link.startswith('/'):
                            link = 'https://www.scholars4dev.com' + link
                        else:
                            link = 'https://www.scholars4dev.com/' + link
                else:
                    link = url

                # Get excerpt (first paragraph or first 200 chars)
                excerpt_elem = article.find('p')
                if excerpt_elem:
                    excerpt = excerpt_elem.get_text(strip=True)
                else:
                    # Get text and truncate
                    text = article.get_text(strip=True)
                    excerpt = (text[:200] + '...') if len(text) > 200 else text

                if title and title != "No title":
                    scholarships.append({
                        'title': title,
                        'link': link,
                        'excerpt': excerpt,
                        'source': url
                    })
        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Deduplicate by title and link
    seen = set()
    unique = []
    for s in scholarships:
        key = (s['title'], s['link'])
        if key not in seen:
            seen.add(key)
            unique.append(s)

    return unique

def format_digest_message(scholarships):
    """Format a digest message for Telegram."""
    if not scholarships:
        return "No scholarships found on scholars4dev.com."

    msg = f"*scholars4dev.com Scholarship Digest*\n"
    msg += f"Found {len(scholarships)} scholarship listings.\n\n"

    for i, schol in enumerate(scholarships, 1):
        # Truncate title if too long
        title = schol['title']
        if len(title) > 80:
            title = title[:77] + "..."
        msg += f"{i}. *{title}*\n"
        msg += f"   🔗 {schol['link']}\n"
        # Optionally add excerpt
        # if schol['excerpt']:
        #     excerpt = schol['excerpt']
        #     if len(excerpt) > 100:
        #         excerpt = excerpt[:97] + "..."
        #     msg += f"   📝 {excerpt}\n"
        msg += "\n"

        # Telegram message limit is 4096 characters, we'll break if needed
        if len(msg) > 3500:
            msg += f"\n_And {len(scholarships) - i} more..._"
            break

    return msg

def main():
    notifier = TelegramNotifier()
    if not notifier.test_connection():
        print("❌ ERROR: Cannot connect to Telegram bot!")
        return 1

    print("✅ Telegram connection successful")

    print("🔍 Fetching scholarships from scholars4dev.com...")
    scholarships = fetch_scholarships()
    print(f"📊 Found {len(scholarships)} scholarships")

    if scholarships:
        print("First few:")
        for i, s in enumerate(scholarships[:3], 1):
            print(f"  {i}. {s['title']} - {s['link']}")

    message = format_digest_message(scholarships)
    print("\n📤 Sending digest message via Telegram...")
    if notifier.send_notification(Scholarship(
        title="scholars4dev.com Digest",
        link="https://www.scholars4dev.com/",
        description=message,
        eligibility="",
        funding="",
        field="",
        level="",
        nationality="",
        source="scholars4dev.com"
    )):
        print("✅ Digest message sent successfully!")
    else:
        print("❌ Failed to send digest message")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())