from django.db.models import Q, QuerySet
from django.utils import timezone

from .models import Block, Follow, Mute, Post, SocialProfile, SpaceBan, SpaceMembership


def _active_banned_space_ids(profile: SocialProfile) -> set[int]:
    return set(
        SpaceBan.objects.filter(profile=profile, state=SpaceBan.State.ACTIVE)
        .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()))
        .values_list("space_id", flat=True)
    )


def visible_posts_for(profile: SocialProfile | None) -> QuerySet[Post]:
    """Return ordinary visible-state posts the supplied social profile may read.

    The Development visibility boundary enforces current audience primitives,
    bilateral blocks, viewer-selected mutes, and active space bans for protected
    space-audience reads. It is not a substitute for future GoreeCloud Identity
    authorization, Privacy Shield policy, age/legal restrictions, or complete
    moderation and community-policy enforcement.
    """

    posts = Post.objects.filter(moderation_state=Post.ModerationState.VISIBLE)
    if profile is None:
        return posts.filter(audience=Post.Audience.PUBLIC).select_related("author", "space")

    blocked_ids = set(Block.objects.filter(blocker=profile).values_list("blocked_id", flat=True))
    blocked_by_ids = set(Block.objects.filter(blocked=profile).values_list("blocker_id", flat=True))
    muted_ids = set(Mute.objects.filter(muter=profile).values_list("muted_id", flat=True))
    excluded_author_ids = blocked_ids | blocked_by_ids | muted_ids

    following_ids = set(
        Follow.objects.filter(follower=profile, state=Follow.State.ACCEPTED).values_list("followed_id", flat=True)
    ) - excluded_author_ids
    follower_ids = set(
        Follow.objects.filter(followed=profile, state=Follow.State.ACCEPTED).values_list("follower_id", flat=True)
    ) - excluded_author_ids
    mutual_ids = following_ids & follower_ids
    banned_space_ids = _active_banned_space_ids(profile)
    space_ids = set(
        SpaceMembership.objects.filter(profile=profile, state=SpaceMembership.State.ACCEPTED).values_list(
            "space_id", flat=True
        )
    ) - banned_space_ids

    return (
        posts.filter(
            Q(audience=Post.Audience.PUBLIC)
            | Q(author=profile)
            | Q(audience=Post.Audience.FOLLOWERS, author_id__in=following_ids)
            | Q(audience=Post.Audience.FRIENDS, author_id__in=mutual_ids)
            | Q(audience=Post.Audience.SPACE, space_id__in=space_ids)
        )
        .exclude(author_id__in=excluded_author_ids)
        .select_related("author", "space")
        .distinct()
    )


def chronological_feed_for(profile: SocialProfile | None) -> QuerySet[Post]:
    """Return the viewer's eligible Social timeline in reverse chronological order.

    This Development read model intentionally adds no recommendation ranking.
    Eligibility remains delegated to the authoritative visibility boundary.
    """

    return visible_posts_for(profile).order_by("-created_at", "-id")


def following_feed_for(profile: SocialProfile | None) -> QuerySet[Post]:
    """Return eligible posts from the viewer, accepted follows, and joined spaces.

    The feed composes on top of ``visible_posts_for`` so audience, moderation,
    bilateral block, viewer-selected mute, and protected-space ban decisions stay
    centralized. An anonymous caller has no personalized Following feed.
    """

    if profile is None:
        return Post.objects.none()

    following_ids = Follow.objects.filter(follower=profile, state=Follow.State.ACCEPTED).values_list(
        "followed_id", flat=True
    )
    banned_space_ids = _active_banned_space_ids(profile)
    space_ids = set(
        SpaceMembership.objects.filter(profile=profile, state=SpaceMembership.State.ACCEPTED).values_list(
            "space_id", flat=True
        )
    ) - banned_space_ids

    return (
        visible_posts_for(profile)
        .filter(Q(author=profile) | Q(author_id__in=following_ids) | Q(space_id__in=space_ids))
        .order_by("-created_at", "-id")
        .distinct()
    )
