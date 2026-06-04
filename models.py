"""
Data model for scholarship objects.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Scholarship:
    """Represents a scholarship opportunity."""
    title: str
    link: str
    description: str
    eligibility: str
    funding: str
    field: str
    level: str  # Master, MPhil, PhD, etc.
    nationality: str  # Who can apply
    deadline: Optional[datetime] = None
    source: str = ""  # Which website it came from

    def __hash__(self):
        """Make Scholarship hashable for use in sets/dicts."""
        return hash((self.title, self.link))

    def __eq__(self, other):
        """Check equality based on title and link."""
        if not isinstance(other, Scholarship):
            return False
        return self.title == other.title and self.link == other.link

    def to_dict(self):
        """Convert to dictionary for storage/serialization."""
        return {
            'title': self.title,
            'link': self.link,
            'description': self.description,
            'eligibility': self.eligibility,
            'funding': self.funding,
            'field': self.field,
            'level': self.level,
            'nationality': self.nationality,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'source': self.source
        }

    @classmethod
    def from_dict(cls, data):
        """Create Scholarship from dictionary."""
        deadline = None
        if data.get('deadline'):
            try:
                deadline = datetime.fromisoformat(data['deadline'])
            except ValueError:
                pass  # Keep as None if parsing fails

        return cls(
            title=data['title'],
            link=data['link'],
            description=data['description'],
            eligibility=data['eligibility'],
            funding=data['funding'],
            field=data['field'],
            level=data['level'],
            nationality=data['nationality'],
            deadline=deadline,
            source=data.get('source', '')
        )