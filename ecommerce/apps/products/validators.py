from .models import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

def validate_name(value):
    qs = Product.objects.filter(name__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(f"L'article {value} existe deja.")
    return value


unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')