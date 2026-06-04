"""
Storage module for tracking seen scholarships to avoid duplicate notifications.
"""
import sqlite3
import hashlib
import json
import os
from datetime import datetime
from typing import Optional
from models import Scholarship

class Storage:
    """Handles persistence of seen scholarships using SQLite."""

    def __init__(self, db_path: str = "scholarships_seen.db"):
        """Initialize storage with SQLite database."""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create the database table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS seen_scholarships (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def _get_scholarship_id(self, scholarship: Scholarship) -> str:
        """Generate a unique ID for a scholarship based on title and link."""
        # Create a consistent hash from title and link
        data = f"{scholarship.title}|{scholarship.link}"
        return hashlib.md5(data.encode()).hexdigest()

    def is_seen(self, scholarship: Scholarship) -> bool:
        """Check if we've already seen this scholarship."""
        scholarship_id = self._get_scholarship_id(scholarship)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM seen_scholarships WHERE id = ?",
                (scholarship_id,)
            )
            return cursor.fetchone() is not None

    def mark_as_seen(self, scholarship: Scholarship):
        """Mark a scholarship as seen."""
        scholarship_id = self._get_scholarship_id(scholarship)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''INSERT OR IGNORE INTO seen_scholarships (id, title, link)
                   VALUES (?, ?, ?)''',
                (scholarship_id, scholarship.title, scholarship.link)
            )
            conn.commit()

    def get_recent_scholarships(self, limit: int = 100) -> list:
        """Get recently seen scholarships (for debugging/inspection)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                '''SELECT title, link, seen_at FROM seen_scholarships
                   ORDER BY seen_at DESC LIMIT ?''',
                (limit,)
            )
            return [
                {
                    'title': row[0],
                    'link': row[1],
                    'seen_at': row[2]
                }
                for row in cursor.fetchall()
            ]

    def clear_old_records(self, days: int = 30):
        """Clear records older than specified days."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM seen_scholarships WHERE seen_at < datetime('now', '-{} days')".format(days)
            )
            conn.commit()