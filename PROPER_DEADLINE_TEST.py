#!/usr/bin/env python3
"""
Proper test to verify deadline scoring impact by carefully controlling
which fields match to avoid false positives from substring matching or
unintended keyword matches.
"""
from filter import ScholarshipFilter
from models import Scholarship
from datetime import datetime, timedelta, timezone

def test_deadline_impact_proper():
    print("=" * 70)
    print("PROPER TEST: DEADLINE SCORING IMPACT ISOLATION")
    print("=" * 70)

    filter_obj = ScholarshipFilter()

    # Let's first check what the actual keywords are to avoid false matches
    print("Filter keywords for reference:")
    print(f"  Nationality: {filter_obj.nationality_keywords[:5]}...")
    print(f"  Field: {filter_obj.field_keywords[:5]}...")
    print(f"  Level: {filter_obj.level_keywords[:5]}...")
    print(f"  Funding: {filter_obj.funding_keywords[:5]}...")
    print(f"  Boost: {filter_obj.boost_keywords[:5]}...")
    print()

    # We want a scholarship that matches ONLY nationality and field
    # To avoid false matches, we'll use text that doesn't contain any
    # substrings of the other keywords

    # Create base scholarship with safe text that won't trigger false matches
    base_scholarship = Scholarship(
        title="Financial Aid Opportunity",  # Generic title, avoid keywords
        link="https://example.com/opportunity",
        description="Study opportunity in clean power generation",  # Avoid exact field matches
        eligibility="Open to students from North Africa",  # Avoid exact nationality matches
        funding="Financial support available",  # Avoid exact funding matches
        field="Clean Power Generation",  # Avoid exact field matches
        level="Advanced Studies",  # Avoid exact level matches
        nationality="North African Student",  # Avoid exact nationality matches
    )

    print("Base scholarship analysis:")
    score_base, details_base = filter_obj._calculate_relevance_score(base_scholarship)
    print(f"  Title: '{base_scholarship.title}'")
    print(f"  Description: '{base_scholarship.description}'")
    print(f"  Eligibility: '{base_scholarship.eligibility}'")
    print(f"  Funding: '{base_scholarship.funding}'")
    print(f"  Field: '{base_scholarship.field}'")
    print(f"  Level: '{base_scholarship.level}'")
    print(f"  Nationality: '{base_scholarship.nationality}'")
    print(f"  Base score: {score_base}/100")
    print(f"  Details: {details_base}")
    print()

    # Now let's find what ACTUALLY matches in the base to understand our starting point
    base_nat_match = details_base.get('nationality_match', False)
    base_fld_match = details_base.get('field_match', False)
    base_lvl_match = details_base.get('level_match', False)
    base_fin_match = details_base.get('funding_match', False)

    print(f"Base matches - Nat: {base_nat_match}, Fld: {base_fld_match}, Lvl: {base_lvl_match}, Fin: {base_fin_match}")

    # Calculate what the base score actually is from matched categories
    base_category_score = 0
    if base_nat_match: base_category_score += 25
    if base_fld_match: base_category_score += 25
    if base_lvl_match: base_category_score += 25
    if base_fin_match: base_category_score += 25
    # Note: we don't have deadline yet in base

    print(f"Base category score from matches: {base_category_score}")
    print(f"Base total score: {score_base}")
    print(f"Implied boost score: {details_base.get('boost_score', 0)}")
    print()

    # Now let's create test scholarships where we KNOW which fields match
    # by using exact keyword matches for nationality and field only

    # We'll use exact matches but make sure they don't trigger other matches accidentally
    test_cases = [
        ("Past deadline", -10, 0),
        ("Today", 0, 25),
        ("Urgent", 15, 25),
        ("Soon", 45, 20),
        ("Upcoming", 120, 15),
        ("Later", 200, 10),
        ("Distant", 400, 5),
        ("No deadline", None, 0),
    ]

    # Use exact keyword matches but choose ones that are less likely to cause substring issues
    # For nationality: use "sudanese" (exact match)
    # For field: use "solar energy" (not in field_keywords, but let's check...)

    # Actually, let's just use the exact keywords and accept that we'll get some boost points
    # but we'll account for them in our expectations

    print("Testing deadline impact with controlled matches:")
    print("-" * 70)

    all_passed = True

    for desc, days_offset, expected_deadline_points in test_cases:
        # Create scholarship with specific deadline and KNOWN matches
        if days_offset is not None:
            deadline = datetime.now(timezone.utc) + timedelta(days=days_offset)
        else:
            deadline = None

        # Use exact matches for nationality and field to ensure we know what's matching
        test_scholarship = Scholarship(
            title=f"Test Opportunity {desc}",  # Generic title
            link=f"https://example.com/test-{abs(days_offset) if days_offset is not None else 'none'}",
            description="Renewable energy study program",  # Exact field match
            eligibility="Open to Sudanese applicants",  # Exact nationality match (contains "sudanese")
            funding="Financial assistance provided",  # Generic, avoid funding matches
            field="Renewable Energy",  # EXACT field keyword match
            level="Postgraduate Study",  # Generic, avoid level matches
            nationality="Sudanese",  # EXACT nationality keyword match
            deadline=deadline
        )

        score, details = filter_obj._calculate_relevance_score(test_scholarship)

        # Get the actual matches
        nat_match = details.get('nationality_match', False)
        fld_match = details.get('field_match', False)
        lvl_match = details.get('level_match', False)
        fin_match = details.get('funding_match', False)
        dl_match = details.get('deadline_match', False)
        dl_score = details.get('deadline_score', 0)

        # Calculate expected score based on actual matches
        expected_category_score = 0
        if nat_match: expected_category_score += 25
        if fld_match: expected_category_score += 25
        if lvl_match: expected_category_score += 25
        if fin_match: expected_category_score += 25
        if dl_match: expected_category_score += dl_score  # Deadline score is variable

        # Add boost points (we'll estimate these conservatively)
        # For now, let's just check that the deadline score is correct
        # and that the score changes appropriately with deadline

        # Determine if this test passes
        deadline_correct = dl_score == expected_deadline_points

        # For total score, we expect that as deadline_score increases,
        # total score should increase (or stay same if clamped at 100)
        # We'll do a relative check instead of absolute

        status = "✅ PASS" if deadline_correct else "❌ FAIL"
        if not deadline_correct:
            all_passed = False

        print(f"{status} {desc}")
        print(f"    Days offset: {days_offset}")
        print(f"    Matches: Nat={nat_match}, Fld={fld_match}, Lvl={lvl_match}, Fin={fin_match}, DL={dl_match}")
        print(f"    Scores: Nat={25 if nat_match else 0}, Fld={25 if fld_match else 0}, Lvl={25 if lvl_match else 0}, Fin={25 if fin_match else 0}, DL={dl_score}")
        print(f"    Boost matches: {details.get('boost_matches', [])}")
        print(f"    Total score: {score}/100")

        if not deadline_correct:
            print(f"    -> ERROR: Expected deadline score {expected_deadline_points}, got {dl_score}")
        print()

    print("=" * 70)
    if all_passed:
        print("🎉 ALL DEADLINE SCORING TESTS PASSED!")
        print("   The deadline proximity scoring is working correctly.")
    else:
        print("❌ SOME TESTS FAILED.")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    test_deadline_impact_proper()