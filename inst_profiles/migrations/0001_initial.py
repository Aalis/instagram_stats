from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        # Add dependencies if any
    ]

    operations = [
        migrations.CreateModel(
            name="InstProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("link", models.URLField(unique=True)),
                ("followers_count", models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
    ]
