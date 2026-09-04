from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from social.models import Follow, Post, Reaction, SocialProfile


class ModelConstraintTests(TestCase):
    def setUp(self):
        self.a = SocialProfile.objects.create(identity_subject="identity:a", handle="alpha", display_name="Alpha")
        self.b = SocialProfile.objects.create(identity_subject="identity:b", handle="bravo", display_name="Bravo")

    def test_follow_cannot_target_self(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Follow.objects.create(follower=self.a, followed=self.a, state=Follow.State.ACCEPTED)

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
