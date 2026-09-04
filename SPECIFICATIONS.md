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

## 3. Unified content and social-domain model

GoreeCloud Social uses versioned domain models with presentation-specific surfaces rather than unrelated systems for each social experience.

A post may contain text and zero or more typed media attachments. Presentation can adapt by surface: a text-focused conversation card in Home, a media card in a profile, an immersive vertical player in Video, or a community-scoped post in a group. The underlying authority, audience, moderation state, and identity relationship remain consistent.

The native Development foundation implements the following domain primitives:

- `SocialProfile`: application-owned social profile metadata linked to an external GoreeCloud Identity subject;
- `ProfileCollection`: an owner-curated List or Circle record;
- `ProfileCollectionMember`: unique profile membership within a profile collection;
- `Space`: a group or community with visibility and an owning social profile;
- `SpaceMembership`: member, moderator, administrator, or owner role and membership state;
- `SpaceInvitation`: explicit invitation intent from an inviter to an invitee for a space;
- `SpaceJoinRequest`: explicit profile-initiated request to join a space;
- `SpaceRule`: ordered active/inactive rule metadata scoped to a space;
- `Follow`: directional social relationship with a pending/accepted state and a no-self-follow invariant;
- `Block`: bilateral read-safety relationship from a blocking profile to a blocked profile, with uniqueness and no-self-block invariants;
- `Mute`: viewer-selected read-safety relationship from a muting profile to a muted profile, with uniqueness and no-self-mute invariants;
- `Restrict`: directional relationship-safety groundwork with uniqueness and no-self-target invariants;
- `Post`: author, optional space, optional parent-reply relationship, content type, audience, reply policy, moderation state, body, and timestamps;
- `MediaAttachment`: ordered photo, video, or GIF reference plus accessibility alternative text;
- `Poll`: one single-choice poll definition attached to a poll-kind post;
- `PollOption`: ordered poll option with unique position inside its poll;
- `PollVote`: one selected option per voter/poll, with application validation that the option belongs to the poll;
- `Reaction`: one typed reaction from a profile to a post;
- `Bookmark`: a private profile/post relationship with one bookmark per profile/post;
- `Repost`: a repost or quote-repost relationship;
- `PostReport`: a post-report allegation record for later moderation workflows;
- `ProfileReport`: a profile-report allegation record with no-self-report enforcement;
- `SpaceBan`: a space-local enforcement record with active, revoked, or expired state and optional expiration;
- `ModerationCase`: a post- or profile-targeted internal moderation case record;
- `ModerationAction`: an attributable record of an internal moderation action associated with a case;
- `ModerationAppeal`: a per-appellant case appeal record with explicit review lifecycle state.

The current code intentionally stores media references rather than implementing production upload, scanning, transcoding, object storage, or CDN behavior. Profile collections, invitations, join requests, rules, replies, polls, bookmarks, restrictions, reports, bans, cases, actions, and appeals are Development domain groundwork only and are not public mutation APIs.

## 4. Audience and social graph

Audience evaluation is a first-class authorization concern, not merely a user-interface filter.

The foundation implements read-side visibility semantics for:

- `public` — visible without a social profile;
- `followers` — visible to accepted followers of the author;
- `friends` — visible to mutual accepted follow relationships;
- `space` — visible to accepted members of the associated group or community when no active non-expired space ban denies the protected membership path;
- `only-me` — visible only to the author.

An author can always retrieve their own visible-state posts through the application visibility service. Removed, limited, and pending-moderation states are excluded from ordinary visibility queries.

For an identified viewer, ordinary read visibility also excludes posts whose author is blocked by the viewer, posts whose author has blocked the viewer, and posts whose author is muted by the viewer. Blocking therefore acts bilaterally at this read boundary, while muting is viewer-selected. These relationships are enforced server-side in the visibility service rather than treated as cosmetic client filtering.

The Development visibility service also excludes an actively banned viewer's space from the accepted-membership set used to authorize protected `space`-audience posts. An active ban whose `expires_at` is in the past, or a ban explicitly marked revoked/expired, does not deny that membership path. This bounded rule does not constitute a complete community enforcement engine or public ban-management workflow.

Accepted mutual relationships are derived from reciprocal accepted follows. Profile collections do not create follow or mutual relationships. The current List/Circle records are internal collection groundwork; custom audience evaluation from Circle membership is not yet implemented by the visibility service.

