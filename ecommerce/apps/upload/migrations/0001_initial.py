# Generated by Django 4.1.5 on 2023-01-25 19:46

import django.core.validators
from django.db import migrations, models
import ecommerce.apps.upload.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="image")),
                (
                    "image",
                    versatileimagefield.fields.VersatileImageField(
                        upload_to=ecommerce.apps.upload.models.upload_image_path,
                        validators=[django.core.validators.FileExtensionValidator(["jpg", "png"])],
                        verbose_name="Image",
                    ),
                ),
                ("image_ppoi", versatileimagefield.fields.PPOIField(default="0.5x0.5", editable=False, max_length=20)),
            ],
        ),
    ]
