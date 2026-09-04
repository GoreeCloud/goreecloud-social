# GoreeCloud Social — Development User Manual

## Status

The current repository is a Development foundation, not an end-user social service. Do not expose it as a production social platform.

## Start the development server

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export PYTHONPATH=src
export SOCIAL_ENV=development
export SOCIAL_SECRET_KEY='development-only-change-me'
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the development shell.

## What can be exercised now

- Check process liveness at `/livez/`.
- Check database readiness at `/readyz/`.
- Inspect bounded source status at `/api/v1/status/`.
- Use Django tests to exercise social-domain model constraints and audience visibility.
- Inspect the responsive UI information architecture.

## What is intentionally unavailable

There is no public account login, content publishing API, media upload flow, recommendation feed, realtime notifications, live streaming, production moderation console, or production deployment in this milestone.

Those features remain unavailable until the required Identity, Privacy Shield, Wardveil, Mesh, Everkeep, Manager, Glaze UI, media, abuse-prevention, and production-readiness work is implemented and verified.