Future custom audiences, broader restrictions, legal restrictions, age policy, richer community enforcement, role-capability policy, and Privacy Shield controls must be composed into the authoritative visibility decision rather than applied as cosmetic client-side filtering.

## 5. Feeds and discovery

GoreeCloud Social should provide distinct user-selectable feed modes rather than hiding all behavior behind one opaque ranking system.

Feed families include:

- Following — content from accepted followed profiles, joined spaces, and the viewer's own eligible posts;
- Chronological — time-ordered eligible content with no recommendation ranking;
- Discover / For You — recommendation-driven discovery with user-understandable controls;
- Communities and Groups — scoped social spaces;
- Video — immersive short-form video plus a Following video mode;
- Media — optional photo/video browsing surfaces;
- Trending — only if a privacy-preserving and abuse-resistant definition is established.

The Development source implements internal Following and Chronological query read models. Both compose on top of the authoritative visibility service so audience, moderation, bilateral block, viewer-selected mute, and protected space-ban behavior is not duplicated or bypassed. The Following read model admits the viewer's own eligible posts, eligible posts from accepted follows, and eligible posts in spaces where the viewer has accepted membership and is not actively banned under the current bounded rule. Anonymous callers have no personalized Following feed. Chronological uses the same eligibility boundary and returns eligible posts in reverse chronological order.

These query services are not public personalized feed endpoints and do not establish production feed delivery, authenticated pagination, client synchronization, or Stable behavior. Public personalized feed APIs remain blocked until GoreeCloud Identity authorization, Privacy Shield policy, Wardveil protections, API pagination/compatibility requirements, and abuse/resource controls are accepted for the interface.

Recommendation systems must expose enough information for users to understand why material is shown, reduce topics or signals, reset recommendations, and choose less-personalized or chronological behavior where supported. Engagement collection must not automatically become unrestricted profiling.

The current foundation does not implement recommendation ranking or behavioral profiling.

## 6. Profiles, lists, groups, and communities

Groups and communities are first-class social spaces, not tags around ordinary posts. Owner-curated Lists and Circles are separate profile collections and do not create community membership or global social relationships.

A space can be public, private, or invitation-only. The Development domain includes explicit `SpaceInvitation`, `SpaceJoinRequest`, ordered `SpaceRule`, and `SpaceBan` records in addition to `SpaceMembership`. Invitation validation rejects an invitee who is already an accepted member. Join-request validation rejects a requester who is already an accepted member. Database constraints prevent duplicate current records under the current Development model, prevent self-invitations, keep rule positions unique within a space, and keep one current `SpaceBan` row per space/profile.

These records are structural groundwork, not completed community workflows. Public invitation, join-request, list/circle, rule-management, role-management, ownership-transfer, membership-approval, ban-management, or moderation APIs do not exist. The current source does not claim that a moderator/admin role label, `imposed_by_subject`, `opened_by_subject`, or `actor_subject` field proves authorization for a privileged action.

Future policy should support explicit role capabilities, moderator teams, pinned content, announcements, richer bans/restrictions, content approval, moderation queues, rule acknowledgement, ownership transfer, and scoped discovery. Administrative capability inside a space does not grant platform-wide authority. Community delegation must use GoreeCloud Identity-scoped authority when implemented, and moderator actions must remain auditable and subject to Wardveil and Privacy Shield requirements.

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

Production media processing, object storage, CDN behavior, scanning, and transcoding are not implemented in the current foundation.

## 8. Reactions, replies, polls, bookmarks, reposts, and interaction

The interaction model supports ordinary likes as well as a bounded set of reactions such as love, laugh, wow, sad, angry, and support. The available set may later become context-sensitive by space policy, but reactions must remain interoperable and exportable.

Replies are represented as posts with an explicit parent relationship. Development validation prevents self-replies and prevents a reply from changing the parent post's space scope. This is structural groundwork only; authenticated reply creation must later enforce the parent's current visibility, reply policy, block/mute/restrict state, community rules and bans, Identity authority, Wardveil protections, and Privacy Shield requirements.

Bookmarks are private profile-owned post relationships with a uniqueness constraint per profile/post. They are not a public engagement signal by default. The current source does not expose bookmark mutation or listing APIs.

