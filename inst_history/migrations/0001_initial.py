import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("inst_profiles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InstHistory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("followers_count", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inst_profiles.instprofile",
                    ),
                ),
            ],
        ),
    ]
