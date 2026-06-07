#!/usr/bin/env python3
"""
Verify that deadline scoring actually impacts the total score
when not all other categories are at maximum.
"""
from filter import ScholarshipFilter
from models import Scholarship
from datetime import datetime, timedelta, timezone

def test_deadline_impact():
    print("=" * 60)
    print("VERIFYING DEADLINE SCORING IMPACT ON TOTAL SCORE")
    print("=" * 60)

    filter_obj = ScholarshipFilter()

    # Base scholarship that matches ONLY nationality and field (50 points base)
    # This way we can see how deadline points affect the total
    base_scholarship = Scholarship(
        title="Base Test",  # Will not match level/funding keywords
        link="https://example.com/base",
        description="Renewable energy opportunity",  # Matches field
        eligibility="Open to Sudanese students",  # Matches nationality
        funding="Partial funding",  # Does NOT match funding keywords
        field="Renewable Energy",  # Matches field
        level="Undergraduate",  # Does NOT match level keywords
        nationality="Sudanese",  # Matches nationality
    )

    # Test different deadlines with this base scholarship
    deadline_tests = [
        ("Past deadline", -10, 0),
        ("Today", 0, 25),
        ("Urgent 15 days", 15, 25),
        ("Urgent 30 days", 30, 25),
        ("Soon 31 days", 31, 20),
        ("Soon 60 days", 60, 20),
        ("Soon 90 days", 90, 20),
        ("Upcoming 91 days", 91, 15),
        ("Upcoming 180 days", 180, 15),
        ("Later 181 days", 181, 10),
        ("Later 200 days", 200, 10),
        ("Later 365 days", 365, 10),
        ("Distant 366 days", 366, 5),
        ("Distant 500 days", 500, 5),
        ("Very distant 1000 days", 1000, 5),
        ("No deadline", None, 0),
    ]

    print(f"Base scholarship (nationality + field only):")
    print(f"  Expected base score: 50 points (25 each for nationality + field)")
    print(f"  Level match: {'MA' in base_scholarship.level or 'MSC' in base_scholarship.level or 'PHD' in base_scholarship.level or 'DOCTORAL' in base_scholarship.level or 'GRADUATE' in base_scholarship.level or 'POSTGRADUATE' in base_scholarship.level or 'RESEARCH DEGREE' in base_scholarship.level}")
    print(f"  Funding match: {'FULLY FUNDED' in base_scholarship.funding or 'FULL SCHOLARSHIP' in base_scholarship.funding or 'TUITION WAIVER' in base_scholarship.funding or 'STIPEND' in base_scholarship.funding or 'LIVING ALLOWANCE' in base_scholarship.funding or 'ACCOMMODATION' in base_scholarship.funding or 'MONTHLY ALLOWANCE' in base_scholarship.funding or 'NO TUITION' in base_scholarship.funding or 'FUNDED' in base_scholarship.funding or 'FULL FINANCIAL SUPPORT' in base_scholarship.funding or 'COVERED' in base_scholarship.funding or 'GRANT' in base_scholarship.funding or 'FELLOWSHIP' in base_scholarship.funding or 'FINANCIAL ASSISTANCE' in base_scholarship.funding or 'AWARD' in base_scholarship.funding or 'PRIZE' in base_scholarship.funding or 'STUDENTSHIP' in base_scholarship.funding or 'MAINTENANCE ALLOWANCE' in base_scholarship.funding or 'LIVING EXPENSES' in base_scholarship.funding or 'TRAVEL GRANT' in base_scholarship.funding}")
    print()

    all_passed = True

    for desc, days_offset, expected_deadline_points in deadline_tests:
        # Create scholarship with specific deadline
        if days_offset is not None:
            deadline = datetime.now(timezone.utc) + timedelta(days=days_offset)
        else:
            deadline = None

        test_scholarship = Scholarship(
            title=f"Test {desc}",
            link=f"https://example.com/test-{days_offset}",
            description="Renewable energy opportunity",  # Matches field
            eligibility="Open to Sudanese students",  # Matches nationality
            funding="Partial funding",  # Does NOT match funding keywords
            field="Renewable Energy",  # Matches field
            level="Undergraduate",  # Does NOT match level keywords
            nationality="Sudanese",  # Matches nationality
            deadline=deadline
        )

        score, details = filter_obj._calculate_relevance_score(test_scholarship)
        base_score = 50  # nationality (25) + field (25)
        expected_total = min(100, base_score + expected_deadline_points)  # Clamped at 100
        actual_deadline_score = details.get('deadline_score', -999)

        # Check if deadline scoring is correct
        deadline_correct = actual_deadline_score == expected_deadline_points

        # Check if total score is correct (base + deadline, clamped at 100)
        total_correct = score == expected_total

        if deadline_correct and total_correct:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False

        print(f"{status} {desc}")
        print(f"    Days offset: {days_offset}")
        print(f"    Deadline score: {actual_deadline_score} (expected {expected_deadline_points})")
        print(f"    Base score: {base_score} (nationality + field)")
        print(f"    Expected total: {expected_total}")
        print(f"    Actual total: {score}")
        print(f"    Details: nat={details['nationality_match']}, fld={details['field_match']}, lvl={details['level_match']}, fin={details['funding_match']}, dl={details['deadline_match']}")
        if not deadline_correct or not total_correct:
            print(f"    -> ISSUE: deadline_correct={deadline_correct}, total_correct={total_correct}")
        print()

    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Deadline scoring correctly impacts total score.")
        print("   The enhancement is working as intended.")
    else:
        print("❌ SOME TESTS FAILED. Please review the output above.")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    test_deadline_impact()