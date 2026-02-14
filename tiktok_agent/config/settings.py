"""Application settings loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    tiktok_access_token: str
    tiktok_advertiser_id: str
    openai_api_key: str
    telegram_bot_token: str
    telegram_chat_id: str
    supabase_url: str
    supabase_key: str
    timezone: str = "Africa/Lagos"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            tiktok_access_token=os.getenv("TIKTOK_ACCESS_TOKEN", ""),
            tiktok_advertiser_id=os.getenv("TIKTOK_ADVERTISER_ID", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_key=os.getenv("SUPABASE_KEY", ""),
            timezone=os.getenv("TIMEZONE", "Africa/Lagos"),
        )

    def validate(self) -> None:
        missing = [
            name
            for name, value in self.__dict__.items()
            if name != "timezone" and not value
        ]
        if missing:
            raise ValueError(
                f"Missing required environment variables for: {', '.join(missing)}"
            )
