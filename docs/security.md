# GoreeCloud Social — Security Status

## Implemented Development controls

- No public social write or account-authentication endpoints.
- Production mode refuses startup without an explicit secret key.
- Bounded health/readiness/status endpoints.
- Database constraints for duplicate reactions, duplicate reposts, duplicate relationships, and self-follow prevention.
- Server framing/content-type hardening defaults.
- Source-status responses explicitly report unfinished platform integration state.

## Required before production

- GoreeCloud Identity authentication and scoped authorization.
- Wardveil session, request, upload, malicious-link/file, automation, abuse, and privileged-action controls.
- CSRF/session design for any browser write surface.
- Rate controls and anti-automation behavior.
- production database and secret-management design.
- TLS/reverse-proxy deployment acceptance.
- media upload validation, scanning, processing isolation, and storage authorization.
- moderator/admin auditability and separation of authority.
- dependency scanning, vulnerability response, security testing, and release evidence.

Development hardening must not be represented as Wardveil Security acceptance.
