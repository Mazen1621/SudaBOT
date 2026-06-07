#!/usr/bin/env python3
"""
Debug the date comparison issue
"""
from datetime import datetime, timedelta, timezone

def debug_deadline_calculation():
    print("=" * 60)
    print("DEBUGGING DEADLINE CALCULATION")
    print("=" * 60)

    # Test case: deadline is "now" (0 days from now)
    print("\n1. Testing deadline = now (0 days from now):")
    now1 = datetime.now(timezone.utc)
    print(f"   First now() call: {now1}")

    deadline = now1 + timedelta(days=0)
    print(f"   Deadline (now + 0 days): {deadline}")
    print(f"   Deadline.tzinfo is None: {deadline.tzinfo is None}")

    now2 = datetime.now(timezone.utc)
    print(f"   Second now() call: {now2}")
    print(f"   Are they equal? {now1 == now2}")
    print(f"   Time difference: {now2 - now1}")

    # Make deadline timezone-aware if needed (replicating filter.py logic)
    if deadline.tzinfo is None:
        deadline_aware = deadline.replace(tzinfo=timezone.utc)
        print(f"   Made timezone aware: {deadline_aware}")
    else:
        deadline_aware = deadline
        print(f"   Already timezone aware: {deadline_aware}")

    # Check if deadline is in the past
    is_past = deadline_aware < now2
    print(f"   Is deadline in the past? (deadline_aware < now2): {is_past}")
    print(f"   deadline_aware < now2 evaluates to: {deadline_aware < now2}")

    if not is_past:
        days_until_deadline = (deadline_aware - now2).days
        print(f"   Days until deadline: {days_until_deadline}")
        print(f"   (deadline_aware - now2): {deadline_aware - now2}")
        print(f"   .days attribute: {(deadline_aware - now2).days}")

    print()

    # Test case: deadline is 31 days from now
    print("2. Testing deadline = now + 31 days:")
    now1 = datetime.now(timezone.utc)
    print(f"   First now() call: {now1}")

    deadline = now1 + timedelta(days=31)
    print(f"   Deadline (now + 31 days): {deadline}")

    now2 = datetime.now(timezone.utc)
    print(f"   Second now() call: {now2}")
    print(f"   Time difference: {now2 - now1}")

    # Make deadline timezone-aware if needed
    if deadline.tzinfo is None:
        deadline_aware = deadline.replace(tzinfo=timezone.utc)
    else:
        deadline_aware = deadline

    # Check if deadline is in the past
    is_past = deadline_aware < now2
    print(f"   Is deadline in the past? {is_past}")

    if not is_past:
        days_until_deadline = (deadline_aware - now2).days
        print(f"   Days until deadline: {days_until_deadline}")
        print(f"   (deadline_aware - now2): {deadline_aware - now2}")

    print()

if __name__ == "__main__":
    debug_deadline_calculation()