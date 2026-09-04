from django.db.models import Q, QuerySet

from .models import Follow, Post, SocialProfile, SpaceMembership


def visible_posts_for(profile: SocialProfile | None) -> QuerySet[Post]:
    """Return ordinary visible-state posts the supplied social profile may read.

    This Development helper covers the current audience primitives only. It is
    not a substitute for future Identity, Privacy Shield, block/mute, age,
    legal, moderation, or community-policy enforcement.
    """

    posts = Post.objects.filter(moderation_state=Post.ModerationState.VISIBLE)
    if profile is None:
        return posts.filter(audience=Post.Audience.PUBLIC).select_related("author", "space")

    following_ids = set(Follow.objects.filter(follower=profile, state=Follow.State.ACCEPTED).values_list("followed_id", flat=True))
    follower_ids = set(Follow.objects.filter(followed=profile, state=Follow.State.ACCEPTED).values_list("follower_id", flat=True))
    mutual_ids = following_ids & follower_ids
    space_ids = SpaceMembership.objects.filter(profile=profile, state=SpaceMembership.State.ACCEPTED).values_list("space_id", flat=True)

    return (
        posts.filter(
            Q(audience=Post.Audience.PUBLIC)
            | Q(author=profile)
            | Q(audience=Post.Audience.FOLLOWERS, author_id__in=following_ids)
            | Q(audience=Post.Audience.FRIENDS, author_id__in=mutual_ids)
            | Q(audience=Post.Audience.SPACE, space_id__in=space_ids)
        )
        .select_related("author", "space")
        .distinct()
    )
