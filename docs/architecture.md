# GoreeCloud Social — Architecture

## Current Development shape

The first native foundation is a Django server with one Social domain application, one relational development database, a read-only development shell, and bounded health/status routes.

The current separation is intentional:

- `SocialProfile` owns social presentation metadata but references an external GoreeCloud Identity subject.
- Social relationships and content metadata remain application-owned.
- `visible_posts_for()` centralizes the current read-side audience rules so clients do not decide authorization independently.
- media records contain storage references only; production storage and media processing are separate future capabilities.
- no public write HTTP API exists before platform authorization, privacy, security, and abuse requirements are ready.

## Intended service boundaries

Long-term Social can split high-load responsibilities without splitting authority semantics:

- Social Core — profiles, posts, relationships, communities, permissions, moderation state;
- Feed & Discovery — eligible-candidate selection and transparent ranking;
- Media — upload, processing, storage, derivatives, playback metadata;
- Realtime — notification/fan-out transport;
- Search — authorized indexing and retrieval;
- Trust & Safety — abuse signals, queues, evidence, enforcement coordination.

These components should communicate through documented, versioned contracts and GoreeCloud Mesh where appropriate. They must not bypass GoreeCloud Identity, Privacy Shield, Wardveil Security, or application ownership boundaries.
