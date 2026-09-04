from django.test import TestCase

from social.models import Block, Follow, Mute, Post, SocialProfile, Space, SpaceBan, SpaceMembership
from social.services import chronological_feed_for, following_feed_for


class FeedReadModelTests(TestCase):
    def setUp(self):
        self.viewer = SocialProfile.objects.create(
            identity_subject="identity:viewer", handle="viewer_feed", display_name="Viewer"
        )
        self.followed = SocialProfile.objects.create(
            identity_subject="identity:followed", handle="followed_feed", display_name="Followed"
        )
        self.other = SocialProfile.objects.create(
            identity_subject="identity:other", handle="other_feed", display_name="Other"
        )
        self.space_author = SocialProfile.objects.create(
            identity_subject="identity:space", handle="space_feed", display_name="Space Author"
        )
        self.muted = SocialProfile.objects.create(
            identity_subject="identity:muted", handle="muted_feed", display_name="Muted"
        )
        self.blocked = SocialProfile.objects.create(
            identity_subject="identity:blocked", handle="blocked_feed", display_name="Blocked"
        )

        Follow.objects.create(follower=self.viewer, followed=self.followed, state=Follow.State.ACCEPTED)
        Follow.objects.create(follower=self.viewer, followed=self.muted, state=Follow.State.ACCEPTED)
        Follow.objects.create(follower=self.viewer, followed=self.blocked, state=Follow.State.ACCEPTED)

        self.space = Space.objects.create(
            kind=Space.Kind.COMMUNITY,
            slug="feed-foundation",
            name="Feed Foundation",
            owner=self.space_author,
        )
        SpaceMembership.objects.create(
            space=self.space,
            profile=self.viewer,
            state=SpaceMembership.State.ACCEPTED,
        )

        self.unrelated_public = Post.objects.create(
            author=self.other,
            body="unrelated public",
            audience=Post.Audience.PUBLIC,
        )
        self.followed_post = Post.objects.create(
            author=self.followed,
            body="followed",
            audience=Post.Audience.FOLLOWERS,
        )
        self.space_post = Post.objects.create(
            author=self.space_author,
            space=self.space,
            body="space",
            audience=Post.Audience.SPACE,
        )
        self.own_post = Post.objects.create(
            author=self.viewer,
            body="own",
            audience=Post.Audience.ONLY_ME,
        )
        self.muted_post = Post.objects.create(
            author=self.muted,
            body="muted",
            audience=Post.Audience.PUBLIC,
        )
        self.blocked_post = Post.objects.create(
            author=self.blocked,
            body="blocked",
            audience=Post.Audience.PUBLIC,
        )

        Mute.objects.create(muter=self.viewer, muted=self.muted)
        Block.objects.create(blocker=self.viewer, blocked=self.blocked)

    def test_following_feed_contains_only_eligible_following_sources(self):
        ids = list(following_feed_for(self.viewer).values_list("id", flat=True))

        self.assertIn(self.followed_post.id, ids)
        self.assertIn(self.space_post.id, ids)
        self.assertIn(self.own_post.id, ids)
        self.assertNotIn(self.unrelated_public.id, ids)
        self.assertNotIn(self.muted_post.id, ids)
        self.assertNotIn(self.blocked_post.id, ids)

    def test_following_feed_is_reverse_chronological(self):
        ids = list(following_feed_for(self.viewer).values_list("id", flat=True))
        expected = [self.own_post.id, self.space_post.id, self.followed_post.id]
        self.assertEqual(ids, expected)

    def test_active_space_ban_removes_space_source_from_following_feed(self):
        SpaceBan.objects.create(
            space=self.space,
            profile=self.viewer,
            imposed_by_subject="identity:moderator",
        )
        ids = list(following_feed_for(self.viewer).values_list("id", flat=True))

        self.assertIn(self.followed_post.id, ids)
        self.assertIn(self.own_post.id, ids)
        self.assertNotIn(self.space_post.id, ids)

    def test_anonymous_caller_has_no_following_feed(self):
        self.assertFalse(following_feed_for(None).exists())

    def test_chronological_feed_uses_visibility_and_safety_boundary(self):
        ids = list(chronological_feed_for(self.viewer).values_list("id", flat=True))

        self.assertIn(self.unrelated_public.id, ids)
        self.assertIn(self.followed_post.id, ids)
        self.assertIn(self.space_post.id, ids)
        self.assertIn(self.own_post.id, ids)
        self.assertNotIn(self.muted_post.id, ids)
        self.assertNotIn(self.blocked_post.id, ids)

    def test_active_space_ban_applies_to_chronological_feed(self):
        SpaceBan.objects.create(
            space=self.space,
            profile=self.viewer,
            imposed_by_subject="identity:moderator",
        )
        ids = list(chronological_feed_for(self.viewer).values_list("id", flat=True))
        self.assertNotIn(self.space_post.id, ids)

    def test_anonymous_chronological_feed_is_public_only(self):
        ids = set(chronological_feed_for(None).values_list("id", flat=True))
        self.assertEqual(
            ids,
            {self.unrelated_public.id, self.muted_post.id, self.blocked_post.id},
        )
