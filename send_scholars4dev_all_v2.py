#!/usr/bin/env python3
"""
Send all scholarships from scholars4dev.com via Telegram without any filtering.
This version includes delays between messages to avoid rate limits.
"""
import requests
from bs4 import BeautifulSoup
import time
import sys
import os
sys.path.insert(0, '/root/scholarship_bot')

from telegram_notifier import TelegramNotifier
from models import Scholarship

def extract_text_from_elements(soup, tags=None, class_contains=None):
    """
    Extract text from elements matching criteria.
    Returns a list of text strings.
    """
    texts = []
    if tags:
        for tag in tags:
            elements = soup.find_all(tag)
            for el in elements:
                text = el.get_text(strip=True)
                if text and len(text) > 10:  # Avoid too short
                    texts.append(text)
    if class_contains:
        # Find elements whose class attribute contains the substring
        elements = soup.find_all(class_=lambda c: c and class_contains in c)
        for el in elements:
            text = el.get_text(strip=True)
            if text and len(text) > 10:
                texts.append(text)
    return texts

def main():
    print("=== Sending All Scholarships from scholars4dev.com (with delays) ===")

    # Initialize Telegram notifier
    notifier = TelegramNotifier()
    if not notifier.test_connection():
        print("❌ ERROR: Cannot connect to Telegram bot!")
        return 1

    print("✅ Telegram connection successful")

    # Define headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    # List of URLs to scrape on scholars4dev.com
    # We'll start with the main page and a few others that are likely to list scholarships
    urls = [
        "https://www.scholars4dev.com/",
        "https://www.scholars4dev.com/international-scholarships/",
        # Note: the international-scholarships page redirects to a specific scholarship, but we'll still try
        # We can also try the scholarships by level/field/country if they exist (they returned 404 earlier, but maybe with proper headers?)
        "https://www.scholars4dev.com/scholarships-by-level/",
        "https://www.scholars4dev.com/scholarships-by-field/",
        "https://www.scholars4dev.com/scholarships-by-country/",
    ]

    all_texts = []

    for url in urls:
        print(f"\n🔍 Scraping: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            print(f"  Status: {response.status_code}")
            print(f"  Final URL: {response.url} (after redirects)")
            print(f"  Content length: {len(response.text)}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract text from common elements that might contain scholarship info
                # We'll look for articles, posts, entries, headings, and elements with class containing certain keywords
                texts = []
                # Articles and posts
                texts.extend(extract_text_from_elements(soup, tags=['article']))
                texts.extend(extract_text_from_elements(soup, tags=['div'], class_contains='post'))
                texts.extend(extract_text_from_elements(soup, tags=['div'], class_contains='entry'))
                # Headings (often contain titles)
                texts.extend(extract_text_from_elements(soup, tags=['h1', 'h2', 'h3', 'h4']))
                # Elements with scholarship in class
                texts.extend(extract_text_from_elements(soup, class_contains='scholarship'))
                # Also get all text and split by lines as a fallback
                all_text = soup.get_text()
                lines = [line.strip() for line in all_text.split('\n') if line.strip()]
                # Filter lines that are reasonably long and contain scholarship-related terms
                scholarship_indicators = [
                    'scholarship', 'funded', 'grant', 'fellowship',
                    'master', 'phd', 'doctoral', 'undergraduate',
                    'apply', 'deadline', 'eligibility', 'award',
                    'university', 'college', 'institute', 'deadline', 'apply'
                ]
                for line in lines:
                    if len(line) > 20 and len(line) < 500:
                        if any(term in line.lower() for term in scholarship_indicators):
                            texts.append(line)

                # Deduplicate texts within this page (exact match)
                unique_texts = list(dict.fromkeys(texts))  # Preserves order
                print(f"  Found {len(unique_texts)} unique text blocks from {url}")
                all_texts.extend([(text, url) for text in unique_texts])
            else:
                print(f"  Failed to fetch {url}: Status {response.status_code}")

            # Be respectful: delay between requests to the same domain
            time.sleep(2)

        except Exception as e:
            print(f"  Error scraping {url}: {e}")

    # Deduplicate across all texts (by exact text)
    seen = set()
    unique_scholarships = []
    for text, url in all_texts:
        if text not in seen:
            seen.add(text)
            unique_scholarships.append({'text': text, 'url': url})

    print(f"\n📊 Total unique scholarship text blocks found: {len(unique_scholarships)}")

    if not unique_scholarships:
        print("ℹ️  No scholarships found.")
        return 0

    # Ask the user how many they want to send? Or send all with delays?
    # Since the user said "all current scholarships", we'll send all.
    # But we'll add a delay between each Telegram message to avoid rate limits.

    print("\n📤 Sending scholarships via Telegram (with 2-second delay between each)...")
    sent_count = 0
    failed_count = 0

    for i, schol in enumerate(unique_scholarships, 1):
        try:
            # Create a Scholarship object with the information we have
            # We don't have detailed structured data, so we'll put the text in description and leave other fields generic.
            scholarship_obj = Scholarship(
                title=schol['text'][:100] + ('...' if len(schol['text']) > 100 else ''),
                link=schol['url'],
                description=schol['text'],
                eligibility="See website for details",
                funding="See website for details",
                field="See website for details",
                level="See website for details",
                nationality="See website for details",
                source="scholars4dev.com"
            )

            print(f"  [{i}/{len(unique_scholarships)}] Sending: {scholarship_obj.title[:50]}...")
            if notifier.send_notification(scholarship_obj):
                sent_count += 1
                print(f"     ✅ Sent")
            else:
                failed_count += 1
                print(f"     ❌ Failed to send")

            # Wait 2 seconds before sending the next message to avoid rate limits
            if i < len(unique_scholarships):  # Don't wait after the last one
                print(f"     ⏳ Waiting 2 seconds before next message...")
                time.sleep(2)

        except Exception as e:
            failed_count += 1
            print(f"     ❌ Error: {e}")

    print(f"\n📊 Results:")
    print(f"   ✅ Successfully sent: {sent_count}")
    print(f"   ❌ Failed to send: {failed_count}")
    print(f"   📝 Total processed: {len(unique_scholarships)}")

    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())