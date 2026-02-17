# Tecton Academy TikTok Growth Automation Agent

Automated TikTok growth system that collects analytics daily, analyzes performance, scans trends,
generates content ideas/scripts, and delivers daily + weekly recommendations to Telegram.

## Features

- **Daily automation (7am)**
  - Pull TikTok analytics from TikTok Business API
  - Store metrics in Supabase
  - Analyze latest performance
  - Scan TikTok/tech trends with OpenAI
  - Generate 3 daily TikTok ideas (hook, script, caption, hashtags, format)
  - Send briefing to Telegram
- **Weekly automation (Sunday 7am)**
  - Build weekly growth report
  - Evaluate pillar performance and growth
  - Generate strategy adjustments and experiments
  - Send weekly strategy update to Telegram

## Project Structure

```text
tiktok_agent/
  data_collector/
  analytics_engine/
  trend_scanner/
  content_generator/
  strategy_brain/
  telegram_bot/
  scheduler/
  database/
  config/
README.md
requirements.txt
.env.example
```

## Setup

1. **Create virtual environment & install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configure environment variables**

```bash
cp .env.example .env
```

Fill `.env`:

- `TIKTOK_ACCESS_TOKEN` - TikTok Business API token
- `TIKTOK_ADVERTISER_ID` - Advertiser/account ID
- `OPENAI_API_KEY` - OpenAI API key
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from BotFather
- `TELEGRAM_CHAT_ID` - Target chat/channel ID
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase service role key
- `TIMEZONE` - e.g. `Africa/Lagos`

3. **Create database table in Supabase**

Run SQL in `tiktok_agent/database/schema.sql` using Supabase SQL editor.

## Run Locally

Start continuous scheduler (best for local dev or VPS):

```bash
python -m tiktok_agent.main
```

## Deploy on Vercel (Step-by-Step)

> Vercel does not run long-lived background processes like APScheduler.
> For Vercel, this project uses **HTTP endpoints + Vercel Cron Jobs**.

### 1) Push code to GitHub

Make sure your repository includes:

- `api/index.py` (API endpoints for daily/weekly runs)
- `vercel.json` (cron schedules)

### 2) Import project into Vercel

1. Log in to Vercel.
2. Click **Add New → Project**.
3. Import your GitHub repo.
4. Framework preset: **Other** (Python runtime is auto-detected).

### 3) Add environment variables in Vercel

In **Project Settings → Environment Variables**, add:

- `TIKTOK_ACCESS_TOKEN`
- `TIKTOK_ADVERTISER_ID`
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `TIMEZONE` (use `Africa/Lagos`)
- `CRON_SECRET` (random strong string, used to protect cron endpoints)

### 4) Configure Supabase table

Run SQL from `tiktok_agent/database/schema.sql` in your Supabase SQL editor.

### 5) Deploy

Click **Deploy** in Vercel.

After deploy, test:

- `GET /api/health` → should return `{"status":"ok"}`

### 6) Set up Vercel Cron

This repo already includes `vercel.json`:

- `0 6 * * *` → calls `/api/daily` (6:00 UTC = 7:00 Lagos)
- `0 6 * * 0` → calls `/api/weekly` (Sunday 6:00 UTC = Sunday 7:00 Lagos)

### 7) Verify cron authorization

Endpoints require:

- `Authorization: Bearer <CRON_SECRET>`

Vercel automatically sends this when `CRON_SECRET` is set in environment variables.

### 8) Monitor production runs

Use:

- Vercel **Logs** for endpoint execution
- Telegram messages for delivery confirmation
- Supabase table rows for ingestion confirmation

If runs fail, first check missing env vars and API credential scopes.

## Module Responsibilities

- `data_collector`: Pulls TikTok analytics and writes to DB.
- `analytics_engine`: Computes engagement, best posting time, best topics, weekly growth.
- `trend_scanner`: Produces structured trend insights.
- `content_generator`: Produces 3 daily content ideas in structured JSON.
- `strategy_brain`: Produces weekly strategy recommendations.
- `telegram_bot`: Formats and sends daily/weekly messages.
- `scheduler`: Runs daily + weekly workflows automatically.

## Deployment Alternatives

### Option 1: VM / VPS

- Deploy to Ubuntu server.
- Use systemd service to keep process alive.
- Run `python -m tiktok_agent.main`.

### Option 2: Docker + Cloud VM

- Containerize app and run as long-lived process.
- Use health checks and restart policy.

### Option 3: Render / Railway background worker

- Deploy as worker process.
- Set environment variables in dashboard.

## Extending the Agent

- Add richer TikTok API fields by editing `data_collector/tiktok_api.py`.
- Add more KPI formulas in `analytics_engine/engine.py`.
- Replace trend scanner prompt with external trend APIs if available.
- Add multilingual content generation for English + Pidgin.
- Add A/B testing memory table in Supabase for experiment tracking.

## Notes

- TikTok endpoint fields may vary by account permissions; adjust dimensions/metrics as needed.
- OpenAI outputs are expected in strict JSON. If model output deviates, add JSON schema enforcement.
- Telegram parser uses Markdown; escape special characters if injecting raw user-generated text.
