# Generated by Django 4.1.5 on 2023-01-25 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "compte", "verbose_name_plural": "comptes"},
        ),
    ]
