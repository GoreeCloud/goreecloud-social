# GoreeCloud Social — Specifications

## 1. Product definition

GoreeCloud Social is an original, first-party GoreeCloud Suite application that combines several forms of social interaction in one coherent platform instead of reproducing separate incompatible products for short-form video, public conversation, personal profiles, groups, and communities.

The canonical product identity for this project is **GoreeCloud Social**. The approved short label is **Social** when the surrounding GoreeCloud context already establishes ownership. The repository is `GoreeCloud/goreecloud-social`. The application identifier mapping is intended to use the `social` suffix under the GoreeCloud reverse-DNS namespace, resulting in `com.goreecloud.social` where that identifier form applies.

GoreeCloud Social is a prefixed GoreeCloud-family product and a GoreeCloud Suite member. It is original GoreeCloud-owned software rather than a maintained fork or rebrand of TikTok, X/Twitter, Facebook, Mastodon, or another social platform.

## 2. Product scope

The long-term product scope includes:

- public, followers-only, mutual/friend, group, community, custom, and private publishing;
- short text, long text, threaded posts, photos, albums, GIFs, links, polls, short-form video, conventional video, and later live media where justified;
- likes, configurable reactions, replies, shares, reposts, quote-posts, bookmarks, mentions, hashtags, and content discovery;
- public and private profiles, follows, mutual relationships, lists/circles where useful, and controlled profile visibility;
- public, private, and invitation-only groups and communities;
- owners, administrators, moderators, members, invitations, membership requests, rules, moderation queues, and community-specific visibility;
- Following, chronological, Discover/For You, Communities, Groups, Video, and media-oriented feed surfaces;
- transparent recommendation controls, explanation of recommendation reasons, chronological choices, signal removal, topic reduction, and recommendation reset controls;
- creator-oriented drafts, scheduling, media libraries, series/playlists, analytics, collaboration, and later optional monetization only if separately approved;
- search, notifications, deep links, and authorized integrations with other GoreeCloud applications through defined contracts;
- export, migration, deletion, retention, recovery, and continuity support that preserves user control.

## 3. Unified content model

GoreeCloud Social should use one versioned content model with presentation-specific surfaces rather than maintaining unrelated post systems for each experience.

A post may contain text and zero or more typed media attachments. Presentation can adapt by surface: a text-focused conversation card in Home, a media card in a profile, an immersive vertical player in Video, or a community-scoped post in a group. The underlying authority, audience, moderation state, and identity relationship remain consistent.

The initial native foundation implements the following domain primitives:

- `SocialProfile`: application-owned social profile metadata linked to an external GoreeCloud Identity subject;
- `Space`: a group or community with visibility and an owning social profile;
- `SpaceMembership`: member, moderator, administrator, or owner role and membership state;
- `Follow`: directional social relationship with a request/accepted state and a no-self-follow invariant;
- `Post`: author, optional space, content type, audience, reply policy, moderation state, body, and timestamps;
- `MediaAttachment`: ordered photo, video, or GIF reference plus accessibility alternative text;
- `Reaction`: one typed reaction from a profile to a post;
- `Repost`: a repost or quote-repost relationship;
- `PostReport`: a user report record for later moderation workflows.

The initial code intentionally stores media references rather than implementing production upload, scanning, transcoding, object storage, or CDN behavior.

## 4. Audience and social graph

Audience evaluation is a first-class authorization concern, not merely a user-interface filter.

The first foundation implements read-side visibility semantics for:

- `public` — visible without a social profile;
- `followers` — visible to accepted followers of the author;
- `friends` — visible to mutual accepted follow relationships;
- `space` — visible to accepted members of the associated group or community;
- `only-me` — visible only to the author.

An author can always retrieve their own visible-state posts through the application visibility service. Removed, limited, and pending-moderation states are excluded from ordinary visibility queries.

Future custom audiences, blocks, mutes, account restrictions, age policy, legal restrictions, community bans, and Privacy Shield controls must be composed into the authoritative visibility decision rather than applied as cosmetic client-side filtering.

## 5. Feeds and discovery

GoreeCloud Social should eventually provide distinct user-selectable feed modes rather than hiding all behavior behind one opaque ranking system.

Planned feed families include:

- Following — content from followed profiles and joined spaces;
- Chronological — time-ordered eligible content with minimal ranking;
- Discover / For You — recommendation-driven discovery with user-understandable controls;
- Communities and Groups — scoped social spaces;
- Video — immersive short-form video plus a Following video mode;
- Media — optional photo/video browsing surfaces;
- Trending — only if a privacy-preserving and abuse-resistant definition is established.

