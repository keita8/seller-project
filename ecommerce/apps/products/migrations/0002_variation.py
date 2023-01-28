# Generated by Django 4.1.5 on 2023-01-25 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Variation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "variation_category",
                    models.CharField(
                        choices=[("couleur", "couleur"), ("taille", "taille")],
                        max_length=100,
                        verbose_name="Caracteristiques",
                    ),
                ),
                ("variation_value", models.CharField(max_length=100, verbose_name="valeur")),
                ("is_active", models.BooleanField(default=True, verbose_name="Deja activé?")),
                ("created_date", models.DateTimeField(auto_now=True, verbose_name="Date de creation")),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                        verbose_name="Article",
                    ),
                ),
            ],
        ),
    ]
