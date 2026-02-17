"""TikTok Business API connector.

This module uses the reporting endpoint shape as a reference implementation.
You may need to adjust endpoint paths/fields to match your TikTok app scope.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import requests

from tiktok_agent.data_collector.models import VideoAnalytics


class TikTokAPIClient:
    def __init__(self, access_token: str, advertiser_id: str) -> None:
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"
        self.access_token = access_token
        self.advertiser_id = advertiser_id

    @property
    def headers(self) -> dict[str, str]:
        return {"Access-Token": self.access_token, "Content-Type": "application/json"}

    def fetch_daily_video_analytics(self) -> list[VideoAnalytics]:
        end_date = datetime.now(timezone.utc).date()
        start_date = end_date - timedelta(days=1)
        payload = {
            "advertiser_id": self.advertiser_id,
            "report_type": "BASIC",
            "data_level": "AUCTION_AD",
            "dimensions": ["stat_time_day", "ad_id"],
            "metrics": [
                "spend",
                "impressions",
                "clicks",
            ],
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "page": 1,
            "page_size": 100,
        }

        response = requests.post(
            f"{self.base_url}/report/integrated/get/",
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        raw_rows = response.json().get("data", {}).get("list", [])
        return [self._to_video_analytics(row) for row in raw_rows]

    def _to_video_analytics(self, row: dict) -> VideoAnalytics:
        stat = row.get("metrics", {})
        dimensions = row.get("dimensions", {})
        impressions = int(stat.get("impressions", 0))
        clicks = int(stat.get("clicks", 0))
        comments = int(stat.get("comments", 0)) if stat.get("comments") else 0
        shares = int(stat.get("shares", 0)) if stat.get("shares") else 0

        return VideoAnalytics(
            video_id=str(dimensions.get("ad_id", "")),
            caption=str(dimensions.get("ad_name", "")),
            posting_time=datetime.fromisoformat(
                dimensions.get("stat_time_day", datetime.utcnow().date().isoformat())
            ),
            views=impressions,
            likes=clicks,
            comments=comments,
            shares=shares,
            saves=int(stat.get("conversion", 0) or 0),
            watch_time=float(stat.get("video_watched_2s", 0) or 0),
            completion_rate=float(stat.get("video_play_actions", 0) or 0),
            follower_growth_after_post=int(stat.get("follows", 0) or 0),
            video_length_seconds=int(stat.get("video_watched_6s", 0) or 0),
        )