Recommendation systems must expose enough information for users to understand why material is shown, reduce topics or signals, reset recommendations, and choose less-personalized or chronological behavior where supported. Engagement collection must not automatically become unrestricted profiling.

The initial foundation does not implement recommendation ranking or behavioral profiling.

## 6. Groups and communities

Groups and communities are first-class social spaces, not tags around ordinary posts.

A space can be public, private, or invitation-only. Its future policy model should support membership requests, invitations, member roles, moderator teams, rules, pinned content, announcements, bans, restricted members, content approval, moderation queues, and scoped discovery.

Administrative capability inside a space does not grant platform-wide authority. Community delegation must use GoreeCloud Identity-scoped authority when implemented, and moderator actions must remain auditable and subject to Wardveil and Privacy Shield requirements.

## 7. Media architecture

Photos, GIFs, short-form video, and conventional video are core product capabilities. Production media handling should be separated from social metadata so storage and processing can evolve independently.

The intended media pipeline includes:

- authorized upload initiation;
- type, size, and metadata validation;
- Wardveil safety and malicious-file evaluation where applicable;
- privacy-aware metadata stripping or preservation decisions;
- durable object storage through a replaceable storage contract;
- image derivatives and video transcoding;
- thumbnails and poster frames;
- captions, subtitles, alt text, and accessibility metadata;
- streaming delivery and range requests;
- retention, deletion, export, and Everkeep continuity behavior;
- lifecycle cleanup for failed or abandoned uploads.

Production media processing, object storage, CDN behavior, and transcoding are not implemented in the initial foundation.

## 8. Reactions, reposts, and interaction

The interaction model should support ordinary likes as well as a bounded set of reactions such as love, laugh, wow, sad, angry, and support. The available set may later become context-sensitive by space policy, but reactions must remain interoperable and exportable.

Reposts and quote-posts should preserve the relationship to the original content and its current accessibility. Reposting must not create a permanent bypass around later deletion, privacy restriction, moderation removal, or audience changes.

Replies, mentions, hashtags, bookmarks, polls, and sharing are planned but not yet implemented by the initial server API.

## 9. Trust, safety, and moderation

A combined social platform requires safety architecture from the beginning. Planned controls include:

- reporting, blocking, muting, restricting, and community bans;
- comment and reply controls;
- spam, automation, scraping, and rate-abuse controls;
- impersonation and identity-abuse protection;
- malicious link and file handling;
- media-safety evaluation where applicable;
- moderator queues, escalation, evidence, and appeals;
- transparent enforcement state and bounded administrator authority;
- age-appropriate behavior where required by the supported deployment and user population;
- auditability for privileged moderation actions.

The initial foundation implements a report data primitive only. It does not claim production abuse detection or moderation operations.

## 10. GoreeCloud Identity integration

GoreeCloud Identity is the authority for authentication, sessions, trusted devices, application/service identities, and actor authorization.

GoreeCloud Social must not create a second authoritative credential store. The Social database may own application-specific profile information and social relationships, but the `identity_subject` field is a reference to the external authoritative identity.

Future integration must define scopes for profile management, publishing, moderation, group/community administration, automation, service identities, and delegated moderation. Public write APIs must remain unavailable until an accepted authority model exists.

## 11. Privacy Shield integration

Privacy Shield must govern profile visibility, audience selection, contact discovery, recommendation signals, activity history, location, analytics, media metadata, retention, deletion, export, external disclosure, and cross-application data movement.

Recommendation and analytics data require explicit data-purpose definitions. GoreeCloud Social must not treat authentication as consent or platform-internal data availability as permission to process that data for unrelated ranking or analytics.

The initial foundation performs no contact ingestion, behavioral profiling, location collection, advertising tracking, or third-party disclosure. Privacy Shield integration and acceptance remain blocked.

## 12. Wardveil Security integration

Wardveil Security must protect account/session operations, privileged moderation, API use, automation, uploads, malicious links/files, service communication, and security-sensitive administration.

The initial server uses bounded read-only health/status routes and deliberately avoids unauthenticated social write routes. This is local Development hardening only; it is not Wardveil integration or acceptance.

## 13. GoreeCloud Mesh integration

GoreeCloud Mesh is the intended coordination layer for replaceable integrations and event distribution. Planned Social capabilities include:

