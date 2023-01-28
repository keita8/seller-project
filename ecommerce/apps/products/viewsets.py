from rest_framework import viewsets, mixins
from ecommerce.apps.products.models import Product
from ecommerce.apps.products.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductGenericViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


product_list_view = ProductGenericViewSet.as_view({'get':'list'})
product_retrieve_view = ProductGenericViewSet.as_view({'get':'retrieve'})