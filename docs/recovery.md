# GoreeCloud Social — Recovery Status

GoreeCloud Social requires recoverability for important configuration, social content, permitted media, relationships, groups/communities, membership state, moderation records, and application metadata.

The foundation does not yet implement Everkeep backup, restore, or export. SQLite is Development/test persistence only and is not an accepted production continuity mechanism.

Production continuity must include:

- documented backup scope;
- clean-environment restore testing;
- recovery of database and permitted media relationships;
- explicit retention/deletion reconciliation with Privacy Shield;
- protected restore authorization through GoreeCloud Identity and Wardveil;
- portable export formats and migration paths;
- evidence that restored application state is usable, not merely that a snapshot exists.
