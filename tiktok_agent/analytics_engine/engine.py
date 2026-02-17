"""Analytics calculations and summaries."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from statistics import mean
from typing import Any


def engagement_rate(video: dict[str, Any]) -> float:
    views = max(int(video.get("views", 0)), 1)
    interactions = sum(
        int(video.get(metric, 0)) for metric in ("likes", "comments", "shares", "saves")
    )
    return round((interactions / views) * 100, 2)


def best_posting_time(videos: list[dict[str, Any]]) -> int:
    hourly_scores: dict[int, list[float]] = defaultdict(list)
    for video in videos:
        post_time = datetime.fromisoformat(video["posting_time"])
        hourly_scores[post_time.hour].append(engagement_rate(video))
    if not hourly_scores:
        return 19
    return max(hourly_scores.items(), key=lambda item: mean(item[1]))[0]


def best_performing_topics(videos: list[dict[str, Any]]) -> list[str]:
    topic_counter: Counter[str] = Counter()
    for video in videos:
        caption = video.get("caption", "").lower()
        for token in ["design", "frontend", "backend", "mobile", "product", "ai", "career"]:
            if token in caption:
                topic_counter[token] += 1
    return [topic for topic, _ in topic_counter.most_common(3)]


def best_video_length(videos: list[dict[str, Any]]) -> int:
    if not videos:
        return 45
    return int(
        mean(
            int(v.get("video_length_seconds", 45) or 45)
            for v in videos
            if float(v.get("completion_rate", 0) or 0) > 0
        )
    )


def weekly_growth_metrics(videos: list[dict[str, Any]]) -> dict[str, float]:
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    last_week = [v for v in videos if datetime.fromisoformat(v["posting_time"]) >= week_ago]
    total_views = sum(int(v.get("views", 0)) for v in last_week)
    total_followers = sum(int(v.get("follower_growth_after_post", 0)) for v in last_week)
    avg_engagement = mean([engagement_rate(v) for v in last_week] or [0])
    return {
        "videos_count": len(last_week),
        "total_views": total_views,
        "follower_growth": total_followers,
        "average_engagement_rate": round(avg_engagement, 2),
    }


def build_daily_insights(videos: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "best_posting_hour": best_posting_time(videos),
        "top_topics": best_performing_topics(videos),
        "best_video_length_seconds": best_video_length(videos),
        "top_video_engagement_rate": max((engagement_rate(v) for v in videos), default=0),
    }


def build_weekly_report(videos: list[dict[str, Any]]) -> dict[str, Any]:
    report = weekly_growth_metrics(videos)
    report["content_pillar_winners"] = best_performing_topics(videos)
    report["recommended_hook_style"] = "Problem → Relatable Story → Actionable Tip"
    return report
