# Railway Deployment Guide

## Steps

### 1. Create a Railway project
- Go to railway.app → New Project → Deploy from GitHub repo
- Or use Railway CLI: `railway init`

### 2. Add plugins in Railway dashboard
- **PostgreSQL**: Add Plugin → PostgreSQL (Railway auto-sets `DATABASE_URL`)
- **Redis** (optional): Add Plugin → Redis (Railway auto-sets `REDIS_URL`)

### 3. Set environment variables in Railway dashboard
```
BOT_TOKEN=8724591968:AAHHrd5IzjWsh4Xt2elwFOxB53Ef4DfxBEE
ADMIN_IDS=917456291
WEBHOOK_URL=https://YOUR_APP.up.railway.app
```
> DATABASE_URL and REDIS_URL are injected automatically by Railway plugins.

### 4. Deploy
Railway will auto-build and deploy using `railway.toml`.
The start command is: `python -m bot.main`

### 5. Seed vocabulary after first deploy
In Railway → your service → shell (or locally with the Railway DATABASE_URL):
```bash
python -m scripts.seed_data
```

## Local development
```bash
pip install -r requirements.txt
# Set up PostgreSQL locally, then:
python -m scripts.seed_data
python -m bot.main
```

## Admin commands
- `/admin` — open admin panel (only works for ADMIN_IDS)

## Architecture
- **Polling mode**: default when WEBHOOK_URL is empty
- **Webhook mode**: set WEBHOOK_URL to your Railway public URL
- **Scheduler**: APScheduler runs at 00:01 (Shijoat reset) and 19:00 (reminders), Tashkent timezone