Single-choice poll groundwork consists of one `Poll` per poll-kind post, ordered `PollOption` records, and `PollVote` records constrained to one vote per voter/poll. Model validation rejects a poll attached to a non-poll post and rejects a vote whose option belongs to another poll. Public poll creation/voting APIs, close-time enforcement, results visibility, minimum-option validation at creation time, and any later multiple-choice extension remain planned.

Reposts and quote-posts preserve the relationship to the original content and its current accessibility. Reposting must not create a permanent bypass around later deletion, privacy restriction, moderation removal, or audience changes.

Structured mentions, hashtags, authenticated sharing, and public reply/bookmark/poll workflows remain planned. None of the Development domain records create unauthenticated write endpoints.

## 9. Trust, safety, and moderation

A combined social platform requires safety architecture from the beginning. Required controls include:

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

The Development foundation implements post/profile report, block, mute, restrict, space-ban, moderation-case/action, and appeal data primitives. Ordinary read visibility enforces bilateral blocks, viewer-selected mutes, and active non-expired space bans for protected space-audience membership reads. Post moderation state continues to exclude limited, pending, and removed content from ordinary visibility.

A report is an allegation record, not a verdict. `imposed_by_subject`, `opened_by_subject`, and `actor_subject` are attributable opaque references only; they do not prove that the referenced actor was authorized. The source does not expose public mutation APIs for these records and does not claim production anti-spam, report-rate controls, automation/bot detection, scraping defenses, impersonation workflows, malicious-link/file/media protection, age-eligibility controls, mature moderation, or accepted GoreeCloud Identity, Privacy Shield, or Wardveil Security integration.

## 10. GoreeCloud Identity integration

GoreeCloud Identity is the authority for authentication, sessions, trusted devices, application/service identities, and actor authorization.

GoreeCloud Social must not create a second authoritative credential store. The Social database may own application-specific profile information, profile collections, social relationships, community state, and moderation state, but the `identity_subject` field and bounded moderation actor-subject fields reference external authoritative identities rather than creating credentials or authorization grants.

Future integration must define scopes for profile management, list/circle management, following, invitations, join requests, membership and rule administration, publishing, replies, reactions, polls, bookmarks, restriction/report/ban management, moderation case/action/appeal workflows, group/community administration, automation, service identities, and delegated moderation. Public write APIs and personalized feed APIs must remain unavailable until an accepted authority model exists.

## 11. Privacy Shield integration

Privacy Shield must govern profile visibility, audience selection, list/circle data, invitations and join requests, community membership, reports, moderation cases/evidence, restrictions and bans, contact discovery, recommendation signals, activity history, location, analytics, media metadata, retention, deletion, export, external disclosure, and cross-application data movement.

Recommendation, analytics, and moderation-evidence data require explicit data-purpose definitions. GoreeCloud Social must not treat authentication, a submitted report, or platform-internal data availability as permission to process data for unrelated ranking, analytics, or indefinite evidence retention.

The current foundation performs no contact ingestion, behavioral profiling, location collection, advertising tracking, or third-party disclosure. Safety/moderation records remain local Development domain state and do not constitute Privacy Shield integration or acceptance. Reporter details, report text, private content, and moderation evidence must not be exposed through ordinary status, search, feed, analytics, or logging surfaces merely because the records exist.

## 12. Wardveil Security integration

Wardveil Security must protect account/session operations, privileged moderation, API use, automation, uploads, malicious links/files, service communication, and security-sensitive administration.

The Development server uses bounded read-only health/status routes and deliberately avoids unauthenticated social write, moderation-write, and personalized-feed routes. Relationship-safety, feed, social-collection/community-workflow, threaded-reply, bookmark, poll, reporting, ban, moderation-case/action, and appeal state are currently exercised through internal domain/query services only. Active space-ban read enforcement is Social application logic, not Wardveil acceptance.

No Wardveil runtime adapter, malicious-link/file/media evaluation, privileged-action enforcement contract, security evidence acceptance, or production safety qualification is implemented by this milestone. Passing source CI does not establish Wardveil Security integration or acceptance.

## 13. GoreeCloud Mesh integration

GoreeCloud Mesh is the intended coordination layer for replaceable integrations and event distribution. Planned Social capabilities include:

