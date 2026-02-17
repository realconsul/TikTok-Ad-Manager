"""Entry point for long-running scheduler."""
from __future__ import annotations

import logging
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from tiktok_agent.config.settings import Settings
from tiktok_agent.scheduler.workflows import run_daily_workflow, run_weekly_workflow

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main() -> None:
    settings = Settings.from_env()
    settings.validate()

    scheduler = BlockingScheduler(timezone=settings.timezone)
    scheduler.add_job(
        run_daily_workflow,
        CronTrigger(hour=7, minute=0),
        args=[settings],
        id="daily_workflow",
        replace_existing=True,
    )
    scheduler.add_job(
        run_weekly_workflow,
        CronTrigger(day_of_week="sun", hour=7, minute=0),
        args=[settings],
        id="weekly_workflow",
        replace_existing=True,
    )

    logging.info("Scheduler started. Daily at 7AM and weekly on Sunday 7AM.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
