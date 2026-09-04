from django.test import TestCase

from social.models import Follow, Post, SocialProfile, Space, SpaceMembership
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
