"""
Manager for coordinating multiple scrapers.
"""
import logging
from typing import List
from models import Scholarship
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class ScraperManager:
    """Manages and runs all scrapers."""

    def __init__(self):
        self.scrapers = self._initialize_scrapers()

    def _initialize_scrapers(self) -> List[BaseScraper]:
        """Initialize all scraper instances."""
        scrapers = []
        # Import scrapers here to avoid circular imports
        try:
            from scrapers.scholarships4dev import Scholarships4DevScraper
            scrapers.append(Scholarships4DevScraper())
            logger.info("Initialized Scholarships4Dev scraper")
        except ImportError as e:
            logger.warning(f"Failed to import Scholarships4Dev scraper: {e}")

        try:
            from scrapers.globalstudyroad import GlobalStudyRoadScraper
            scrapers.append(GlobalStudyRoadScraper())
            logger.info("Initialized GlobalStudyRoad scraper")
        except ImportError as e:
            logger.warning(f"Failed to import GlobalStudyRoad scraper: {e}")

        # Add more scrapers as they are implemented
        # Example:
        # try:
        #     from scrapers.findaphd import FindAPhDScraper
        #     scrapers.append(FindAPhDScraper())
        # except ImportError as e:
        #     logger.warning(f"Failed to import FindAPhD scraper: {e}")

        return scrapers

    def scrape_all(self) -> List[Scholarship]:
        """Run all scrapers and return combined results."""
        all_scholarships = []
        for scraper in self.scrapers:
            try:
                logger.info(f"Running scraper: {scraper.__class__.__name__}")
                scholarships = scraper.scrape()
                logger.info(f"Scraper {scraper.__class__.__name__} found {len(scholarships)} scholarships")
                all_scholarships.extend(scholarships)
            except Exception as e:
                logger.error(f"Error running scraper {scraper.__class__.__name__}: {e}", exc_info=True)
        return all_scholarships