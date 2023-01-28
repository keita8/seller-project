import email
from rest_framework import serializers
from rest_framework.reverse import reverse
# from products.serializers import ProductSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('products:product-detail', kwargs={'pk':obj.pk}, request=request)

class UserPublicSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email'
        ]
    # other_products = serializers.SerializerMethodField(read_only=True)

    # def get_other_products(self, obj):
    #     request = self.context.get('request')
    #     user = obj
    #     my_products_qs = user.product_set.all()[:5]
    #     return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data