- notifications through the shared notification architecture;
- sharing posts, videos, profiles, groups, or communities to GoreeCloud Messenger when authorized;
- optional people discovery through GoreeCloud Contacts when authorized by Privacy Shield and Identity;
- media/file capability use through documented contracts;
- Universal Search registration and deep links;
- event publication for bounded social-domain changes;
- capability discovery without treating discovery as authorization.

No Mesh runtime integration is implemented by the current foundation. Future moderation or safety events must be minimized and must not distribute unrestricted report/evidence content to consumers.

## 14. Everkeep continuity

Important social configuration, posts, permitted media, thread relationships, user-owned bookmarks, poll structure and permitted vote state, profile collections, follow/block/mute/restrict state, spaces, memberships, invitations, join requests, rules, bans, reports, moderation cases/actions/appeals, and required application state need defined backup, restore, migration, and export behavior.

Continuity must respect Privacy Shield retention and deletion. A deleted post, relationship, invitation, report, moderation-evidence item, or private collection must not silently become permanently retained merely because backup exists. Recovery must preserve Identity and Wardveil protection rather than becoming an alternate authorization path. Restored moderation state must be reconciled with current retention/deletion policy and must not recreate ordinary visibility.

Everkeep integration and restore acceptance remain blocked.

## 15. GoreeCloud Manager

GoreeCloud Manager should eventually expose bounded operational state such as version, lifecycle, health, dependency status, platform-conformance status, moderation-service health, media-processing health, and maintenance state. It must not become the source of social identity, privacy policy, relationship authority, community authority, or moderation authority merely because it can display or invoke administrative workflows.

The status endpoint provides bounded source identity for later management integration. No Manager moderation workflow or application integration is currently implemented.

## 16. Glaze UI

All user-facing Social surfaces must use the current Stable Glaze UI consumer baseline and pass application-specific visual, responsive, touch, keyboard, reduced-motion, contrast, text-scaling, screen-reader, and platform acceptance before Stable eligibility.

The repository contains a responsive, accessible development shell that establishes information architecture only. It does not claim Glaze UI 1.1.0 conformance or acceptance.

Primary mobile navigation is intended to center on Home, Discover, Create, Communities, and Profile, with notification and Messenger access available through shared GoreeCloud surfaces. Larger displays may expand to a multi-column layout while preserving the same information architecture.

## 17. API and service boundaries

The initial API version is `v1`. The implemented HTTP routes remain intentionally bounded and read-only:

- `/livez/` — process liveness;
- `/readyz/` — database-aware readiness;
- `/api/v1/status/` — bounded product and Development capability status.

Following and Chronological are internal query services, not HTTP feed APIs. Profile collections, space invitations, join requests, rules, threaded replies, bookmarks, polls, poll votes, restrict relationships, profile reports, space bans, moderation cases/actions, and appeals are internal domain records, not public mutation APIs.

Future APIs must use scoped authorization, versioned contracts, request identifiers, bounded pagination, validation, idempotency where appropriate, rate/resource controls, documented errors, explicit privacy behavior, exact role/capability checks for community administration, and proportionate Wardveil protection for sensitive actions.

Direct cross-application database access is not an accepted integration method.

## 18. Initial deployment and clients

The first implementation is a self-hosted web/server Development foundation on Linux, with a responsive web interface. Long-term client targets may include PWA/web, Android, iOS, and desktop where a dedicated client adds value.

Mobile and desktop clients should share authoritative APIs and platform contracts while preserving platform-appropriate interaction behavior. Offline support must distinguish drafts/cached content from authoritative synchronized social state. Client-local moderation or relationship labels must never substitute for current server authorization or enforcement state.

Production database, reverse proxy, TLS termination, media storage, background jobs, realtime fan-out, search indexing, recommendation services, notification delivery, abuse-control infrastructure, and horizontal scalability are not established by the current foundation.

## 19. Current implementation milestones

Milestone 0 established the smallest useful native foundation:

- canonical product and repository documentation;
- Platform Contract v0.2 participation;
- Django Development server;
- liveness/readiness/source-status routes;
- social profile, group/community, membership, follow, post, media-reference, reaction, repost, and report models;
- read-side audience visibility service;
- responsive Development UI shell;
- tests and continuous integration;
- explicit documentation of security, privacy, continuity, and platform-integration blockers.

