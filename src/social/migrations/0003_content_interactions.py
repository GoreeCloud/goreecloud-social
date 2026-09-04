from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("social", "0002_relationship_safety")]

    operations = [
        migrations.AddField(
            model_name="post",
            name="reply_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="replies",
                to="social.post",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="content_kind",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("photo", "Photo"),
                    ("video", "Video"),
                    ("gif", "GIF"),
                    ("link", "Link"),
                    ("poll", "Poll"),
                ],
                default="text",
                max_length=16,
            ),
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookmarked_by", to="social.post")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookmarks", to="social.socialprofile")),
            ],
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=280)),
                ("closes_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("post", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="poll", to="social.post")),
            ],
        ),
        migrations.CreateModel(
            name="PollOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=160)),
                ("position", models.PositiveSmallIntegerField()),
                ("poll", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="social.poll")),
            ],
            options={"ordering": ("position", "id")},
        ),
        migrations.CreateModel(
            name="PollVote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("option", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="social.polloption")),
                ("poll", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="social.poll")),
                ("voter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="poll_votes", to="social.socialprofile")),
            ],
        ),
        migrations.AddConstraint(
            model_name="bookmark",
            constraint=models.UniqueConstraint(fields=("profile", "post"), name="social_unique_bookmark"),
        ),
        migrations.AddConstraint(
            model_name="polloption",
            constraint=models.UniqueConstraint(fields=("poll", "position"), name="social_unique_poll_option_position"),
        ),
        migrations.AddConstraint(
            model_name="pollvote",
            constraint=models.UniqueConstraint(fields=("poll", "voter"), name="social_unique_single_choice_poll_vote"),
        ),
    ]
