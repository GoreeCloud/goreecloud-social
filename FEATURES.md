# GoreeCloud Social — Features

## Implemented in the native foundation

- Social profile metadata linked to an external GoreeCloud Identity subject.
- Group and community records with public/private/invite-only visibility.
- Membership roles and states.
- Directional follow relationships with a no-self-follow database constraint.
- Bilateral block relationships and viewer-selected mute relationships with uniqueness and no-self-target constraints.
- Directional restrict records with uniqueness and no-self-target constraints as internal safety-domain groundwork.
- Owner-curated List and Circle collection records plus unique profile membership per collection.
- Explicit space invitation and join-request records with lifecycle states and accepted-member validation groundwork.
- Ordered active/inactive space-rule records with unique positions within each space.
- Posts with typed content, audiences, reply policy, moderation state, optional space scope, and an explicit parent-reply relationship.
- Ordered media references for photos, video, and GIF content.
- Single-choice poll records, ordered poll options, and one-vote-per-profile poll-vote groundwork.
- Private bookmark relationships with one bookmark per profile/post.
- Reactions, reposts/quote text, post-report primitives, and profile-report primitives.
- Space-ban records with active/revoked/expired lifecycle state and bounded actor references.
- Moderation case, moderation action, and appeal records for internal Development workflow groundwork.
- Audience-aware read visibility for public, followers, mutual relationships, spaces, and private-to-self content.
- Ordinary read visibility that excludes authors blocked by the viewer, authors who have blocked the viewer, and authors muted by the viewer.
- Active non-expired space-ban enforcement for protected space-audience reads and space-sourced Following feed content.
- Internal Following and Chronological feed read models that compose on the authoritative visibility boundary instead of duplicating audience or relationship-safety rules.
- Read-only liveness, readiness, and source-status endpoints.
- Responsive Development interface shell.
- Repository CI and Platform Contract v0.2 declaration.

## Planned product capabilities

- Authenticated publishing, editing, reply creation, deletion, bookmark mutation, mentions, hashtags, poll creation/voting, and sharing APIs.
- Richer thread traversal and reply-policy enforcement tied to accepted Identity authorization and abuse controls.
- Poll lifecycle/results policy, minimum-option validation at creation time, and any later multiple-choice mode through an explicit compatible extension.
- Photo galleries, albums, short-form video, full video, captions, subtitles, thumbnails, and transcoding.
- Public feed APIs and client surfaces for Following and Chronological, plus Discover/For You, Communities, Groups, Video, media, and optional Trending experiences.
- Recommendation transparency, topic/signal controls, reset controls, and less-personalized feed options.
- Authenticated private-profile follow-request workflows, list/circle management and custom-audience APIs, and richer profile surfaces.
- Full group/community invitation and join-request workflows, role-capability authorization, ownership transfer, moderator teams, queues, member approvals, bans, announcements, pinned content, and rule-acknowledgement behavior.
- Authenticated restrict, reporting, space-ban, moderation-case/action/appeal, block, and mute mutation workflows with accepted GoreeCloud Identity authorization.
- Production anti-spam, rate/resource controls, bot and automation controls, scraping defenses, impersonation handling, appeals/review operations, and mature moderation evidence.
- Wardveil-integrated malicious-link/file/media protection and privileged-action protection with current evidence; source-only safety records do not establish Wardveil acceptance.
- Privacy Shield-approved moderation/report evidence purposes, access, retention, deletion, export, disclosure, and privacy-safe logging.
- Age-appropriate controls only where required and approved, using minimized eligibility information rather than unnecessary raw age/identity data.
- Notifications, GoreeCloud Messenger sharing, Universal Search, and authorized Contacts discovery through GoreeCloud Mesh.
- Everkeep backup/restore, portable export, migration, and account-transition support.
- Glaze UI 1.1.0 acceptance across responsive web and future dedicated clients.