Milestone 1 relationship-safety groundwork added:

- `Block` and `Mute` domain records with database uniqueness and self-target prevention;
- bilateral block enforcement in ordinary server-side read visibility;
- viewer-selected mute enforcement in ordinary server-side read visibility;
- regression coverage for public, follower, mutual, space, and private-to-self visibility behavior under block/mute relationships;
- Development capability/status and documentation updates without opening unauthenticated mutation APIs.

Milestone 2 feed-read groundwork added:

- an internal `chronological_feed_for` query service that returns eligible posts in reverse chronological order;
- an internal `following_feed_for` query service limited to the viewer, accepted follows, and accepted joined spaces;
- composition on the existing visibility boundary so feed reads inherit audience, moderation, bilateral block, and viewer-selected mute enforcement;
- regression tests for feed source selection, safety filtering, anonymous behavior, and chronological ordering;
- Development version and source-status updates without exposing a personalized public feed API.

Milestone 3 content-interaction groundwork added:

- explicit parent-reply relationships on posts with self-reply and cross-space validation;
- a `poll` post kind plus `Poll`, ordered `PollOption`, and single-choice `PollVote` records;
- one-vote-per-profile/poll uniqueness and option-to-poll validation;
- private `Bookmark` records with profile/post uniqueness;
- migration `0003_content_interactions` and regression coverage for the new invariants;
- Development version and source-status updates without opening public reply, bookmark, poll, or vote mutation APIs.

Milestone 4 social-graph/community groundwork added:

- owner-curated `ProfileCollection` records typed as List or Circle, with unique owner/kind/name combinations;
- `ProfileCollectionMember` with unique profile membership per collection;
- explicit `SpaceInvitation` records with lifecycle state, no-self-invitation protection, and accepted-member validation;
- explicit `SpaceJoinRequest` records with lifecycle state and accepted-member validation;
- ordered `SpaceRule` records with active state and unique position per space;
- migration `0004_social_graph_community` and regression coverage for the new invariants;
- Development version and bounded source-status updates without opening public collection, invitation, join-request, rule, role, or membership mutation APIs.

Milestone 5 trust-and-safety groundwork adds:

- directional `Restrict` records with uniqueness and self-target prevention;
- `ProfileReport` allegation records with no-self-report enforcement while retaining the existing `PostReport` primitive;
- `SpaceBan` records with active/revoked/expired lifecycle state, optional expiration, and one row per space/profile under the current Development model;
- `ModerationCase` records constrained to exactly one post or profile target, with optional space-context validation;
- attributable `ModerationAction` records and per-appellant `ModerationAppeal` records with explicit lifecycle state;
- active non-expired space-ban enforcement at the authoritative protected space-audience membership-read boundary and inherited Following/Chronological feed behavior;
- migration `0005_trust_safety_groundwork` and regression coverage for domain invariants and bounded read enforcement;
- Development capability/status and documentation updates without exposing public safety/moderation mutation APIs or claiming production anti-spam, rate controls, impersonation handling, malicious-media protection, age controls, or platform-system acceptance.

These milestones are Development source only. They do not establish public availability, Stable qualification, production safety, platform-system acceptance, or production readiness.

## 20. Roadmap

Subsequent milestones should prioritize, in order:

1. accepted GoreeCloud Identity authentication and scoped authorization;
2. Privacy Shield data-category, purpose, retention, recommendation, relationship/community/moderation-evidence disclosure, and deletion contracts;
3. Wardveil API, session, upload, abuse, malicious-link/file/media, and privileged-action protections;
4. authorized profile/follow/collection/community/publishing/reply/reaction/repost/bookmark/poll/safety/moderation APIs with exact role-capability checks, concurrency controls, and idempotency where needed;
5. production media upload, processing, storage, export, and deletion architecture;
6. mature moderation workflows, report-rate controls, restrictions, community bans, anti-spam, automation/bot controls, impersonation handling, appeals/review operations, and evidence governance;
7. authenticated, paginated Following/Chronological feed APIs and client surfaces using the validated read models;
8. controlled Discover/Video recommendation systems with user-facing transparency controls;
9. Mesh notifications, Messenger sharing, Contacts discovery, Universal Search, and events;
10. Everkeep backup/restore/export acceptance and production deployment qualification;
11. dedicated client applications when justified by the shared client strategy.
