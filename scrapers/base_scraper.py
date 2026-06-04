"""
Base scraper class defining the interface for all scrapers.
Enhanced with better session handling, retry logic, and error management.
"""
import abc
import logging
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from models import Scholarship

logger = logging.getLogger(__name__)

class BaseScraper(abc.ABC):
    """Abstract base class for scrapers with enhanced capabilities."""

    def __init__(self, delay_range=(1, 3), max_retries=3):
        """
        Initialize the scraper with session and retry configuration.

        Args:
            delay_range: Tuple of (min_delay, max_delay) in seconds between requests
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.session = requests.Session()
        # Set a realistic browser user-agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.delay_range = delay_range
        self.max_retries = max_retries

    @abc.abstractmethod
    def scrape(self) -> List[Scholarship]:
        """
        Scrape scholarships from the source.
        Returns a list of Scholarship objects.
        """
        pass

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a webpage with retry logic and return a BeautifulSoup object.
        Returns None if all retries fail.
        """
        for attempt in range(self.max_retries):
            try:
                # Add jittered delay to be respectful
                if attempt > 0:
                    delay = random.uniform(*self.delay_range)
                    logger.info(f"Retry attempt {attempt + 1} for {url} after {delay:.1f}s delay")
                    time.sleep(delay)

                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                # Check if we got redirected to an error page
                if self._is_error_page(response):
                    logger.warning(f"Received error page for {url} (final URL: {response.url})")
                    if attempt < self.max_retries - 1:
                        continue
                    else:
                        return None

                return BeautifulSoup(response.content, 'html.parser')

            except requests.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    continue
                else:
                    logger.error(f"All retry attempts failed for {url}")
                    return None
        return None

    def _is_error_page(self, response: requests.Response) -> bool:
        """
        Check if the response indicates an error page.
        Override this in subclasses if needed for site-specific detection.
        """
        # Check for common error indicators in URL or content
        error_indicators = [
            'error', 'blocked', 'access denied', 'not found',
            'cf.trekpeak.site', 'middle.html'  # Known redirect patterns for scholars4dev
        ]

        # Check URL
        url_lower = response.url.lower()
        if any(indicator in url_lower for indicator in error_indicators):
            return True

        # Check content (first 1000 chars for efficiency)
        if response.text:
            content_start = response.text[:1000].lower()
            if any(indicator in content_start for indicator in ['error', 'access denied', 'not found']):
                return True

        return False

    def parse_date(self, date_str: str):
        """
        Parse a date string into a datetime object.
        Override this method if the site uses a specific date format.
        """
        # This is a placeholder; implement per site if needed
        return None

    def clean_text(self, text: str) -> str:
        """Clean up text by extra whitespace and newlines."""
        if not text:
            return ""
        return ' '.join(text.split())

    def extract_text_safely(self, element, fallback="") -> str:
        """
        Safely extract text from a BeautifulSoup element.
        Returns cleaned text or fallback if element is None or empty.
        """
        if element is None:
            return fallback
        text = element.get_text(strip=True)
        return text if text else fallback