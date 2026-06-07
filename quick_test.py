#!/usr/bin/env python3
"""Quick test to verify the filter works"""
from models import Scholarship
from filter import ScholarshipFilter
from datetime import datetime, timedelta

# Create scholarship with deadline
now = datetime.now()
scholarship = Scholarship(
    title="Test Scholarship",
    link="https://example.com",
    description="Renewable energy scholarship for Sudanese students",
    eligibility="Open to Sudanese students",
    funding="Fully funded",
    field="Renewable Energy",
    level="PhD",
    nationality="Sudanese",
    deadline=now + timedelta(days=30)  # 30 days from now
)

# Test filter
filter_obj = ScholarshipFilter()
score, details = filter_obj._calculate_relevance_score(scholarship)

print(f"Title: {scholarship.title}")
print(f"Score: {score}/100")
print(f"Details: {details}")

# Check if deadline scoring worked
if details.get('deadline_match'):
    print(f"✅ Deadline scoring active: {details.get('deadline_score')} points")
else:
    print("❌ Deadline scoring not active")

# Check if it passes threshold
if score >= 60:
    print("✅ Scholarship passes relevance threshold")
else:
    print("❌ Scholarship fails relevance threshold")