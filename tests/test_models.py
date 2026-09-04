from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from social.models import (
    Block,
    Bookmark,
    Follow,
    Mute,
    Poll,
    PollOption,
    PollVote,
    Post,
    ProfileCollection,
    ProfileCollectionMember,
    Reaction,
    SocialProfile,
    Space,
    SpaceInvitation,
    SpaceJoinRequest,
    SpaceMembership,
    SpaceRule,
)


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

    def test_profile_collection_name_is_unique_per_owner_and_kind(self):
        ProfileCollection.objects.create(owner=self.a, kind=ProfileCollection.Kind.LIST, name="Close friends")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProfileCollection.objects.create(owner=self.a, kind=ProfileCollection.Kind.LIST, name="Close friends")

    def test_profile_collection_name_can_repeat_across_collection_kinds(self):
        ProfileCollection.objects.create(owner=self.a, kind=ProfileCollection.Kind.LIST, name="Close friends")
        circle = ProfileCollection.objects.create(owner=self.a, kind=ProfileCollection.Kind.CIRCLE, name="Close friends")
        self.assertEqual(circle.kind, ProfileCollection.Kind.CIRCLE)

    def test_profile_collection_member_is_unique(self):
        collection = ProfileCollection.objects.create(owner=self.a, kind=ProfileCollection.Kind.CIRCLE, name="Family")
        ProfileCollectionMember.objects.create(collection=collection, profile=self.b)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProfileCollectionMember.objects.create(collection=collection, profile=self.b)

    def test_space_rule_position_is_unique_within_space(self):
        space = Space.objects.create(kind=Space.Kind.COMMUNITY, slug="rules-space", name="Rules", owner=self.a)
        SpaceRule.objects.create(space=space, title="Be kind", position=0)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SpaceRule.objects.create(space=space, title="Stay on topic", position=0)

    def test_space_invitation_cannot_target_inviter(self):
        space = Space.objects.create(kind=Space.Kind.GROUP, slug="invite-self", name="Invite Self", owner=self.a)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SpaceInvitation.objects.create(space=space, inviter=self.a, invitee=self.a)

    def test_space_invitation_is_unique_per_space_and_invitee(self):
        space = Space.objects.create(kind=Space.Kind.GROUP, slug="invite-unique", name="Invite Unique", owner=self.a)
        SpaceInvitation.objects.create(space=space, inviter=self.a, invitee=self.b)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SpaceInvitation.objects.create(space=space, inviter=self.a, invitee=self.b)

    def test_space_invitation_rejects_accepted_member(self):
        space = Space.objects.create(kind=Space.Kind.GROUP, slug="invite-member", name="Invite Member", owner=self.a)
        SpaceMembership.objects.create(space=space, profile=self.b, state=SpaceMembership.State.ACCEPTED)
        invitation = SpaceInvitation(space=space, inviter=self.a, invitee=self.b)
        with self.assertRaises(ValidationError):
            invitation.full_clean()

    def test_space_join_request_is_unique_per_space_and_requester(self):
        space = Space.objects.create(kind=Space.Kind.COMMUNITY, slug="request-unique", name="Request Unique", owner=self.a)
        SpaceJoinRequest.objects.create(space=space, requester=self.b)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SpaceJoinRequest.objects.create(space=space, requester=self.b)

    def test_space_join_request_rejects_accepted_member(self):
        space = Space.objects.create(kind=Space.Kind.COMMUNITY, slug="request-member", name="Request Member", owner=self.a)
        SpaceMembership.objects.create(space=space, profile=self.b, state=SpaceMembership.State.ACCEPTED)
        request = SpaceJoinRequest(space=space, requester=self.b)
        with self.assertRaises(ValidationError):
            request.full_clean()

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

    def test_reply_cannot_target_itself(self):
        post = Post.objects.create(author=self.a, body="root")
        post.reply_to = post
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_reply_must_remain_in_parent_space_scope(self):
        first = Space.objects.create(kind=Space.Kind.COMMUNITY, slug="first-space", name="First", owner=self.a)
        second = Space.objects.create(kind=Space.Kind.COMMUNITY, slug="second-space", name="Second", owner=self.a)
        parent = Post.objects.create(author=self.a, space=first, body="parent", audience=Post.Audience.SPACE)
        reply = Post(author=self.b, space=second, reply_to=parent, body="reply", audience=Post.Audience.SPACE)
        with self.assertRaises(ValidationError):
            reply.full_clean()

    def test_bookmark_relationship_is_unique(self):
        post = Post.objects.create(author=self.b, body="bookmark me")
        Bookmark.objects.create(profile=self.a, post=post)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Bookmark.objects.create(profile=self.a, post=post)

    def test_poll_requires_poll_content_kind(self):
        post = Post.objects.create(author=self.a, body="not a poll")
        poll = Poll(post=post, question="Choose one")
        with self.assertRaises(ValidationError):
            poll.full_clean()

    def test_poll_option_position_is_unique_within_poll(self):
        post = Post.objects.create(author=self.a, content_kind=Post.ContentKind.POLL)
        poll = Poll.objects.create(post=post, question="Choose one")
        PollOption.objects.create(poll=poll, text="One", position=0)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PollOption.objects.create(poll=poll, text="Two", position=0)

    def test_single_choice_poll_allows_one_vote_per_voter(self):
        post = Post.objects.create(author=self.a, content_kind=Post.ContentKind.POLL)
        poll = Poll.objects.create(post=post, question="Choose one")
        first = PollOption.objects.create(poll=poll, text="One", position=0)
        second = PollOption.objects.create(poll=poll, text="Two", position=1)
        PollVote.objects.create(poll=poll, option=first, voter=self.b)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PollVote.objects.create(poll=poll, option=second, voter=self.b)

    def test_poll_vote_option_must_belong_to_selected_poll(self):
        first_post = Post.objects.create(author=self.a, content_kind=Post.ContentKind.POLL)
        second_post = Post.objects.create(author=self.a, content_kind=Post.ContentKind.POLL)
        first_poll = Poll.objects.create(post=first_post, question="First")
        second_poll = Poll.objects.create(post=second_post, question="Second")
        wrong_option = PollOption.objects.create(poll=second_poll, text="Wrong", position=0)
        vote = PollVote(poll=first_poll, option=wrong_option, voter=self.b)
        with self.assertRaises(ValidationError):
            vote.full_clean()
