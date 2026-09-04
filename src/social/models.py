from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


handle_validator = RegexValidator(
    regex=r"^[a-z0-9_]{3,30}$",
    message="Handles must contain 3-30 lowercase letters, numbers, or underscores.",
)


class SocialProfile(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"

    identity_subject = models.CharField(max_length=255, unique=True)
    handle = models.CharField(max_length=30, unique=True, validators=[handle_validator])
    display_name = models.CharField(max_length=120)
    bio = models.CharField(max_length=500, blank=True)
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"@{self.handle}"


class Space(models.Model):
    class Kind(models.TextChoices):
        GROUP = "group", "Group"
        COMMUNITY = "community", "Community"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"
        INVITE_ONLY = "invite-only", "Invite only"

    kind = models.CharField(max_length=16, choices=Kind.choices)
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500, blank=True)
    visibility = models.CharField(max_length=16, choices=Visibility.choices, default=Visibility.PUBLIC)
    owner = models.ForeignKey(SocialProfile, on_delete=models.PROTECT, related_name="owned_spaces")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class SpaceMembership(models.Model):
    class Role(models.TextChoices):
        MEMBER = "member", "Member"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Administrator"
        OWNER = "owner", "Owner"

    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        SUSPENDED = "suspended", "Suspended"

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="memberships")
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="space_memberships")
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.MEMBER)
    state = models.CharField(max_length=16, choices=State.choices, default=State.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("space", "profile"), name="social_unique_space_membership")]


class Follow(models.Model):
    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"

    follower = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="following_edges")
    followed = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="follower_edges")
    state = models.CharField(max_length=16, choices=State.choices, default=State.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("follower", "followed"), name="social_unique_follow"),
            models.CheckConstraint(condition=~models.Q(follower=models.F("followed")), name="social_follow_no_self"),
        ]


class Block(models.Model):
    blocker = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="blocks_created")
    blocked = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="blocks_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("blocker", "blocked"), name="social_unique_block"),
            models.CheckConstraint(condition=~models.Q(blocker=models.F("blocked")), name="social_block_no_self"),
        ]


class Mute(models.Model):
    muter = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="mutes_created")
    muted = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="mutes_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("muter", "muted"), name="social_unique_mute"),
            models.CheckConstraint(condition=~models.Q(muter=models.F("muted")), name="social_mute_no_self"),
        ]


class Post(models.Model):
    class ContentKind(models.TextChoices):
        TEXT = "text", "Text"
        PHOTO = "photo", "Photo"
        VIDEO = "video", "Video"
        GIF = "gif", "GIF"
        LINK = "link", "Link"

    class Audience(models.TextChoices):
        PUBLIC = "public", "Public"
        FOLLOWERS = "followers", "Followers"
        FRIENDS = "friends", "Mutual relationships"
        SPACE = "space", "Group or community"
        ONLY_ME = "only-me", "Only me"

    class ReplyPolicy(models.TextChoices):
        EVERYONE = "everyone", "Everyone"
        FOLLOWED = "followed", "People I follow"
        MENTIONED = "mentioned", "Mentioned profiles"
        NO_ONE = "no-one", "No one"

    class ModerationState(models.TextChoices):
        VISIBLE = "visible", "Visible"
        LIMITED = "limited", "Limited"
        PENDING = "pending", "Pending review"
        REMOVED = "removed", "Removed"

    author = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="posts")
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=True, blank=True, related_name="posts")
    content_kind = models.CharField(max_length=16, choices=ContentKind.choices, default=ContentKind.TEXT)
    body = models.TextField(blank=True)
    audience = models.CharField(max_length=16, choices=Audience.choices, default=Audience.PUBLIC)
    reply_policy = models.CharField(max_length=16, choices=ReplyPolicy.choices, default=ReplyPolicy.EVERYONE)
    moderation_state = models.CharField(max_length=16, choices=ModerationState.choices, default=ModerationState.VISIBLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        super().clean()
        if self.audience == self.Audience.SPACE and self.space_id is None:
            raise ValidationError({"space": "A space-audience post must belong to a group or community."})

    class Meta:
        ordering = ("-created_at", "-id")


class MediaAttachment(models.Model):
    class Kind(models.TextChoices):
        PHOTO = "photo", "Photo"
        VIDEO = "video", "Video"
        GIF = "gif", "GIF"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    kind = models.CharField(max_length=16, choices=Kind.choices)
    storage_key = models.CharField(max_length=512)
    alt_text = models.CharField(max_length=1000, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "id")
        constraints = [models.UniqueConstraint(fields=("post", "position"), name="social_unique_media_position")]


class Reaction(models.Model):
    class Kind(models.TextChoices):
        LIKE = "like", "Like"
        LOVE = "love", "Love"
        LAUGH = "laugh", "Laugh"
        WOW = "wow", "Wow"
        SAD = "sad", "Sad"
        ANGRY = "angry", "Angry"
        SUPPORT = "support", "Support"

    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.LIKE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("profile", "post"), name="social_unique_post_reaction")]


class Repost(models.Model):
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="reposts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reposts")
    quote_text = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("profile", "post"), name="social_unique_repost")]


class PostReport(models.Model):
    class State(models.TextChoices):
        OPEN = "open", "Open"
        REVIEWING = "reviewing", "Reviewing"
        RESOLVED = "resolved", "Resolved"
        DISMISSED = "dismissed", "Dismissed"

    reporter = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name="reports")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=80)
    details = models.CharField(max_length=1000, blank=True)
    state = models.CharField(max_length=16, choices=State.choices, default=State.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
