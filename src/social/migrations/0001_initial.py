from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(name="SocialProfile", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("identity_subject", models.CharField(max_length=255, unique=True)),
            ("handle", models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message="Handles must contain 3-30 lowercase letters, numbers, or underscores.", regex="^[a-z0-9_]{3,30}$")])),
            ("display_name", models.CharField(max_length=120)),
            ("bio", models.CharField(blank=True, max_length=500)),
            ("visibility", models.CharField(choices=[("public", "Public"), ("private", "Private")], default="public", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
        ]),
        migrations.CreateModel(name="Space", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("kind", models.CharField(choices=[("group", "Group"), ("community", "Community")], max_length=16)),
            ("slug", models.SlugField(max_length=80, unique=True)),
            ("name", models.CharField(max_length=120)),
            ("description", models.CharField(blank=True, max_length=500)),
            ("visibility", models.CharField(choices=[("public", "Public"), ("private", "Private"), ("invite-only", "Invite only")], default="public", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="owned_spaces", to="social.socialprofile")),
        ]),
        migrations.CreateModel(name="Post", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("content_kind", models.CharField(choices=[("text", "Text"), ("photo", "Photo"), ("video", "Video"), ("gif", "GIF"), ("link", "Link")], default="text", max_length=16)),
            ("body", models.TextField(blank=True)),
            ("audience", models.CharField(choices=[("public", "Public"), ("followers", "Followers"), ("friends", "Mutual relationships"), ("space", "Group or community"), ("only-me", "Only me")], default="public", max_length=16)),
            ("reply_policy", models.CharField(choices=[("everyone", "Everyone"), ("followed", "People I follow"), ("mentioned", "Mentioned profiles"), ("no-one", "No one")], default="everyone", max_length=16)),
            ("moderation_state", models.CharField(choices=[("visible", "Visible"), ("limited", "Limited"), ("pending", "Pending review"), ("removed", "Removed")], default="visible", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="posts", to="social.socialprofile")),
            ("space", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="posts", to="social.space")),
        ], options={"ordering": ("-created_at", "-id")}),
        migrations.CreateModel(name="Follow", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("state", models.CharField(choices=[("pending", "Pending"), ("accepted", "Accepted")], default="pending", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("followed", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="follower_edges", to="social.socialprofile")),
            ("follower", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="following_edges", to="social.socialprofile")),
        ]),
        migrations.CreateModel(name="MediaAttachment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("kind", models.CharField(choices=[("photo", "Photo"), ("video", "Video"), ("gif", "GIF")], max_length=16)),
            ("storage_key", models.CharField(max_length=512)),
            ("alt_text", models.CharField(blank=True, max_length=1000)),
            ("position", models.PositiveSmallIntegerField(default=0)),
            ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="media", to="social.post")),
        ], options={"ordering": ("position", "id")}),
        migrations.CreateModel(name="PostReport", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("reason", models.CharField(max_length=80)),
            ("details", models.CharField(blank=True, max_length=1000)),
            ("state", models.CharField(choices=[("open", "Open"), ("reviewing", "Reviewing"), ("resolved", "Resolved"), ("dismissed", "Dismissed")], default="open", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reports", to="social.post")),
            ("reporter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reports", to="social.socialprofile")),
        ]),
        migrations.CreateModel(name="Reaction", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("kind", models.CharField(choices=[("like", "Like"), ("love", "Love"), ("laugh", "Laugh"), ("wow", "Wow"), ("sad", "Sad"), ("angry", "Angry"), ("support", "Support")], default="like", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to="social.post")),
            ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to="social.socialprofile")),
        ]),
        migrations.CreateModel(name="Repost", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("quote_text", models.CharField(blank=True, max_length=1000)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reposts", to="social.post")),
            ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reposts", to="social.socialprofile")),
        ]),
        migrations.CreateModel(name="SpaceMembership", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("role", models.CharField(choices=[("member", "Member"), ("moderator", "Moderator"), ("admin", "Administrator"), ("owner", "Owner")], default="member", max_length=16)),
            ("state", models.CharField(choices=[("pending", "Pending"), ("accepted", "Accepted"), ("suspended", "Suspended")], default="pending", max_length=16)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="space_memberships", to="social.socialprofile")),
            ("space", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="social.space")),
        ]),
        migrations.AddConstraint(model_name="follow", constraint=models.UniqueConstraint(fields=("follower", "followed"), name="social_unique_follow")),
        migrations.AddConstraint(model_name="follow", constraint=models.CheckConstraint(condition=~models.Q(follower=models.F("followed")), name="social_follow_no_self")),
        migrations.AddConstraint(model_name="mediaattachment", constraint=models.UniqueConstraint(fields=("post", "position"), name="social_unique_media_position")),
        migrations.AddConstraint(model_name="reaction", constraint=models.UniqueConstraint(fields=("profile", "post"), name="social_unique_post_reaction")),
        migrations.AddConstraint(model_name="repost", constraint=models.UniqueConstraint(fields=("profile", "post"), name="social_unique_repost")),
        migrations.AddConstraint(model_name="spacemembership", constraint=models.UniqueConstraint(fields=("space", "profile"), name="social_unique_space_membership")),
    ]
