#!/usr/bin/env python3
"""
Main script for the Scholarship Bot.
Orchestrates scraping, filtering, deduplication, and notification.
Designed for continuous automated operation via GitHub Actions or similar services.
"""
import logging
import schedule
import time
import os
import sys
import argparse
from datetime import datetime
from scraper_manager import ScraperManager
from filter import ScholarshipFilter
from storage import Storage
from telegram_notifier import TelegramNotifier
from models import Scholarship

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scholarship_bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Scholarship Bot - Find and notify about scholarships')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run the bot in dry-run mode (no Telegram notifications sent)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run the job once and exit (do not schedule recurring runs)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=6,
        help='Schedule interval in hours (default: 6)'
    )
    return parser.parse_args()

def job(dry_run: bool = False):
    """Job to be scheduled: scrape, filter, deduplicate, and notify."""
    logger.info("=" * 60)
    logger.info("Starting scholarship scraping job")
    logger.info(f"Job started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if dry_run:
        logger.info("🧪 DRY-RUN MODE: No notifications will be sent")

    # Initialize components
    try:
        scraper_manager = ScraperManager()
        scholarship_filter = ScholarshipFilter()
        storage = Storage()
        notifier = TelegramNotifier()
        logger.info("All components initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return

    # Test Telegram connection first (skip in dry-run mode)
    if not dry_run:
        if not notifier.test_connection():
            logger.error("Cannot connect to Telegram bot! Aborting job.")
            return
        logger.info("✅ Telegram connection verified")
    else:
        logger.info("🧪 Skipping Telegram connection test in dry-run mode")

    # Scrape all sites
    logger.info("🔍 Starting scholarship scraping process...")
    raw_scholarships = scraper_manager.scrape_all()
    logger.info(f"📊 Scraped {len(raw_scholarships)} raw scholarships from all sources")

    if len(raw_scholarships) == 0:
        logger.warning("⚠️  No raw scholarships found - this may indicate website access issues")
        logger.info("💡 The bot will continue running and will try again in the next cycle")
        # Still complete the job to maintain schedule
        logger.info("Job completed (no data found)")
        return

    # Filter scholarships based on criteria
    logger.info("🎯 Applying relevance filters...")
    filtered_scholarships = scholarship_filter.filter(raw_scholarships)
    logger.info(f"✅ {len(filtered_scholarships)} scholarships match your criteria after filtering")

    if len(filtered_scholarships) == 0:
        logger.info("ℹ️  No scholarships matched your specific criteria")
        logger.info("💡 Consider adjusting filter criteria if this persists")
        logger.info("Job completed (no matches)")
        return

    # Remove duplicates (based on storage)
    logger.info("🔄 Checking for duplicate scholarships...")
    new_scholarships = []
    duplicate_count = 0

    for scholarship in filtered_scholarships:
        if not storage.is_seen(scholarship):
            new_scholarships.append(scholarship)
            storage.mark_as_seen(scholarship)
        else:
            duplicate_count += 1

    logger.info(f"📋 Found {len(new_scholarships)} NEW scholarships")
    logger.info(f"🔁 Skipped {duplicate_count} duplicate scholarships")

    if len(new_scholarships) == 0:
        logger.info("ℹ️  No new scholarships to report this cycle")
        logger.info("Job completed (no new data)")
        return

    # Notify via Telegram (unless in dry-run mode)
    logger.info("📤 Sending scholarship notifications via Telegram...")
    sent_count = 0
    failed_count = 0

    for i, scholarship in enumerate(new_scholarships, 1):
        try:
            # Log the scholarship being sent for debugging
            logger.info(f"  [{i}/{len(new_scholarships)}] Preparing to send: {scholarship.title[:60]}...")

            if dry_run:
                logger.info(f"     🧪 [DRY-RUN] Would send: {scholarship.title}")
                sent_count += 1  # Count as sent in dry-run for statistics
            elif notifier.send_notification(scholarship):
                sent_count += 1
                logger.info(f"     ✅ Sent successfully")
            else:
                failed_count += 1
                logger.error(f"     ❌ Failed to send notification")

        except Exception as e:
            failed_count += 1
            logger.error(f"     ❌ Error sending notification: {e}", exc_info=True)

    # Final summary
    logger.info("=" * 60)
    logger.info("JOB COMPLETION SUMMARY")
    logger.info(f"  🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"  📊 Raw scholarships found: {len(raw_scholarships)}")
    logger.info(f"  ✅ After filtering: {len(filtered_scholarships)}")
    logger.info(f"  🆕 New scholarships: {len(new_scholarships)}")
    logger.info(f"  🔁 Duplicates skipped: {duplicate_count}")
    if dry_run:
        logger.info(f"  📬 Notifications would be sent: {sent_count}")
    else:
        logger.info(f"  📬 Notifications sent: {sent_count}")
    logger.info(f"  ❌ Notifications failed: {failed_count}")
    if sent_count + failed_count > 0:
        success_rate = sent_count/(sent_count+failed_count)*100
        logger.info(f"  ✅ Success rate: {success_rate:.1f}%")
    else:
        logger.info(f"  ✅ Success rate: N/A")
    logger.info("=" * 60)

def main():
    """Main entry point for the scholarship bot."""
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("🚀 Scholarship Bot Starting Up")
    logger.info("=" * 50)

    # Log configuration
    logger.info(f"📍 Working directory: {os.getcwd()}")
    logger.info(f"🐍 Python version: {sys.version}")
    if args.once:
        logger.info("⏰ Schedule: Run once and exit")
    else:
        logger.info(f"⏰ Schedule: Every {args.interval} hours")
    logger.info(f"🎯 Target criteria:")
    logger.info(f"    • Nationality: Sudanese/African/International students")
    logger.info(f"    • Field: Renewable Energy / Sustainable Energy")
    logger.info(f"    • Level: Master, MPhil, PhD (including direct PhD after BSc)")
    logger.info(f"    • Funding: Fully funded (tuition + stipend + expenses)")
    logger.info(f"📬 Notification: Telegram Bot (@RESudaBOT)")
    if args.dry_run:
        logger.info(f"🧪 Mode: Dry-run (no actual notifications)")
    logger.info("=" * 50)

    try:
        # Run job immediately on start
        logger.info("🏃‍♂️ Running initial scholarship check...")
        job(dry_run=args.dry_run)

        # If --once flag is set, exit after first run
        if args.once:
            logger.info("✅ Completed single run as requested")
            return

        # Schedule job to run every N hours
        logger.info(f"⏰ Scheduling recurring checks every {args.interval} hours...")
        schedule.every(args.interval).hours.do(job, dry_run=args.dry_run)

        # Keep the script running
        logger.info("🔄 Entering main loop - bot is now running continuously...")
        logger.info("💡 To stop the bot: Press Ctrl+C or terminate the process")
        logger.info("=" * 50)

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled jobs

    except KeyboardInterrupt:
        logger.info("🛑 Received shutdown signal - stopping gracefully...")
        logger.info("👋 Scholarship Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error in main loop: {e}", exc_info=True)
        logger.info("👋 Scholarship Bot terminated due to error")
    finally:
        logger.info("🏁 Scholarship Bot shutdown complete")

if __name__ == "__main__":
    main()