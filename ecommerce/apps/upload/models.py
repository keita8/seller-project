from distutils.command.upload import upload
from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
import os
import random
import string


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910207878)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"products/{new_filename}/{final_filename}"


class Image(models.Model):
    name = models.CharField(max_length=255, verbose_name="image")
    image = VersatileImageField(
        "Image",
        upload_to=upload_image_path,
        ppoi_field="image_ppoi",
        validators=[FileExtensionValidator(["jpg", "png"])],
    )

    image_ppoi = PPOIField()

    def __str__(self):
        return self.name
