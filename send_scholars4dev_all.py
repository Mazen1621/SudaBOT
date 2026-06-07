#!/usr/bin/env python3
"""
Send all scholarships from scholars4dev.com via Telegram without any filtering.
"""
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
sys.path.insert(0, '/root/scholarship_bot')

from telegram_notifier import TelegramNotifier
from models import Scholarship

def extract_scholarships_from_page(url, headers):
    """Scrape a page for scholarship listings."""
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"  Failed to fetch {url}: Status {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]

        scholarship_indicators = [
            'scholarship', 'funded', 'grant', 'fellowship',
            'master', 'phd', 'doctoral', 'undergraduate',
            'apply', 'deadline', 'eligibility', 'award',
            'university', 'college', 'institute'
        ]

        potential_scholarships = []
        for line in lines:
            if len(line) > 20 and len(line) < 500:  # Reasonable length
                # Check if it contains scholarship-related terms
                if any(term in line.lower() for term in scholarship_indicators):
                    potential_scholarships.append(line)

        # Also look for specific patterns like "Deadline:" or "Apply by:"
        # We'll add a few more indicators
        deadline_indicators = ['deadline', 'apply by', 'closes', 'due date']
        for line in lines:
            if any(indicator in line.lower() for indicator in deadline_indicators) and len(line) > 20 and len(line) < 500:
                if line not in potential_scholarships:
                    potential_scholarships.append(line)

        return potential_scholarships[:20]  # Limit to avoid too many messages
    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return []

def main():
    print("=== Sending All Scholarships from scholars4dev.com ===")

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
    urls = [
        "https://www.scholars4dev.com/",
        "https://www.scholars4dev.com/international-scholarships/",
        # Add more pages if needed
    ]

    all_scholarships = []

    for url in urls:
        print(f"\n🔍 Scraping: {url}")
        scholarships = extract_scholarships_from_page(url, headers)
        print(f"  Found {len(scholarships)} potential scholarships")
        for scholarship in scholarships:
            all_scholarships.append({
                'text': scholarship,
                'url': url
            })

    # Remove duplicates based on the text
    unique_scholarships = []
    seen = set()
    for schol in all_scholarships:
        if schol['text'] not in seen:
            seen.add(schol['text'])
            unique_scholarships.append(schol)

    print(f"\n📊 Total unique scholarships found: {len(unique_scholarships)}")

    if not unique_scholarships:
        print("ℹ️  No scholarships found.")
        return 0

    # Send each scholarship via Telegram
    print("\n📤 Sending scholarships via Telegram...")
    sent_count = 0
    failed_count = 0

    for i, schol in enumerate(unique_scholarships, 1):
        try:
            # Create a Scholarship object with the information we have
            scholarship_obj = Scholarship(
                title=schol['text'][:100] + ('...' if len(schol['text']) > 100 else ''),
                link=schol['url'],
                description=schol['text'],
                eligibility="See website for details",  # We don't have this info
                funding="See website for details",      # We don't have this info
                field="See website for details",        # We don't have this info
                level="See website for details",        # We don't have this info
                nationality="See website for details",  # We don't have this info
                source="scholars4dev.com"
            )

            print(f"  [{i}/{len(unique_scholarships)}] Sending: {scholarship_obj.title[:50]}...")
            if notifier.send_notification(scholarship_obj):
                sent_count += 1
                print(f"     ✅ Sent")
            else:
                failed_count += 1
                print(f"     ❌ Failed to send")
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