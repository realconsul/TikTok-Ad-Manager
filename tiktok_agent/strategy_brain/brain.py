"""Weekly strategy recommendation module."""
from __future__ import annotations

import json

from openai import OpenAI


PROMPT = """
You are a growth strategist for a TikTok tech academy.
Using weekly analytics and trend insights, return STRICT JSON with:
content_pillar_focus (array), posting_frequency_recommendation (string),
experiment_ideas (array), messaging_improvements (array), summary (string).
"""


def generate_weekly_strategy(openai_api_key: str, weekly_report: dict, trends: dict) -> dict:
    client = OpenAI(api_key=openai_api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": PROMPT},
            {
                "role": "user",
                "content": f"Weekly report: {json.dumps(weekly_report)}\nTrends: {json.dumps(trends)}",
            },
        ],
        temperature=0.4,
    )
    return json.loads(response.output_text)
