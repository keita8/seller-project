# Generated by Django 4.1.5 on 2023-01-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_alter_categorie_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="categorie",
            name="active",
        ),
        migrations.AddField(
            model_name="categorie",
            name="is_public",
            field=models.BooleanField(default=True, verbose_name="public"),
        ),
    ]
