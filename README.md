# Scholarship Bot

<<<<<<< HEAD
A Python application that continuously fetches scholarship opportunities from various websites and sends real-time alerts via Telegram for fully funded Master's or PhD programs.
=======
## Version 1.0.1

A Python application that continuously fetches scholarship opportunities from various websites and sends real-time alerts via Telegram for fully funded Master's or PhD programs in Renewable Energy for Sudanese students with a Bachelor's in Mechanical Engineering.
>>>>>>> addebeb (Update to V1.0.1: Added Deadline Proximity Scoring system)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Changelog](#changelog)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Components](#components)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

The Scholarship Bot is an automated system designed to help Sudanese students with Mechanical Engineering backgrounds find fully funded Master's and PhD scholarships in Renewable Energy and Sustainable Energy fields. The bot continuously monitors scholarship websites, filters opportunities based on specific criteria, eliminates duplicates, and sends real-time notifications via Telegram.

## Features

<<<<<<< HEAD
- Scrapes multiple scholarship websites for new opportunities
- Filters results based on specific criteria:
  - Open to Sudanese/African/international students
  - Level: Master's, MPhil, PhD (including direct PhD after BSc)
  - Funding: Fully funded (tuition + stipend + other expenses)
- Eliminates duplicate notifications using persistent storage
- Sends formatted alerts via Telegram bot
- Runs on a schedule (every 6 hours by default)
- Built with free tiers in mind for cost-effective deployment
=======
### Core Functionality
- 🔍 **Automated Scraping**: Continuously monitors multiple scholarship websites for new opportunities
- 🎯 **Intelligent Filtering**: Advanced 0-100 scoring system that evaluates scholarships based on:
  - Nationality eligibility (Sudanese, African, international students)
  - Academic field (Renewable Energy, Sustainable Energy, etc.)
  - Education level (Master's, MPhil, PhD, Doctoral)
  - Funding status (Fully funded, stipend, living allowance, etc.)
  - Application deadline proximity (urgent, soon, upcoming, later, distant)
- 🚫 **Duplicate Prevention**: SQLite-based storage ensures each scholarship is notified only once
- 📱 **Telegram Integration**: Sends beautifully formatted notifications via Telegram bot
- ⏰ **Scheduled Execution**: Runs automatically every 6 hours (configurable)
- 💰 **Cost Effective**: Designed to run on free-tier hosting services
>>>>>>> addebeb (Update to V1.0.1: Added Deadline Proximity Scoring system)

### Scoring System (v1.0.1)
The enhanced filtering system uses a 0-100 point scale:
- **Nationality Match**: 25 points
- **Field Match**: 25 points  
- **Level Match**: 25 points
- **Funding Match**: 25 points
- **Deadline Proximity**: 25 points

**Deadline Scoring Breakdown:**
- 🔴 **0-30 days**: 25 points (Urgent - Apply Soon!)
- 🟠 **31-90 days**: 20 points (Soon)
- 🟡 **91-180 days**: 15 points (Upcoming)
- 🟢 **181-365 days**: 10 points (Later)
- ⚪ **365+ days**: 5 points (Distant)
- ⚫ **Past deadline**: 0 points

<<<<<<< HEAD
=======
---

## Changelog

### Version 1.0.1 (Current)
- **Added Deadline Proximity Scoring** - Enhanced filtering system prioritizes scholarships by application deadline
- **Enhanced Scoring Algorithm** - Updated from 4-category to 5-category scoring system (100 points max)
- **Improved Readme Documentation** - Professional formatting with clear sections and changelog
- **Maintained Backward Compatibility** - All existing functionality preserved
- **Fixed Boundary Conditions** - Robust deadline calculation using date-only comparison
- **Enhanced Test Suite** - Added comprehensive validation tests for deadline scoring
>>>>>>> addebeb (Update to V1.0.1: Added Deadline Proximity Scoring system)

### Version 1.0.0 (Initial Release)
- **Core Scholarship Bot System** - Basic scraping, filtering, and notification functionality
- **Telegram Integration** - Working bot connection with @RESudaBOT
- **Website Scraping** - Scrapers for Scholarships4Dev and GlobalStudyRoad
- **Filtering System** - Basic keyword matching for nationality, field, level, funding
- **Duplicate Prevention** - SQLite-based storage system
- **Scheduled Execution** - GitHub Actions workflow (every 6 hours)
- **Documentation** - Initial README and setup guides

<<<<<<< HEAD
1. **Update scrapers with more realistic browser headers**
2. **Add session cookie handling**
3. **Implement retry mechanisms with delays**
4. **Use alternative URLs or mobile versions of the sites**

### Option 2: Add More Scholarship Sources
Consider adding scrapers for sites that are more scraper-friendly:
- University websites directly (often have clearer structures)
- Government scholarship portals
- International organization websites (UN, World Bank, etc.)
- Regional scholarship databases

### Option 3: Manual Seeding + Automation
1. Manually collect a list of known scholarship sources
2. Use the bot to monitor those specific sources
3. Gradually add more sources as you verify they work

### Option 4: Use Alternative Data Sources
Some sites offer:
- RSS feeds
- JSON APIs
- Newsletter subscriptions you could monitor
- Affiliate programs or data partnerships


The scholarship bot includes:

### Core Components:
- `scholarship_bot.py` - Main orchestrator
- `models.py` - Scholarship data structure
- `filter.py` - Criteria-based filtering (Sudanese eligibility, Renewable Energy, Master/PhD+, Fully funded)
- `storage.py` - SQLite-based duplicate prevention
- `telegram_notifier.py` - Telegram Bot API communication (✅ TESTED AND WORKING)
- `scraper_manager.py` - Coordinates multiple scrapers
- `scrapers/base_scraper.py` - Base scraper class
- `scrapers/scholarships4dev.py` - Scraper for Scholarships4Dev
- `scrapers/globalstudyroad.py` - Scraper for GlobalStudyRoad

### Configuration:
- `.env` - Your Telegram credentials (BOT_TOKEN and CHAT_ID)
- `requirements.txt` - All required Python packages
- `README.md` - This documentation

## 🧪 Testing Results

All internal systems tested successfully:
- ✅ Telegram bot connection and messaging (you received a test message)
- ✅ Scholarship data model creation
- ✅ Filtering logic (correctly identifies relevant scholarships)
- ✅ Storage/deduplication system
- ✅ End-to-end workflow test

## 🔧 To Make the Bot Work with Current Sites

If you want to troubleshoot the website access:

1. **Check what the sites actually return** by visiting them in your browser
2. **Update the scrapers** to match the actual HTML structure
3. **Add more realistic headers** (referer, accept-language, etc.)
4. **Implement session handling** for sites that require cookies
5. **Add rate limiting** to be respectful to the sites

### Example improvements you could make to scrapers:
```python
# In base_scraper.py, enhance the session:
self.session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
})
=======
---

## System Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌──────────────────────┐
│   Scheduler     │    │  Scraper     │    │  Scholarship Sites     │
│  (GitHub Actions)│───▶│ Manager      │◀───│ (scholarships4dev.com, │
└─────────────────┘    │              │    │  globalstudyroad.com,  │
                       │              │    │  and others)           │
           ▲           └──────────────┘    └──────────────────────┘
           │                    │
           │                    ▼
           │              ┌─────────────────┐
           │              │   Filtering     │
           │              │   System        │
           │              │  (0-100 scoring)│
           │              └─────────────────┘
           │                    │
           │                    ▼
           │              ┌─────────────────┐
           │              │  Storage/Dedup  │
           │              │  (SQLite)       │
           │              └─────────────────┘
           │                    │
           ▼                    ▼
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│  Notification   │    │  Logging &      │    │  Output/Results      │
│  (Telegram Bot) │    │  Error Handling │    │  (Telegram Alerts)   │
└─────────────────┘    └──────────────────┘    └────────────────────┘
>>>>>>> addebeb (Update to V1.0.1: Added Deadline Proximity Scoring system)
```

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Git (for version control)
- Telegram Bot Token and Chat ID (from @BotFather)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd scholarship-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```bash
   BOT_TOKEN=your_telegram_bot_token_here
   CHAT_ID=your_telegram_chat_id_here
   ```

4. **Initialize the Database**
   The storage system will automatically create the SQLite database on first run.

5. **Run the Bot**
   ```bash
   python scholarship_bot.py
   ```

### Docker Deployment (Alternative)
```bash
# Build the image
docker build -t scholarship-bot .

# Run the container
docker run -d \
  --name scholarship-bot \
  -e BOT_TOKEN=$BOT_TOKEN \
  -e CHAT_ID=$CHAT_ID \
  scholarship-bot
```

---

## Configuration

### Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ` |
| `CHAT_ID` | Your Telegram Chat ID | `987654321` |

### Optional Configuration
Edit `scholarship_bot.py` to adjust:
- `DEFAULT_INTERVAL_HOURS`: Change how often the bot runs (default: 6)
- `SCHOLARSHIP_SITES`: Modify which scrapers are active

### Logging Configuration
Logs are written to `scholarship_bot.log` with rotation handled by the logging configuration.

---

## Usage

### Running Modes

#### 1. Continuous Operation (Default)
```bash
python scholarship_bot.py
```
The bot runs once immediately, then schedules itself to run every 6 hours.

#### 2. Single Run (For Testing/Cron)
```bash
python scholarship_bot.py --once
```
Runs the bot once and exits - perfect for cron jobs or testing.

#### 3. Dry Run Mode (No Telegram Messages)
```bash
python scholarship_bot.py --dry-run
```
Simulates execution without sending actual Telegram notifications.

#### 4. Verbose Mode (Debug Logging)
```bash
python scholarship_bot.py --verbose
```
Enables debug-level logging for troubleshooting.

#### 5. Custom Interval
```bash
python scholarship_bot.py --interval 12
```
Runs every 12 hours instead of the default 6.

### Combined Examples
```bash
# Run once with verbose logging for testing
python scholarship_bot.py --once --verbose

# Dry run every 12 hours
python scholarship_bot.py --dry-run --interval 12
```

---

## Components

### Core Modules
- `scholarship_bot.py` - Main orchestrator and scheduler
- `models.py` - Scholarship data class with serialization methods
- `filter.py` - Enhanced 0-100 scoring filter system with deadline proximity
- `storage.py` - SQLite-based duplicate prevention storage
- `telegram_notifier.py` - Telegram Bot API communication
- `scraper_manager.py` - Coordinates multiple website scrapers
- `scrapers/base_scraper.py` - Base scraper class with common functionality
- `scrapers/scholarships4dev.py` - Scraper for Scholarships4Dev website
- `scrapers/globalstudyroad.py` - Scraper for GlobalStudyRoad website

### Configuration Files
- `.env` - Environment variables (Telegram credentials)
- `requirements.txt` - Python package dependencies
- `.gitignore` - Files to exclude from version control
- `scholarship_bot.log` - Application log file (auto-generated)

### Automation
- `.github/workflows/scholarship-bot.yml` - GitHub Actions workflow (runs every 6 hours)

---

## Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Suites
```bash
# Test deadline scoring logic
python test_deadline_thorough.py

# Test filtering system
python test_bot.py

# Test end-to-end functionality
python test_end_to_end.py

# Quick verification
python quick_test.py
```

### Test Coverage
- ✅ Unit testing for all components
- ✅ Integration testing of full workflow
- ✅ Boundary condition testing for deadline scoring
- ✅ Regression testing to ensure backward compatibility
- ✅ Edge case testing (past deadlines, no deadlines, etc.)

---

## Troubleshooting

### Common Issues

#### 1. Telegram Connection Failures
- **Symptoms**: "Cannot connect to Telegram bot!" errors
- **Solutions**:
  - Verify `BOT_TOKEN` and `CHAT_ID` in `.env` file
  - Check internet connectivity
  - Ensure bot hasn't been deleted or blocked
  - Test bot manually by sending a message to @RESudaBOT

#### 2. Website Access Problems
- **Symptoms**: No scholarships found, scraper errors in logs
- **Solutions**:
  - Update user-agent strings in `base_scraper.py`
  - Add session handling and cookie support
  - Implement retry mechanisms with exponential backoff
  - Consider alternative URLs or mobile site versions
  - Check if website structure has changed (update selectors)

#### 3. Duplicate Notifications
- **Symptoms**: Receiving the same scholarship multiple times
- **Solutions**:
  - Verify SQLite database file exists and is writable
  - Check storage system logs for database errors
  - Ensure bot isn't running multiple instances simultaneously
  - Clear database and restart (will lose history but fix immediate issues)

#### 4. High Memory/CPU Usage
- **Symptoms**: Bot consuming excessive resources
- **Solutions**:
  - Check for infinite loops in scrapers
  - Verify session cleanup in base scraper
  - Ensure proper error handling prevents hanging connections
  - Consider adding rate limiting to be respectful to target sites

#### 5. Scheduled Execution Failures (GitHub Actions)
- **Symptoms**: Workflow failing in GitHub Actions tab
- **Solutions**:
  - Check workflow logs for specific error messages
  - Verify secrets are correctly configured in repo settings
  - Ensure `requirements.txt` is up to date
  - Check that all file paths are correct in the workflow

### Debugging Tips
1. **Enable Verbose Mode**: Use `--verbose` flag for detailed logging
2. **Check Logs**: Examine `scholarship_bot.log` for error traces
3. **Test Components Individually**: Run specific test scripts to isolate issues
4. **Check Network Connectivity**: Verify bot can reach target websites
5. **Validate Telegram Credentials**: Test bot manually outside the application

---

## Maintenance

### Regular Tasks
- **Weekly**: Check bot logs for errors or warnings
- **Monthly**: Review and update scraper selectors if websites change
- **Quarterly**: Update keyword lists based on evolving scholarship trends
- **Biannual**: Evaluate and add/remove scholarship sources
- **Annual**: Review overall bot effectiveness and consider major enhancements

### Log Management
The bot uses Python's built-in logging with:
- Console output (stdout/stderr)
- File output to `scholarship_bot.log`
- Info level logging for standard operations
- Debug level available with `--verbose` flag

For long-term deployments, consider implementing external log rotation.

### Database Maintenance
The SQLite storage system:
- Automatically creates `scholarships_seen.db` on first run
- Stores SHA256 hashes of scholarship.title + scholarship.link
- Requires minimal maintenance
- Can be inspected with SQLite tools if needed
- To reset history: delete `scholarships_seen.db` (will lose duplicate prevention)

### Updating the Bot
```bash
# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Restart the bot
# (If using GitHub Actions, next scheduled run will use updated code)
```

---

## Future Enhancements

Based on ongoing research and user feedback, planned enhancements include:

### Near Term (1.x Releases)
- **Geographical Weighting** - Prefer scholarships from African/European institutions
- **Language Preferences** - Filter by language of instruction (English/Arabic)
- **Application Difficulty Estimation** - Score based on requirements complexity
- **Enhanced Notification Formatting** - Better visual hierarchy in Telegram messages
- **Quiet Hours** - Option to disable notifications during sleeping hours

### Mid Term (2.x Releases)
- **Machine Learning Refinement** - Improve relevance scoring using ML models
- **RSS/JSON Feed Integration** - Add structured data sources where available
- **Social Media Monitoring** - Monitor Telegram groups, WhatsApp lists for opportunities
- **Multi-Channel Notifications** - Support for WhatsApp, Email, SMS in addition to Telegram
- **Personalized Recommendations** - Learn from user interactions to improve future suggestions

### Long Term (3.x Releases)
- **Application Assistance** - Deadline tracking, document checklist management
- **Community Features** - User scholarship success stories, tips exchange
- **Offline Capabilities** - Periodic digests for low-connectivity users
- **Change Detection Services** - Advanced monitoring for scholarship page updates
- **Educational Partnerships** - Direct data sharing with universities and organizations

### Alternative Approaches
If website scraping becomes prohibitively difficult:
- **Official Scholarship APIs** - Where available from institutions or aggregators
- **Email Newsletter Parsing** - Monitor scholarship-focused mailing lists
- **University API Integration** - Direct integration with university scholarship systems
- **Change Detection Services** - Services like Visualping or Distill.io for change alerts
- **Partnership Models** - Direct data feeds from educational consulting organizations

---

## 📱 What You'll Receive

When the bot finds a matching scholarship, you'll get a Telegram message like this:

```
*Fully Funded PhD in Renewable Energy Engineering*

🔗 [Link](https://example.com/scholarship)

📚 *Field:* Renewable Energy Engineering
🎓 *Level:* PhD
🌍 *Eligible Nationalities:* Sudanese, African students
💰 *Funding:* Fully funded tuition + monthly stipend + accommodation
⏰ *Deadline:* 2026-12-31
📅 *Days Until Deadline:* 45 (Soon)

📝 *Description:*
This scholarship supports research in solar and wind energy technologies...
Focus areas include photovoltaic systems, wind turbine design, and energy storage solutions.

🏭 *Source:* Scholarships4Dev
📊 *Relevance Score:* 85/100
    🎯 Nationality: 25/25
    🎯 Field: 25/25
    🎯 Level: 25/25
    🎯 Funding: 10/25 (Partial funding - not fully funded)
    🎯 Deadline: 25/25 (Soon - 45 days)
```

<<<<<<< HEAD
## 🛠️ Maintenance Tips

- The bot automatically avoids sending duplicate notifications
- Check `scholarship_bot.log` for detailed error messages
- Consider setting up log rotation for long-term deployments
- Update scrapers periodically as websites change their structure

## 💡 Alternative Approach

If website scraping proves consistently difficult, consider:
1. Using official scholarship APIs where available
2. Monitoring scholarship newsletters via email parsing
3. Using university RSS feeds for new postings
4. Partnering with educational offices that share opportunity lists
5. Using change detection services on scholarship pages



=======
---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For issues, questions, or contributions:
1. Check the [Issues](<your-repo-url>/issues) tab on GitHub
2. Review the documentation and troubleshooting guide above
3. Ensure your Telegram bot (@RESudaBOT) is functioning correctly
4. Verify website accessibility before reporting scraping issues

---

## 🎉 Ready to Use

Your Scholarship Bot is now enhanced with **Deadline Proximity Scoring (v1.0.1)** to help you never miss an urgent scholarship opportunity!

The bot continuously works to find and notify you about:
- Fully funded Master's and PhD scholarships
- In Renewable Energy and Sustainable Energy fields
- Open to Sudanese and African students
- With timely application deadlines highlighted

**Stay persistent, stay informed, and may your scholarship hunt be successful!** 🎓🔍💰

---
*Last updated: 2026-06-06*
*Version: 1.0.1*
>>>>>>> addebeb (Update to V1.0.1: Added Deadline Proximity Scoring system)
