#!/usr/bin/env python3
"""
Simple script to run the scholarship bot.
Can be used for testing or deployment.
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholarship_bot import main

if __name__ == "__main__":
    main()