from django.db.models import Q, QuerySet

from .models import Block, Follow, Mute, Post, SocialProfile, SpaceMembership


def visible_posts_for(profile: SocialProfile | None) -> QuerySet[Post]:
    """Return ordinary visible-state posts the supplied social profile may read.

    The Development visibility boundary enforces current audience primitives,
    bilateral blocks, and viewer-selected mutes. It is not a substitute for
    future GoreeCloud Identity authorization, Privacy Shield policy, age/legal
    restrictions, or complete moderation and community-policy enforcement.
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
    space_ids = SpaceMembership.objects.filter(profile=profile, state=SpaceMembership.State.ACCEPTED).values_list(
        "space_id", flat=True
    )

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
