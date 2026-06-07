#!/usr/bin/env python3
"""
Script to send all currently known scholarships (not just new ones) via Telegram.
Useful for initial batch sending or periodic comprehensive updates.
"""
import os
import sys
sys.path.insert(0, '/root/scholarship_bot')

from scraper_manager import ScraperManager
from filter import ScholarshipFilter
from storage import Storage
from telegram_notifier import TelegramNotifier
from models import Scholarship

def main():
    print("=== Sending All Currently Open Scholarships ===")

    # Initialize components
    scraper_manager = ScraperManager()
    scholarship_filter = ScholarshipFilter()
    storage = Storage()  # Uses default scholarships_seen.db
    notifier = TelegramNotifier()

    # Test Telegram connection first
    if not notifier.test_connection():
        print("❌ ERROR: Cannot connect to Telegram bot!")
        return 1

    print("✅ Telegram connection successful")

    # Scrape all sites
    print("\n🔍 Scraping all scholarship sources...")
    raw_scholarships = scraper_manager.scrape_all()
    print(f"📊 Found {len(raw_scholarships)} raw scholarships")

    # Filter scholarships based on criteria
    print("\n🎯 Filtering for relevant scholarships...")
    filtered_scholarships = scholarship_filter.filter(raw_scholarships)
    print(f"✅ {len(filtered_scholarships)} scholarships match your criteria")

    if not filtered_scholarships:
        print("ℹ️  No scholarships found matching your criteria.")
        print("💡 This could be due to:")
        print("   - Website access issues (sites blocking scrapers)")
        print("   - No currently open scholarships matching your profile")
        print("   - Need to adjust filtering criteria")
        return 0

    # Send ALL filtered scholarships (not just new ones)
    print("\n📤 Sending all matching scholarships via Telegram...")
    sent_count = 0
    failed_count = 0

    for i, scholarship in enumerate(filtered_scholarships, 1):
        try:
            print(f"  [{i}/{len(filtered_scholarships)}] Sending: {scholarship.title[:50]}...")
            if notifier.send_notification(scholarship):
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
    print(f"   📝 Total processed: {len(filtered_scholarships)}")

    # Optionally, you could mark all as seen to avoid duplicates in future runs
    # Uncomment the following lines if you want to treat this as setting the "baseline"
    # print("\n💾 Marking all scholarships as seen to avoid future duplicates...")
    # for scholarship in filtered_scholarships:
    #     storage.mark_as_seen(scholarship)
    # print("   ✅ Baseline established")

    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())