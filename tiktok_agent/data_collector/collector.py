"""Daily data collection workflow."""
from __future__ import annotations

from tiktok_agent.config.settings import Settings
from tiktok_agent.data_collector.tiktok_api import TikTokAPIClient
from tiktok_agent.database.supabase_client import SupabaseClient


def run_daily_collection(settings: Settings) -> list[dict]:
    tiktok = TikTokAPIClient(settings.tiktok_access_token, settings.tiktok_advertiser_id)
    db = SupabaseClient(settings.supabase_url, settings.supabase_key)

    analytics_rows = [item.to_db_row() for item in tiktok.fetch_daily_video_analytics()]
    if not analytics_rows:
        return []
    return db.upsert_rows("video_analytics", analytics_rows, on_conflict="video_id,posting_time")
