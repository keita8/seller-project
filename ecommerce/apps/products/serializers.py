from unicodedata import category
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import (validate_name, unique_product_title)
from ecommerce.apps.api.serializers import UserPublicSerializer
from rest_framework.serializers import Serializer
from rest_framework_money_field import MoneyField
from ecommerce.apps.products.models import Categorie
from djmoney.contrib.django_rest_framework import MoneyField

from ecommerce.apps.products import validators

class CategorieSerializer(serializers.ModelSerializer):
    categorie = serializers.SerializerMethodField(source='categorie', read_only=True)

    class Meta:
        model = Categorie
        fields = ('categorie',)


        
class ProductInlineSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(read_only=True)

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('products:product-update', kwargs={'slug':obj.slug}, request=request)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    # category = CategorieSerializer(read_only=True)
    # related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    prix = serializers.DecimalField(source='price', max_digits=10, decimal_places=2)
    # prix = MoneyField(source='price', max_digits=10, decimal_places=2)
    modifier= serializers.SerializerMethodField(source='updateurl', read_only=True)
    article = serializers.CharField(source='title', validators=[unique_product_title])
    stock = serializers.IntegerField(source='quantity')
    tendance = serializers.BooleanField(source='featured')
    url = serializers.SerializerMethodField(read_only=True)
    #url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')
    class Meta:
        model = Product
        fields = [
            'id',
            # 'user',
            'owner',
            'url',
            'category',
            'stock',
            'modifier',
            # 'email',
            'article',
            'content',
            'prix',
            'path',
            'image',
            'active',
            'tendance',
            'endpoint'
            
            # 'sale_price',
            # 'my_user_data',
            # 'related_products'
        ]

    def get_my_user_data(self, obj):
        return {
            'username': obj.user.username
        }

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('products:product-detail', kwargs={'slug':obj.slug}, request=request)

    def get_updateurl(self, obj):
        # return f"api/products/details/{obj.pk}/"
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("products:product-update", kwargs={'slug':obj.slug}, request=request)
   
    def get_modifier(self, obj):
        # return f"api/products/details/{obj.pk}/"
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("products:product-update", kwargs={'slug':obj.slug}, request=request)

    
    def validate_name(self, value):
        qs = Product.objects.filter(name__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f"L'article {value} existe deja.")
        return value

    
    # def create(self, validated_data):
    #     # email = validated_data.pop('email')
    #     # print(email)
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)
