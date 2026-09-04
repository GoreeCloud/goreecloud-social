from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("social", "0003_content_interactions")]

    operations = [
        migrations.CreateModel(
            name="ProfileCollection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(choices=[("list", "List"), ("circle", "Circle")], max_length=16)),
                ("name", models.CharField(max_length=120)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="profile_collections", to="social.socialprofile")),
            ],
        ),
        migrations.CreateModel(
            name="ProfileCollectionMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("collection", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="members", to="social.profilecollection")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="collection_memberships", to="social.socialprofile")),
            ],
        ),
        migrations.CreateModel(
            name="SpaceRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("description", models.CharField(blank=True, max_length=1000)),
                ("position", models.PositiveSmallIntegerField()),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("space", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rules", to="social.space")),
            ],
            options={"ordering": ("position", "id")},
        ),
        migrations.CreateModel(
            name="SpaceInvitation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("state", models.CharField(choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined"), ("revoked", "Revoked"), ("expired", "Expired")], default="pending", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                ("invitee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="space_invitations_received", to="social.socialprofile")),
                ("inviter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="space_invitations_sent", to="social.socialprofile")),
                ("space", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="invitations", to="social.space")),
            ],
        ),
        migrations.CreateModel(
            name="SpaceJoinRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("state", models.CharField(choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined"), ("cancelled", "Cancelled"), ("expired", "Expired")], default="pending", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                ("requester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="space_join_requests", to="social.socialprofile")),
                ("space", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="join_requests", to="social.space")),
            ],
        ),
        migrations.AddConstraint(
            model_name="profilecollection",
            constraint=models.UniqueConstraint(fields=("owner", "kind", "name"), name="social_unique_profile_collection_name"),
        ),
        migrations.AddConstraint(
            model_name="profilecollectionmember",
            constraint=models.UniqueConstraint(fields=("collection", "profile"), name="social_unique_profile_collection_member"),
        ),
        migrations.AddConstraint(
            model_name="spacerule",
            constraint=models.UniqueConstraint(fields=("space", "position"), name="social_unique_space_rule_position"),
        ),
        migrations.AddConstraint(
            model_name="spaceinvitation",
            constraint=models.UniqueConstraint(fields=("space", "invitee"), name="social_unique_space_invitation"),
        ),
        migrations.AddConstraint(
            model_name="spaceinvitation",
            constraint=models.CheckConstraint(condition=~models.Q(inviter=models.F("invitee")), name="social_invitation_no_self"),
        ),
        migrations.AddConstraint(
            model_name="spacejoinrequest",
            constraint=models.UniqueConstraint(fields=("space", "requester"), name="social_unique_space_join_request"),
        ),
    ]
