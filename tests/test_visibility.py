from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from social.models import Block, Follow, Mute, Post, SocialProfile, Space, SpaceBan, SpaceMembership
from social.services import visible_posts_for


class VisibilityTests(TestCase):
    def setUp(self):
        self.viewer = SocialProfile.objects.create(identity_subject="identity:viewer", handle="viewer", display_name="Viewer")
        self.followed = SocialProfile.objects.create(identity_subject="identity:followed", handle="followed", display_name="Followed")
        self.mutual = SocialProfile.objects.create(identity_subject="identity:mutual", handle="mutual", display_name="Mutual")
        self.space_author = SocialProfile.objects.create(identity_subject="identity:space", handle="space_author", display_name="Space Author")
        self.other = SocialProfile.objects.create(identity_subject="identity:other", handle="other_user", display_name="Other")
        Follow.objects.create(follower=self.viewer, followed=self.followed, state=Follow.State.ACCEPTED)
        Follow.objects.create(follower=self.viewer, followed=self.mutual, state=Follow.State.ACCEPTED)
        Follow.objects.create(follower=self.mutual, followed=self.viewer, state=Follow.State.ACCEPTED)
        self.space = Space.objects.create(kind=Space.Kind.COMMUNITY, slug="foundation", name="Foundation", owner=self.space_author)
        SpaceMembership.objects.create(space=self.space, profile=self.viewer, state=SpaceMembership.State.ACCEPTED)
        self.public = Post.objects.create(author=self.other, body="public", audience=Post.Audience.PUBLIC)
        self.followers = Post.objects.create(author=self.followed, body="followers", audience=Post.Audience.FOLLOWERS)
        self.friends = Post.objects.create(author=self.mutual, body="friends", audience=Post.Audience.FRIENDS)
        self.space_post = Post.objects.create(author=self.space_author, space=self.space, body="space", audience=Post.Audience.SPACE)
        self.only_me = Post.objects.create(author=self.other, body="private", audience=Post.Audience.ONLY_ME)
        self.own_private = Post.objects.create(author=self.viewer, body="own", audience=Post.Audience.ONLY_ME)
        self.removed = Post.objects.create(author=self.other, body="removed", audience=Post.Audience.PUBLIC, moderation_state=Post.ModerationState.REMOVED)

    def test_profile_visibility(self):
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertTrue({self.public.id, self.followers.id, self.friends.id, self.space_post.id, self.own_private.id}.issubset(ids))
        self.assertNotIn(self.only_me.id, ids)
        self.assertNotIn(self.removed.id, ids)

    def test_anonymous_visibility_is_public_only(self):
        ids = set(visible_posts_for(None).values_list("id", flat=True))
        self.assertEqual(ids, {self.public.id})

    def test_viewer_block_hides_blocked_author(self):
        Block.objects.create(blocker=self.viewer, blocked=self.other)
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertNotIn(self.public.id, ids)

    def test_inbound_block_hides_blocking_author(self):
        Block.objects.create(blocker=self.followed, blocked=self.viewer)
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertNotIn(self.followers.id, ids)

    def test_viewer_mute_hides_muted_author(self):
        Mute.objects.create(muter=self.viewer, muted=self.mutual)
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertNotIn(self.friends.id, ids)

    def test_blocked_space_author_is_hidden_even_when_viewer_is_member(self):
        Block.objects.create(blocker=self.viewer, blocked=self.space_author)
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertNotIn(self.space_post.id, ids)

    def test_active_space_ban_hides_protected_space_post(self):
        SpaceBan.objects.create(
            space=self.space,
            profile=self.viewer,
            imposed_by_subject="identity:moderator",
        )
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertNotIn(self.space_post.id, ids)
        self.assertIn(self.public.id, ids)

    def test_expired_space_ban_does_not_hide_protected_space_post(self):
        SpaceBan.objects.create(
            space=self.space,
            profile=self.viewer,
            imposed_by_subject="identity:moderator",
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertIn(self.space_post.id, ids)

    def test_revoked_space_ban_does_not_hide_protected_space_post(self):
        SpaceBan.objects.create(
            space=self.space,
            profile=self.viewer,
            imposed_by_subject="identity:moderator",
            state=SpaceBan.State.REVOKED,
        )
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertIn(self.space_post.id, ids)

    def test_safety_filters_do_not_hide_viewers_own_private_posts(self):
        Block.objects.create(blocker=self.viewer, blocked=self.other)
        Mute.objects.create(muter=self.viewer, muted=self.mutual)
        ids = set(visible_posts_for(self.viewer).values_list("id", flat=True))
        self.assertIn(self.own_private.id, ids)
