# Changelog

All notable changes to the Scholarship Bot will be documented in this file.

## [Unreleased]
### Added
- 
### Changed
- 
### Fixed
- 

## [1.0.1] - 2026-06-06
### Added
- Deadline Proximity Scoring system (0-25 points based on application deadline urgency)
- Enhanced scoring algorithm from 4-category to 5-category system (100 points max)
- Comprehensive test suite for deadline scoring boundary conditions
- Professional README documentation with clear sections and table of contents
- Detailed notification formatting including days until deadline and score breakdown

### Changed
- Updated filter.py to implement the new 0-100 scoring system
- Enhanced README.md with improved structure, features documentation, and usage examples
- Improved deadline calculation using robust date-only comparison
- Enhanced test coverage including unit, integration, and boundary condition tests

### Fixed
- Boundary conditions in deadline scoring (0, 30, 31, 90, 91, 180, 181, 365, 366 days)
- Maintained full backward compatibility with existing functionality
- Fixed any edge cases in deadline processing

## [1.0.0] - 2026-06-03
### Added
- Core Scholarship Bot System with basic scraping, filtering, and notification functionality
- Telegram Bot Integration with @RESudaBOT (tested and working)
- Website Scrapers for Scholarships4Dev and GlobalStudyRoad
- Basic Filtering System for nationality, field, level, and funding criteria
- SQLite-based Duplicate Prevention Storage System
- GitHub Actions Workflow for scheduled execution (every 6 hours)
- Initial README and setup guides
- Requirements.txt for dependency management
- Core modules: scholarship_bot.py, models.py, filter.py, storage.py, telegram_notifier.py, scraper_manager.py
- Base scraper class and specific scrapers for target websites
- .env file template for configuration
- .gitignore file
