"""
Filter module for scholarships based on user criteria.
Enhanced with better keyword matching and weighting system.
"""
import re
from typing import List
from models import Scholarship

class ScholarshipFilter:
    """Filters scholarships based on user's specific criteria with scoring system."""

    def __init__(self):
        # Keywords for filtering (case-insensitive)
        self.nationality_keywords = [
            'sudan', 'sudanese', 'african', 'africa', 'developing countries',
            'international', 'all nationalities', 'open to all', 'worldwide',
            'no restriction', 'global', 'from abroad', 'overseas students'
        ]

        self.field_keywords = [
            'renewable energy', 'sustainable energy', 'clean energy',
            'power systems', 'energy engineering', 'energy technology',
            'solar', 'wind', 'hydro', 'hydroelectric', 'geothermal', 'bioenergy',
            'biomass', 'wave power', 'tidal power', 'alternative energy',
            'green energy', 'energy systems', 'energy management', 'energy policy'
        ]

        self.level_keywords = [
            'master', 'msc', 'ma', 'mphil', 'phd', 'ph.d', 'doctoral',
            'doctorate', 'graduate', 'postgraduate', 'research degree'
        ]

        self.funding_keywords = [
            'fully funded', 'full scholarship', 'tuition waiver',
            'stipend', 'living allowance', 'accommodation',
            'monthly allowance', 'no tuition', 'funded',
            'full financial support', 'covered', 'grant', 'fellowship',
            'financial assistance', 'award', 'prize', 'studentship',
            'maintenance allowance', 'living expenses', 'travel grant'
        ]

        # Keywords that might indicate ineligibility (negative filters)
        self.exclude_keywords = [
            'citizens only', 'national only', 'locals only',
            'residents only', 'employed by', 'must be employed',
            'current employees', 'staff only', 'faculty only',
            'single citizenship', 'dual citizenship not accepted'
        ]

        # Boost keywords - if present, increase relevance score
        self.boost_keywords = [
            'sudan', 'sudanese', 'african', 'africa',
            'renewable energy', 'sustainable energy', 'clean energy',
            'fully funded', 'full scholarship', 'phd', 'doctoral',
            'master', 'msc', 'masters'
        ]

    def filter(self, scholarships: List[Scholarship]) -> List[Scholarship]:
        """
        Filter scholarships based on criteria using a scoring system.
        Returns list of scholarships that meet minimum threshold.
        """
        filtered = []
        for scholarship in scholarships:
            score, details = self._calculate_relevance_score(scholarship)
            # Only include if it meets minimum relevance threshold
            if score >= 60:  # Threshold can be adjusted
                scholarship.relevance_score = score
                scholarship.relevance_details = details
                filtered.append(scholarship)

        # Sort by relevance score (highest first)
        filtered.sort(key=lambda x: getattr(x, 'relevance_score', 0), reverse=True)
        return filtered

    def _calculate_relevance_score(self, scholarship: Scholarship) -> tuple:
        """
        Calculate a relevance score for a scholarship based on how well it matches criteria.
        Returns (score, details_dict) where score is 0-100.
        """
        # Combine all text fields for searching
        text_to_search = f"{scholarship.title} {scholarship.description} {scholarship.eligibility} {scholarship.funding} {scholarship.field} {scholarship.level} {scholarship.nationality}".lower()

        score = 0
        details = {
            'nationality_match': False,
            'field_match': False,
            'level_match': False,
            'funding_match': False,
            'boost_matches': [],
            'exclude_matches': [],
            'negative_score': 0
        }

        # Check negative filters first (if any exclude keyword is found, heavily penalize)
        exclude_penalty = 0
        for exclude in self.exclude_keywords:
            if exclude in text_to_search:
                exclude_penalty += 30  # Heavy penalty for exclusionary language
                details['exclude_matches'].append(exclude)

        # If strong exclusionary language, return low score
        if exclude_penalty >= 50:
            details['negative_score'] = exclude_penalty
            return max(0, 50 - exclude_penalty), details

        # Check nationality: must match at least one nationality keyword
        nationality_score = 0
        for keyword in self.nationality_keywords:
            if keyword in text_to_search:
                nationality_score += 25  # Each match adds points
                details['nationality_match'] = True
                details['boost_matches'].append(keyword)
                break  # Just need one match

        # Check field: must match at least one field keyword
        field_score = 0
        for keyword in self.field_keywords:
            if keyword in text_to_search:
                field_score += 25
                details['field_match'] = True
                details['boost_matches'].append(keyword)
                break  # Just need one match

        # Check level: must match at least one level keyword
        level_score = 0
        for keyword in self.level_keywords:
            if keyword in text_to_search:
                level_score += 25
                details['level_match'] = True
                details['boost_matches'].append(keyword)
                break  # Just need one match

        # Check funding: must match at least one funding keyword
        funding_score = 0
        for keyword in self.funding_keywords:
            if keyword in text_to_search:
                funding_score += 25
                details['funding_match'] = True
                details['boost_matches'].append(keyword)
                break  # Just need one match

        # Calculate category score (sum of matched categories, each worth 25)
        category_score = nationality_score + field_score + level_score + funding_score

        # Add boost points for additional matches beyond the basics
        boost_score = 0
        for keyword in self.boost_keywords:
            if keyword in text_to_search and keyword not in details['boost_matches']:
                boost_score += 5  # Small boost for additional relevant keywords
                details['boost_matches'].append(keyword)

        # Calculate final score
        raw_score = category_score + boost_score - exclude_penalty
        final_score = max(0, min(100, raw_score))  # Clamp between 0 and 100

        details['category_score'] = category_score
        details['boost_score'] = boost_score
        details['exclude_penalty'] = exclude_penalty
        details['raw_score'] = raw_score
        details['final_score'] = final_score

        return final_score, details

    def _is_relevant(self, scholarship: Scholarship) -> bool:
        """
        Legacy method for backward compatibility.
        Returns True if scholarship meets minimum relevance threshold.
        """
        score, _ = self._calculate_relevance_score(scholarship)
        return score >= 60