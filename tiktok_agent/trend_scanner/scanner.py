"""Trend scanning module using OpenAI web-informed reasoning input prompts."""
from __future__ import annotations

import json

from openai import OpenAI

TREND_PROMPT = """
You are a TikTok trend analyst for a Nigerian tech education brand.
Find current trends around: tech careers, learning tech, programming,
product design, AI tools, and career switching.
Return STRICT JSON with keys:
viral_hooks (array), storytelling_formats (array), trending_topics (array), notes (string).
"""


def scan_trends(openai_api_key: str) -> dict:
    client = OpenAI(api_key=openai_api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=TREND_PROMPT,
        temperature=0.4,
    )
    text = response.output_text.strip()
    return json.loads(text)
