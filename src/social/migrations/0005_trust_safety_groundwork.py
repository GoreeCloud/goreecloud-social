from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("social", "0004_social_graph_community")]

    operations = [
        migrations.CreateModel(
            name="Restrict",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("restricted", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="restrictions_received", to="social.socialprofile")),
                ("restrictor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="restrictions_created", to="social.socialprofile")),
            ],
        ),
        migrations.CreateModel(
            name="ProfileReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.CharField(max_length=80)),
                ("details", models.CharField(blank=True, max_length=1000)),
                ("state", models.CharField(choices=[("open", "Open"), ("reviewing", "Reviewing"), ("resolved", "Resolved"), ("dismissed", "Dismissed")], default="open", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reporter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="profile_reports_created", to="social.socialprofile")),
                ("target", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="profile_reports_received", to="social.socialprofile")),
            ],
        ),
        migrations.CreateModel(
            name="SpaceBan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("imposed_by_subject", models.CharField(max_length=255)),
                ("reason", models.CharField(blank=True, max_length=500)),
                ("state", models.CharField(choices=[("active", "Active"), ("revoked", "Revoked"), ("expired", "Expired")], default="active", max_length=16)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="space_bans", to="social.socialprofile")),
                ("space", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bans", to="social.space")),
            ],
        ),
        migrations.CreateModel(
            name="ModerationCase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("opened_by_subject", models.CharField(max_length=255)),
                ("reason", models.CharField(max_length=80)),
                ("state", models.CharField(choices=[("open", "Open"), ("reviewing", "Reviewing"), ("actioned", "Actioned"), ("dismissed", "Dismissed"), ("closed", "Closed")], default="open", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("post", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="moderation_cases", to="social.post")),
                ("profile", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="moderation_cases", to="social.socialprofile")),
                ("space", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="moderation_cases", to="social.space")),
            ],
        ),
        migrations.CreateModel(
            name="ModerationAction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("actor_subject", models.CharField(max_length=255)),
                ("kind", models.CharField(choices=[("warn", "Warn"), ("limit", "Limit"), ("remove", "Remove"), ("restore", "Restore"), ("restrict", "Restrict"), ("suspend", "Suspend"), ("space-ban", "Space ban"), ("space-unban", "Space unban")], max_length=20)),
                ("note", models.CharField(blank=True, max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="actions", to="social.moderationcase")),
            ],
        ),
        migrations.CreateModel(
            name="ModerationAppeal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.CharField(max_length=1000)),
                ("state", models.CharField(choices=[("submitted", "Submitted"), ("reviewing", "Reviewing"), ("upheld", "Upheld"), ("modified", "Modified"), ("overturned", "Overturned"), ("dismissed", "Dismissed")], default="submitted", max_length=16)),
                ("resolution_note", models.CharField(blank=True, max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("appellant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="moderation_appeals", to="social.socialprofile")),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="appeals", to="social.moderationcase")),
            ],
        ),
        migrations.AddConstraint(
            model_name="restrict",
            constraint=models.UniqueConstraint(fields=("restrictor", "restricted"), name="social_unique_restrict"),
        ),
        migrations.AddConstraint(
            model_name="restrict",
            constraint=models.CheckConstraint(condition=~models.Q(restrictor=models.F("restricted")), name="social_restrict_no_self"),
        ),
        migrations.AddConstraint(
            model_name="profilereport",
            constraint=models.CheckConstraint(condition=~models.Q(reporter=models.F("target")), name="social_profile_report_no_self"),
        ),
        migrations.AddConstraint(
            model_name="spaceban",
            constraint=models.UniqueConstraint(fields=("space", "profile"), name="social_unique_space_ban"),
        ),
        migrations.AddConstraint(
            model_name="moderationcase",
            constraint=models.CheckConstraint(
                condition=(
                    (models.Q(post__isnull=False) & models.Q(profile__isnull=True))
                    | (models.Q(post__isnull=True) & models.Q(profile__isnull=False))
                ),
                name="social_moderation_case_one_target",
            ),
        ),
        migrations.AddConstraint(
            model_name="moderationappeal",
            constraint=models.UniqueConstraint(fields=("case", "appellant"), name="social_unique_moderation_appeal"),
        ),
    ]
