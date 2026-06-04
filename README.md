# Scholarship Bot

A Python application that continuously fetches scholarship opportunities from various websites and sends real-time alerts via Telegram for fully funded Master's or PhD programs.

## Features

- Scrapes multiple scholarship websites for new opportunities
- Filters results based on specific criteria:
  - Open to Sudanese/African/international students
  - Level: Master's, MPhil, PhD (including direct PhD after BSc)
  - Funding: Fully funded (tuition + stipend + other expenses)
- Eliminates duplicate notifications using persistent storage
- Sends formatted alerts via Telegram bot
- Runs on a schedule (every 6 hours by default)
- Built with free tiers in mind for cost-effective deployment

## Status: Bot System Built Successfully

✅ **Telegram Bot Configured**: Your bot is set up and tested - you received a test message
✅ **All Components Built**: Scrapers, filtering, storage, notification systems are complete
✅ **Core Logic Verified**: Filtering, deduplication, and notification systems work correctly
⚠️ **Website Access Issue**: Target scholarship sites are currently blocking/requesting different access methods


## 🚀 Next Steps to Make the Bot Operational

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
```

## 📋 When Sites Are Working Again

Once you can access the scholarship sites, the bot will:
1. Run immediately upon startup
2. Check all configured scholarship sites
3. Filter results based on your criteria (Sudanese students, Renewable Energy, Master/PhD+, Fully funded)
4. Send new opportunities via Telegram with formatted messages
5. Repeat every 6 hours (configurable)

You'll receive Telegram messages like:
```
*Fully Funded PhD in Renewable Energy Engineering*

🔗 [Link](https://example.com/scholarship)

📚 *Field:* Renewable Energy Engineering
🎓 *Level:* PhD
🌍 *Eligible Nationalities:* Sudanese, African students
💰 *Funding:* Fully funded tuition + monthly stipend + accommodation
⏰ *Deadline:* 2026-12-31

📝 *Description:*
This scholarship supports research in solar and wind energy technologies...

🏭 *Source:* Scholarships4Dev
```

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



