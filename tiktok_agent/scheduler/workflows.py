"""Orchestrates daily and weekly workflows."""
from __future__ import annotations

from tiktok_agent.analytics_engine.engine import build_daily_insights, build_weekly_report
from tiktok_agent.config.settings import Settings
from tiktok_agent.content_generator.generator import generate_daily_ideas
from tiktok_agent.data_collector.collector import run_daily_collection
from tiktok_agent.database.supabase_client import SupabaseClient
from tiktok_agent.strategy_brain.brain import generate_weekly_strategy
from tiktok_agent.telegram_bot.bot import TelegramBot, format_daily_message, format_weekly_message
from tiktok_agent.trend_scanner.scanner import scan_trends


def run_daily_workflow(settings: Settings) -> None:
    run_daily_collection(settings)
    db = SupabaseClient(settings.supabase_url, settings.supabase_key)
    videos = db.select("video_analytics", order="posting_time.desc", limit=100)

    insights = build_daily_insights(videos)
    trends = scan_trends(settings.openai_api_key)
    ideas = generate_daily_ideas(settings.openai_api_key, insights, trends)

    bot = TelegramBot(settings.telegram_bot_token, settings.telegram_chat_id)
    bot.send_message(format_daily_message(insights, ideas))


def run_weekly_workflow(settings: Settings) -> None:
    db = SupabaseClient(settings.supabase_url, settings.supabase_key)
    videos = db.select("video_analytics", order="posting_time.desc", limit=500)

    weekly_report = build_weekly_report(videos)
    trends = scan_trends(settings.openai_api_key)
    strategy = generate_weekly_strategy(settings.openai_api_key, weekly_report, trends)

    bot = TelegramBot(settings.telegram_bot_token, settings.telegram_chat_id)
    bot.send_message(format_weekly_message(weekly_report, strategy))
