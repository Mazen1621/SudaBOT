# Scholarship Bot

A Python application that continuously fetches scholarship opportunities from various websites and sends real-time alerts via Telegram for fully funded Master's or PhD programs in Renewable Energy.

## Features

- **Automated Scraping**: Monitors multiple scholarship websites for new opportunities
- **Intelligent Filtering**: 0-100 scoring system evaluating nationality, field, level, funding, and deadline proximity
- **Duplicate Prevention**: SQLite-based storage ensures each scholarship is notified only once
- **Telegram Integration**: Sends formatted notifications via Telegram bot
- **Scheduled Execution**: Runs automatically every 6 hours (configurable)
- **Cost Effective**: Designed to run on free-tier hosting services

## Scoring System

The enhanced filtering system uses a 0-100 point scale:
- **Nationality Match**: 25 points
- **Field Match**: 25 points
- **Level Match**: 25 points
- **Funding Match**: 25 points
- **Deadline Proximity**: 25 points

### Deadline Scoring Breakdown
- **0-30 days**: 25 points (Urgent - Apply Soon!)
- **31-90 days**: 20 points (Soon)
- **91-180 days**: 15 points (Upcoming)
- **181-365 days**: 10 points (Later)
- **365+ days**: 5 points (Distant)
- **Past deadline**: 0 points

## Installation

### Prerequisites
- Python 3.7 or higher
- Git (for version control)
- Telegram Bot Token and Chat ID (from @BotFather)

### Setup
1. Clone the repository
   ```bash
   git clone <repository-url>
   cd scholarship-bot
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables
   Create a `.env` file:
   ```bash
   BOT_TOKEN=your_telegram_bot_token_here
   CHAT_ID=your_telegram_chat_id_here
   ```

4. Run the bot
   ```bash
   python scholarship_bot.py
   ```

### Docker Deployment (Optional)
```bash
docker build -t scholarship-bot .
docker run -d \
  --name scholarship-bot \
  -e BOT_TOKEN=$BOT_TOKEN \
  -e CHAT_ID=$CHAT_ID \
  scholarship-bot
```

## Usage

### Running Modes
- **Continuous Operation** (default): `python scholarship_bot.py`
- **Single Run**: `python scholarship_bot.py --once`
- **Dry Run**: `python scholarship_bot.py --dry-run`
- **Verbose**: `python scholarship_bot.py --verbose`
- **Custom Interval**: `python scholarship_bot.py --interval 12`

## Components

- `scholarship_bot.py` - Main orchestrator
- `models.py` - Scholarship data class
- `filter.py` - Enhanced 0-100 scoring filter system
- `storage.py` - SQLite-based duplicate prevention
- `telegram_notifier.py` - Telegram Bot API communication
- `scraper_manager.py` - Coordinates multiple scrapers
- Scrapers for Scholarships4Dev and GlobalStudyRoad

## License

MIT License