- notifications through the shared notification architecture;
- sharing posts, videos, profiles, groups, or communities to GoreeCloud Messenger when authorized;
- optional people discovery through GoreeCloud Contacts when authorized by Privacy Shield and Identity;
- media/file capability use through documented contracts;
- Universal Search registration and deep links;
- event publication for bounded social-domain changes;
- capability discovery without treating discovery as authorization.

No Mesh runtime integration is implemented by the initial foundation.

## 14. Everkeep continuity

Important social configuration, posts, permitted media, relationships, groups/communities, moderation records, and required application state need defined backup, restore, migration, and export behavior.

Continuity must respect Privacy Shield retention and deletion. A deleted post must not silently become permanently retained merely because backup exists. Recovery must preserve Identity and Wardveil protection rather than becoming an alternate authorization path.

Everkeep integration and restore acceptance remain blocked.

## 15. GoreeCloud Manager

GoreeCloud Manager should eventually expose bounded operational state such as version, lifecycle, health, dependency status, platform-conformance status, moderation-service health, media-processing health, and maintenance state. It must not become the source of social identity, privacy policy, or moderation authority merely because it can display or invoke administrative workflows.

The initial status endpoint provides bounded source identity for later management integration. No Manager integration is currently implemented.

## 16. Glaze UI

All user-facing Social surfaces must use the current Stable Glaze UI consumer baseline and pass application-specific visual, responsive, touch, keyboard, reduced-motion, contrast, text-scaling, screen-reader, and platform acceptance before Stable eligibility.

The initial repository contains a responsive, accessible development shell that establishes information architecture only. It does not claim Glaze UI 1.1.0 conformance or acceptance.

Primary mobile navigation is intended to center on Home, Discover, Create, Communities, and Profile, with notification and Messenger access available through shared GoreeCloud surfaces. Larger displays may expand to a multi-column layout while preserving the same information architecture.

## 17. API and service boundaries

The initial API version is `v1`. The first implemented routes are intentionally read-only:

- `/livez/` — process liveness;
- `/readyz/` — database-aware readiness;
- `/api/v1/status/` — bounded product and development capability status.

Future APIs must use scoped authorization, versioned contracts, request identifiers, bounded pagination, validation, idempotency where appropriate, rate controls, documented errors, and explicit privacy behavior.

Direct cross-application database access is not an accepted integration method.

## 18. Initial deployment and clients

The first implementation is a self-hosted web/server development foundation on Linux, with a responsive web interface. Long-term client targets may include PWA/web, Android, iOS, and desktop where a dedicated client adds value.

Mobile and desktop clients should share authoritative APIs and platform contracts while preserving platform-appropriate interaction behavior. Offline support must distinguish drafts/cached content from authoritative synchronized social state.

Production database, reverse proxy, TLS termination, media storage, background jobs, realtime fan-out, search indexing, recommendation services, notification delivery, and horizontal scalability are not established by the initial foundation.

## 19. Current implementation milestone

Milestone 0 establishes the smallest useful native foundation:

- canonical product and repository documentation;
- Platform Contract v0.2 participation;
- Django development server;
- liveness/readiness/source-status routes;
- social profile, group/community, membership, follow, post, media-reference, reaction, repost, and report models;
- read-side audience visibility service;
- responsive development UI shell;
- tests and continuous integration;
- explicit documentation of security, privacy, continuity, and platform-integration blockers.

This milestone is Development source only. It does not establish public availability, Stable qualification, production safety, platform-system acceptance, or production readiness.

## 20. Roadmap

Subsequent milestones should prioritize, in order:

1. accepted GoreeCloud Identity authentication and scoped authorization;
2. Privacy Shield data-category, purpose, retention, recommendation, disclosure, and deletion contracts;
3. Wardveil API, session, upload, abuse, and privileged-action protections;
4. authorized publishing/reply/reaction/repost APIs with concurrency and idempotency controls;
5. production media upload, processing, storage, export, and deletion architecture;
6. moderation workflows, blocks, mutes, rate controls, anti-spam, appeals, and evidence;
7. Following/chronological feeds before opaque recommendation ranking;
8. controlled Discover/Video recommendation systems with user-facing transparency controls;
9. Mesh notifications, Messenger sharing, Contacts discovery, Universal Search, and events;
10. Everkeep backup/restore/export acceptance and production deployment qualification;
11. dedicated client applications when justified by the shared client strategy.
