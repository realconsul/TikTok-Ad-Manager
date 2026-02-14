"""Domain models for TikTok analytics."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class VideoAnalytics:
    video_id: str
    caption: str
    posting_time: datetime
    views: int
    likes: int
    comments: int
    shares: int
    saves: int
    watch_time: float
    completion_rate: float
    follower_growth_after_post: int
    video_length_seconds: int

    def to_db_row(self) -> dict[str, Any]:
        row = asdict(self)
        row["posting_time"] = self.posting_time.isoformat()
        return row
