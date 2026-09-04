# GoreeCloud Social

GoreeCloud Social is the in-development, first-party GoreeCloud social platform for public and private social publishing, short-form video, photos, communities, groups, social relationships, reactions, reposts, discovery, and supported GoreeCloud integrations.

## Current status

**Development source — not Stable, not production-ready, and not yet a public social service.**

The native Development foundation establishes:

- a Django 5.2 development server and read-only source-status interface;
- liveness, database-aware readiness, and bounded product-status endpoints;
- GoreeCloud Social profile metadata that references an external GoreeCloud Identity subject instead of creating a second password or authentication store;
- groups and communities with membership and role primitives;
- follow relationships, block and mute relationships, posts, explicit reply-parent relationships, media references, single-choice poll groundwork, private bookmarks, reactions, reposts, and report records;
- audience-aware post visibility for public, followers, mutual relationships, spaces, and private-to-self content;
- ordinary read visibility that enforces bilateral blocks and viewer-selected mutes;
- internal Following and Chronological feed read models that reuse the same visibility and relationship-safety boundary;
- a responsive Glaze-oriented development shell for Home, Discover, Video, Communities, and Profile surfaces without claiming Glaze UI acceptance;
- repository documentation, tests, CI, and a Platform Contract v0.2 declaration that truthfully records unfinished platform integrations.

The reply, bookmark, poll, and feed foundations are internal Development domain/query capabilities only. They do not expose public mutation or personalized-feed endpoints and do not establish production thread authorization, poll policy, recommendation ranking, production feed delivery, authentication, or client synchronization.

This source does **not** yet provide production authentication, public social write APIs, public personalized feed APIs, production media upload/transcoding, recommendation ranking, notifications, live streaming, production moderation operations, production storage, mobile applications, production deployment, or accepted integrations with GoreeCloud Identity, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, GoreeCloud Manager, or Glaze UI.

## Development setup

Requirements:

- Python 3.14

Create an isolated environment and run the development server:

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

Then open `http://127.0.0.1:8000/`.

## Development endpoints

- `GET /livez/` — process liveness.
- `GET /readyz/` — database-aware readiness.
- `GET /api/v1/status/` — bounded product, lifecycle, version, capability, and integration-status information.

No content-creation, account-authentication, bookmark/poll/reply mutation, or personalized-feed API is exposed by this milestone. That boundary is intentional until GoreeCloud Identity authorization, Privacy Shield policy, Wardveil Security controls, and abuse protections are defined and implemented for those operations.

## Validation

```bash
export PYTHONPATH=src
export SOCIAL_ENV=test
export SOCIAL_SECRET_KEY='test-only-key'
python scripts/validate_repository.py
python -m compileall -q manage.py src tests scripts
python manage.py makemigrations --check --dry-run
python manage.py migrate --noinput
python manage.py check
python manage.py test tests -v 2
```

Passing source CI does not establish production deployment, platform-system acceptance, privacy acceptance, security acceptance, recovery acceptance, or Stable qualification.

## Documentation

- [Specifications](SPECIFICATIONS.md)
- [Features](FEATURES.md)
- [Benefits](BENEFITS.md)
- [Competitive objectives](COMPETITIVE-OBJECTIVES.md)
- [Branding](BRANDING.md)
- [User manual](USER-MANUAL.md)
- [Architecture](docs/architecture.md)
- [Platform integration status](docs/platform-integration-status.md)
- [Security status](docs/security.md)
- [Privacy status](docs/privacy.md)
- [Recovery status](docs/recovery.md)

## Platform Contract

This repository carries a schema-version `0.2` `goreecloud.platform.yaml` declaration. It records the application as Development and nonconformant while required Integral Platform System integrations and acceptance evidence remain incomplete.

## License

GoreeCloud Social is licensed under the GNU Affero General Public License v3.0 only (`AGPL-3.0-only`). See [LICENSE](LICENSE) for the complete license text.
