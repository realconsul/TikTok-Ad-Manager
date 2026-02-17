from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException

from tiktok_agent.config.settings import Settings
from tiktok_agent.scheduler.workflows import run_daily_workflow, run_weekly_workflow

app = FastAPI(title="Tecton TikTok Agent API")


def _validate_cron_secret(authorization: str | None) -> None:
    expected = os.getenv("CRON_SECRET", "")
    if not expected:
        return
    expected_header = f"Bearer {expected}"
    if authorization != expected_header:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/daily")
def daily(authorization: str | None = Header(default=None)) -> dict[str, str]:
    _validate_cron_secret(authorization)
    settings = Settings.from_env()
    settings.validate()
    run_daily_workflow(settings)
    return {"status": "daily workflow completed"}


@app.get("/api/weekly")
def weekly(authorization: str | None = Header(default=None)) -> dict[str, str]:
    _validate_cron_secret(authorization)
    settings = Settings.from_env()
    settings.validate()
    run_weekly_workflow(settings)
    return {"status": "weekly workflow completed"}
