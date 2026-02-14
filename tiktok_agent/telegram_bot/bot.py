"""Telegram delivery helpers."""
from __future__ import annotations

import json

import requests


class TelegramBot:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id
        self.endpoint = f"https://api.telegram.org/bot{token}/sendMessage"

    def send_message(self, message: str) -> None:
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(self.endpoint, json=payload, timeout=30)
        response.raise_for_status()


def format_daily_message(insights: dict, ideas: dict) -> str:
    lines = [
        "*📈 Tecton Academy Daily TikTok Briefing*",
        f"Best posting time today: *{insights.get('best_posting_hour', 19)}:00*",
        f"Top insights: {', '.join(insights.get('top_topics', [])) or 'N/A'}",
        "",
        "*Today's 3 content ideas:*",
    ]
    for idx, idea in enumerate(ideas.get("ideas", []), start=1):
        lines.extend(
            [
                f"{idx}. *{idea.get('topic', 'Topic')}*",
                f"Hook: {idea.get('hook', '-')}",
                f"Caption: {idea.get('caption', '-')}",
                f"Hashtags: {' '.join(idea.get('hashtags', []))}",
                "",
            ]
        )
    return "\n".join(lines)


def format_weekly_message(report: dict, strategy: dict) -> str:
    return "\n".join(
        [
            "*📊 Weekly TikTok Growth Report*",
            f"Videos: {report.get('videos_count', 0)}",
            f"Views: {report.get('total_views', 0)}",
            f"Follower growth: {report.get('follower_growth', 0)}",
            f"Avg engagement rate: {report.get('average_engagement_rate', 0)}%",
            "",
            "*Strategy update*",
            f"Pillar focus: {', '.join(strategy.get('content_pillar_focus', []))}",
            f"Posting recommendation: {strategy.get('posting_frequency_recommendation', 'N/A')}",
            f"Experiments: {json.dumps(strategy.get('experiment_ideas', []), ensure_ascii=False)}",
        ]
    )
