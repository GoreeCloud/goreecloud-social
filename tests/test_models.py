from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from social.models import Block, Follow, Mute, Post, Reaction, SocialProfile


class ModelConstraintTests(TestCase):
    def setUp(self):
        self.a = SocialProfile.objects.create(identity_subject="identity:a", handle="alpha", display_name="Alpha")
        self.b = SocialProfile.objects.create(identity_subject="identity:b", handle="bravo", display_name="Bravo")

    def test_follow_cannot_target_self(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Follow.objects.create(follower=self.a, followed=self.a, state=Follow.State.ACCEPTED)

    def test_block_cannot_target_self(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Block.objects.create(blocker=self.a, blocked=self.a)

    def test_mute_cannot_target_self(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Mute.objects.create(muter=self.a, muted=self.a)

    def test_block_relationship_is_unique(self):
        Block.objects.create(blocker=self.a, blocked=self.b)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Block.objects.create(blocker=self.a, blocked=self.b)

    def test_mute_relationship_is_unique(self):
        Mute.objects.create(muter=self.a, muted=self.b)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Mute.objects.create(muter=self.a, muted=self.b)

    def test_one_reaction_per_profile_per_post(self):
        post = Post.objects.create(author=self.b, body="hello")
        Reaction.objects.create(profile=self.a, post=post, kind=Reaction.Kind.LIKE)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reaction.objects.create(profile=self.a, post=post, kind=Reaction.Kind.LOVE)

    def test_space_audience_requires_space(self):
        post = Post(author=self.a, audience=Post.Audience.SPACE, body="scoped")
        with self.assertRaises(ValidationError):
            post.full_clean()
