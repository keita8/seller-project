# Generated by Django 4.1.5 on 2023-01-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_categorie_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorie",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]
