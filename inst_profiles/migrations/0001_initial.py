# Generated by Django 5.0 on 2024-01-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('followers_count', models.PositiveIntegerField()),
            ],
        ),
    ]
