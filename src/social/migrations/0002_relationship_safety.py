from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("social", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Block",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("blocked", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blocks_received", to="social.socialprofile")),
                ("blocker", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blocks_created", to="social.socialprofile")),
            ],
        ),
        migrations.CreateModel(
            name="Mute",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("muted", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="mutes_received", to="social.socialprofile")),
                ("muter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="mutes_created", to="social.socialprofile")),
            ],
        ),
        migrations.AddConstraint(
            model_name="block",
            constraint=models.UniqueConstraint(fields=("blocker", "blocked"), name="social_unique_block"),
        ),
        migrations.AddConstraint(
            model_name="block",
            constraint=models.CheckConstraint(condition=~models.Q(blocker=models.F("blocked")), name="social_block_no_self"),
        ),
        migrations.AddConstraint(
            model_name="mute",
            constraint=models.UniqueConstraint(fields=("muter", "muted"), name="social_unique_mute"),
        ),
        migrations.AddConstraint(
            model_name="mute",
            constraint=models.CheckConstraint(condition=~models.Q(muter=models.F("muted")), name="social_mute_no_self"),
        ),
    ]
