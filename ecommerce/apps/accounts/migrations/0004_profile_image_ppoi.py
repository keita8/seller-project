# Generated by Django 4.1.5 on 2023-01-26 09:21

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="image_ppoi",
            field=versatileimagefield.fields.PPOIField(default="0.5x0.5", editable=False, max_length=20),
        ),
    ]
