# Generated by Django 4.1.5 on 2023-01-26 09:32

import django.core.validators
from django.db import migrations
import ecommerce.apps.accounts.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_profile_image_ppoi"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=versatileimagefield.fields.VersatileImageField(
                upload_to=ecommerce.apps.accounts.models.upload_image_path,
                validators=[django.core.validators.FileExtensionValidator(["jpg", "png"])],
                verbose_name="Photo de profil",
            ),
        ),
    ]
