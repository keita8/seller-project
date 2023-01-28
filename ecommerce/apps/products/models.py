from base64 import encode
from decimal import Decimal
from unicodedata import category
from django.db import models
from django.db.models import Q
from django.forms import DecimalField
from django.urls import reverse
from django.utils.text import slugify
from moneyed import force_decimal
from .utils import *
from tinymce.models import HTMLField
from djmoney.models.fields import MoneyField
from django.db.models.signals import *

from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
import os
import random
import string
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
import uuid
# from moneyfield import MoneyField
from versatileimagefield.fields import VersatileImageField, PPOIField
from djmoney.money import Money
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from ecommerce.apps.upload.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

TAGS_MODEL_VALUES = ['electroniques', 'voitures', 'vêtements', 'films', 'cameras']


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910207878)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"product/qr_code/{new_filename}/{final_filename}"


def get_filename_ext2(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path2(instance, filename):
    new_filename = random.randint(1, 3910207878)
    name, ext = get_filename_ext2(filename)
    final_filename = f"{new_filename}{ext}"
    return f"articles/images/{new_filename}/{final_filename}"





class CategorieQuerySet(models.query.QuerySet):
    def is_public(self):
        return self.filter(is_public=True)

    def search(self, query, user=None):
        lookup = Q(categorie__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class CategorieManager(models.Manager):
    def get_queryset(self):
        return CategorieQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

    # affiche tous les articles disponibles
    def all(self):
        return self.get_queryset().is_public()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None




class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def is_public(self):
            return self.filter(active=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

    def featured(self):
        return self.filter(featured=True, active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

    # affiche tous les articles disponibles
    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None



class Categorie(models.Model):
    categorie = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    is_public = models.BooleanField("public", default=True)
    
    objects = CategorieManager()
    
    def get_product(self):
        return self.product_set.all()
    
    def save(self, *args, **kwargs):
           if not self.slug:
               self.slug = slugify(self.categorie)
               return super().save(*args, **kwargs) # Call the real save() method
    
    def __str__(self):
        return self.categorie
        

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def is_public(self):
            return self.filter(active=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

    def featured(self):
        return self.filter(featured=True, active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

    # affiche tous les articles disponibles
    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


class ProductManager2(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def features(self):
        return self.get_queryset().featured()
    

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


    # affiche tous les articles disponibles
    def all(self):
        return self.get_queryset().active()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None


class Product(models.Model):
    product_id = models.UUIDField(
         default = uuid.uuid4,
         editable = False, 
         unique=True
    )
    user = models.ForeignKey(User,default=1, on_delete=models.CASCADE, verbose_name='vendeur')
    category = models.ForeignKey(Categorie,related_name='categories', verbose_name="catégorie", on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name="article", unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    reference = models.CharField(max_length=20, blank=True, unique=True)
    content = HTMLField(blank=True, null=True)
    quantity = models.IntegerField(default=1, verbose_name='quantité')
    price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name="Prix")
    # price = MoneyField(
    #     default=800.00,
    #     max_digits=20,
    #     decimal_places=2,
    #     default_currency="GNF",
    #     validators=[
    #         MinMoneyValidator(10),
    #         MaxMoneyValidator(1000000000000),
    #         MinMoneyValidator(Money(500, "GNF")),
    #         MaxMoneyValidator(Money(1000000000000, "GNF")),
    #         MinMoneyValidator({"EUR": 100, "USD": 50}),
    #         MaxMoneyValidator({"EUR": 1000000000000, "USD": 1000000000000}),
    #     ],
    #     verbose_name="prix",
    # )
    image = models.ManyToManyField(Image,related_name='upload', verbose_name="article image")
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True, verbose_name="Disponible ?")
    image_ppoi = PPOIField()
    objects = ProductManager2()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def price_by_quantity(self):
        amount = self.price * force_decimal(self.quantity)
        return amount

    @property
    def get_reference(self):
        return self.reference if self.reference else None


    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

       
    def is_public(self)->bool:
        return self.active
    
    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/products/{self.pk}/"
    
    @property
    def sale_price(self):
        return "%.2f"%(float(self.price) * 0.8)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.reference:
        instance.reference = unique_order_id_generator(instance)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)




class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='couleur', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='taille', is_active=True)


variation_category_choice = (
    ('couleur', 'couleur'),
    ('taille', 'taille'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Article", blank=True, null=True)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice,verbose_name="Caracteristiques")
    variation_value = models.CharField(max_length=100, verbose_name="valeur")
    is_active = models.BooleanField(default=True, verbose_name="Deja activé?")
    created_date = models.DateTimeField(auto_now=True, verbose_name="Date de creation")

    objects = VariationManager()
    
    class Meta:
        verbose_name = 'Caracteristique'
        verbose_name_plural = 'Caracteristiques'

    def __str__(self):
        return self.variation_value

