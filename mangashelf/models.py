from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List

@dataclass
class Manga:
    title: str
    author: str
    current_chapter: int = 0
    total_chapters: Optional[int] = None
    status: str = "Plan to Read"  # Reading, Completed, On Hold, Dropped, Plan to Read
    rating: Optional[float] = None
    notes: str = ""
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
