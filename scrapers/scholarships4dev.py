"""
Scraper for Scholarships4Dev website.
Enhanced with better parsing logic for the current site structure.
"""
import re
import datetime
from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from models import Scholarship
from .base_scraper import BaseScraper
import logging
import time

logger = logging.getLogger(__name__)

class Scholarships4DevScraper(BaseScraper):
    """Enhanced scraper for Scholarships4Dev with better parsing."""

    def __init__(self):
        super().__init__(delay_range=(2, 4), max_retries=3)
        self.base_url = "https://www.scholars4dev.com"
        # Focus on pages that are likely to contain current scholarship listings
        self.start_urls = [
            "https://www.scholars4dev.com/",  # Main page often has featured scholarships
            "https://www.scholars4dev.com/scholarships/",  # Scholarships archive if it exists
            "https://www.scholars4dev.com/category/scholarships/",  # Category page
            "https://www.scholars4dev.com/scholarships-by-level/",  # Level-based pages
            "https://www.scholars4dev.com/scholarships-by-field/",   # Field-based pages
            "https://www.scholars4dev.com/scholarships-by-country/", # Country-based pages
        ]

    def scrape(self) -> List[Scholarship]:
        """Scrape scholarships from Scholarships4Dev with enhanced parsing."""
        scholarships = []

        for start_url in self.start_urls:
            try:
                logger.info(f"Scraping URL: {start_url}")
                soup = self.fetch_page(start_url)
                if soup is None:
                    logger.warning(f"Failed to fetch {start_url} after all retries")
                    continue

                page_scholarships = self._extract_scholarships_from_page(soup, start_url)
                logger.info(f"Extracted {len(page_scholarships)} scholarships from {start_url}")
                scholarships.extend(page_scholarships)

                # Be respectful between different pages
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error scraping {start_url}: {e}", exc_info=True)

        logger.info(f"Scholarships4Dev scraper found {len(scholarships)} total scholarships")
        return scholarships

    def _extract_scholarships_from_page(self, soup: BeautifulSoup, page_url: str) -> List[Scholarship]:
        """Extract scholarship listings from a page using multiple strategies."""
        scholarships = []

        # Strategy 1: Look for article/post elements (common in WordPress sites)
        articles = soup.find_all('article')
        for article in articles:
            scholarship = self._extract_scholarship_from_article(article, page_url)
            if scholarship:
                scholarships.append(scholarship)

        # Strategy 2: Look for divs with class containing post or entry
        if not scholarships:  # Only try this if strategy 1 yielded nothing
            post_divs = soup.find_all('div', class_=lambda c: c and ('post' in c.lower() or 'entry' in c.lower()))
            for div in post_divs:
                scholarship = self._extract_scholarship_from_div(div, page_url)
                if scholarship:
                    scholarships.append(scholarship)

        # Strategy 3: Look for list items that might contain scholarships
        if not scholarships:
            list_items = soup.find_all('li')
            for li in list_items:
                # Only process if it looks like it contains substantial scholarship info
                text = li.get_text(strip=True)
                if len(text) > 30 and any(keyword in text.lower() for keyword in
                                        ['scholarship', 'funded', 'grant', 'fellowship',
                                         'master', 'phd', 'deadline', 'apply']):
                    scholarship = self._extract_scholarship_from_text_block(text, page_url, li)
                    if scholarship:
                        scholarships.append(scholarship)

        # Deduplicate by title and link within this page
        unique_scholarships = []
        seen = set()
        for schol in scholarships:
            key = (schol.title, schol.link)
            if key not in seen:
                seen.add(key)
                unique_scholarships.append(schol)

        return unique_scholarships

    def _extract_scholarship_from_article(self, article, page_url: str) -> Scholarship:
        """Extract scholarship details from an article element."""
        # Try to find title and link
        title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
        if not title_elem:
            # Sometimes title is in a link
            title_elem = article.find('a')

        title = self.extract_text_safely(title_elem)
        if not title or len(title) < 5:
            return None

        # Find link - either the title element itself is a link or find a link nearby
        link = None
        if title_elem.name == 'a' and title_elem.get('href'):
            link = urljoin(self.base_url, title_elem.get('href'))
        else:
            link_elem = article.find('a', href=True)
            if link_elem:
                link = urljoin(self.base_url, link_elem.get('href'))

        if not link:
            return None

        # Get the text content for parsing details
        full_text = self.extract_text_safely(article)

        # Extract other details
        description = self._extract_description(full_text, title)
        eligibility = self._extract_eligibility(full_text)
        funding = self._extract_funding(full_text)
        field = self._extract_field(full_text)
        level = self._extract_level(full_text)
        nationality = self._extract_nationality(full_text)
        deadline = self._extract_date_from_text(full_text)

        return Scholarship(
            title=title,
            link=link,
            description=description,
            eligibility=eligibility,
            funding=funding,
            field=field,
            level=level,
            nationality=nationality,
            deadline=deadline,
            source="Scholarships4Dev"
        )

    def _extract_scholarship_from_div(self, div, page_url: str) -> Scholarship:
        """Extract scholarship details from a div element."""
        # Similar to article extraction but for div elements
        title_elem = div.find(['h1', 'h2', 'h3', 'h4'])
        if not title_elem:
            title_elem = div.find('a')

        title = self.extract_text_safely(title_elem)
        if not title or len(title) < 5:
            return None

        # Find link
        link = None
        if title_elem.name == 'a' and title_elem.get('href'):
            link = urljoin(self.base_url, title_elem.get('href'))
        else:
            link_elem = div.find('a', href=True)
            if link_elem:
                link = urljoin(self.base_url, link_elem.get('href'))

        if not link:
            return None

        # Get text content
        full_text = self.extract_text_safely(div)

        # Extract details
        description = self._extract_description(full_text, title)
        eligibility = self._extract_eligibility(full_text)
        funding = self._extract_funding(full_text)
        field = self._extract_field(full_text)
        level = self._extract_level(full_text)
        nationality = self._extract_nationality(full_text)
        deadline = self._extract_date_from_text(full_text)

        return Scholarship(
            title=title,
            link=link,
            description=description,
            eligibility=eligibility,
            funding=funding,
            field=field,
            level=level,
            nationality=nationality,
            deadline=deadline,
            source="Scholarships4Dev"
        )

    def _extract_scholarship_from_text_block(self, text: str, page_url: str, element) -> Scholarship:
        """Extract scholarship from a text block when we can't find clear title/link structure."""
        # This is a fallback - we'll try to construct a reasonable scholarship object
        # Look for potential title-like patterns (longer phrases that might be titles)
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Find the longest line that looks like a title
        title_candidates = []
        for line in lines:
            if 20 <= len(line) <= 200:  # Reasonable title length
                # Boost score if it contains scholarship-related terms
                score = len(line)
                if any(term in line.lower() for term in ['scholarship', 'grant', 'fellowship', 'award']):
                    score += 20
                if any(term in line.lower() for term in ['master', 'phd', 'ph.d', 'doctoral']):
                    score += 15
                if any(term in line.lower() for term in ['renewable', 'energy', 'sustainable']):
                    score += 15
                title_candidates.append((line, score))

        if not title_candidates:
            return None

        # Sort by score and take the best
        title_candidates.sort(key=lambda x: x[1], reverse=True)
        title = title_candidates[0][0]

        # Try to find a link associated with this text
        link = page_url  # Default to the page URL
        link_elem = element.find('a', href=True)
        if link_elem:
            link = urljoin(self.base_url, link_elem.get('href'))

        # Extract details from the full text
        description = self._extract_description(text, title)[:300]  # Limit description length
        eligibility = self._extract_eligibility(text)
        funding = self._extract_funding(text)
        field = self._extract_field(text)
        level = self._extract_level(text)
        nationality = self._extract_nationality(text)
        deadline = self._extract_date_from_text(text)

        return Scholarship(
            title=title,
            link=link,
            description=description,
            eligibility=eligibility,
            funding=funding,
            field=field,
            level=level,
            nationality=nationality,
            deadline=deadline,
            source="Scholarships4Dev"
        )

    def _extract_description(self, text: str, title: str) -> str:
        """Extract or generate description from text."""
        # Try to find the title in the text and get surrounding context
        idx = text.find(title)
        if idx != -1:
            # Get some text after the title
            start = idx + len(title)
            end = min(start + 400, len(text))
            desc = text[start:end].strip()
            # Clean up the description
            desc = re.sub(r'\s+', ' ', desc)
            return desc

        # Fallback: return first 400 chars of text
        return self.clean_text(text[:400])

    def _extract_eligibility(self, text: str) -> str:
        """Extract eligibility information from text."""
        # Look for common eligibility patterns
        patterns = [
            r'eligible[:\s]+([^.]*?(?:\.|$))',
            r'open\s+to[:\s]+([^.]*?(?:\.|$))',
            r'applicants?[:\s]+([^.]*?(?:\.|$))',
            r'nationality[:\s]+([^.]*?(?:\.|$))',
            r'who\s+can\s+apply[:\s]+([^.]*?(?:\.|$))',
            r'requirements?[:\s]+([^.]*?(?:\.|$))'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                eligibility = self.clean_text(match.group(1))
                if len(eligibility) > 250:
                    eligibility = eligibility[:247] + "..."
                return eligibility
        return "See website for details"

    def _extract_funding(self, text: str) -> str:
        """Extract funding information from text."""
        patterns = [
            r'fund(?:ing|ed)[:\s]+([^.]*?(?:\.|$))',
            r'covers?[:\s]+([^.]*?(?:\.|$))',
            r'stipend[:\s]+([^.]*?(?:\.|$))',
            r'tuition[:\s]+([^.]*?(?:\.|$))',
            r'fully\s+funded',
            r'full\s+scholarship',
            r'financial\s+support[:\s]+([^.]*?(?:\.|$))',
            r'grant[:\s]+([^.]*?(?:\.|$))',
            r'award[:\s]+([^.]*?(?:\.|$))'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if match.group(0).lower().strip() in ['fully funded', 'full scholarship']:
                    return match.group(0).strip()
                funding = self.clean_text(match.group(1))
                if len(funding) > 250:
                    funding = funding[:247] + "..."
                return funding
        return "See website for details"

    def _extract_field(self, text: str) -> str:
        """Extract field of study from text."""
        patterns = [
            r'(?:field|subject|program|study|degree|faculty|major)[:\s]+([^.]*?(?:\.|$))',
            r'in\s+([^.]*(?:energy|power|renewable|sustainable|engineering)[^.]*?(?:\.|$))',
            r'([^.]*(?:energy|power|renewable|sustainable|engineering)[^.]*?(?:\.|$))',
            r'(?:research|study|focus)[:\s]+([^.]*?(?:\.|$))'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                field = self.clean_text(match.group(1))
                if len(field) > 150:
                    field = field[:147] + "..."
                return field
        return "See website for details"

    def _extract_level(self, text: str) -> str:
        """Extract study level from text."""
        level_patterns = [
            r'\b(master|msc|ma|mphil|phd|ph\.d|doctoral?|doctorate|graduate|postgraduate)\b',
        ]
        for pattern in level_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                level = match.group(1).lower()
                # Normalize common variations
                if level in ['ph.d', 'phd']:
                    return 'PhD'
                elif level == 'masters':
                    return 'Master'
                elif level in ['graduate', 'postgraduate']:
                    return level.capitalize()
                else:
                    return level.upper()
        return "See website for details"

    def _extract_nationality(self, text: str) -> str:
        """Extract eligible nationalities from text."""
        patterns = [
            r'(?:open\s+to|eligible\s+for|nationalities?|applicants?\s+from|who\s+can\s+apply)[:\s]+([^.]*?(?:\.|$))',
            r'(sudan|sudanese|african|developing\s+countries?|international|all\s+nationalities?|worldwide)',
            r'(?:no\s+restriction|open\s+to\s+all|global)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                nationality = self.clean_text(match.group(1))
                if len(nationality) > 150:
                    nationality = nationality[:147] + "..."
                return nationality
        return "See website for details"

    def _extract_date_from_text(self, text: str):
        """Extract deadline date from text."""
        # Look for common date patterns
        date_patterns = [
            r'deadline[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'application\s+deadline[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'closes?[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'due\s+date[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'apply\s+by[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',  # Fallback: any date-like pattern
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                # Try to parse common formats
                for fmt in ('%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d.%m.%Y'):
                    try:
                        return datetime.datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
        return None