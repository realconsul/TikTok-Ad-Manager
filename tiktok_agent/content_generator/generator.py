"""Daily content idea generation."""
from __future__ import annotations

import json

from openai import OpenAI

SYSTEM_PROMPT = """
You generate TikTok content for Tecton Academy.
Audience: Nigerian students, beginners, career switchers.
Topics: Product Design, Frontend, Backend, Mobile, Product Management, AI in product dev,
career switch, salaries, affordable learning.
Return STRICT JSON with key 'ideas' containing exactly 3 items.
Each idea must include:
topic, target_audience, content_goal, hook, script_30_60_seconds,
caption, hashtags, on_screen_text, video_format.
"""


def generate_daily_ideas(openai_api_key: str, insights: dict, trends: dict) -> dict:
    client = OpenAI(api_key=openai_api_key)
    user_prompt = (
        "Use these analytics insights and trends to create today's ideas.\n"
        f"Insights: {json.dumps(insights)}\n"
        f"Trends: {json.dumps(trends)}"
    )
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.6,
    )
    return json.loads(response.output_text)
