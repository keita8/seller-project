from django.shortcuts import render
from django.http import JsonResponse 
import json

from yaml import serialize
from ecommerce.apps.products.models import Product
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ecommerce.apps.products.serializers import ProductSerializer
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response


# from products.models import Product
# from products.serializers import ProductSerializer
@api_view(['POST'])
def api_home_view(request, *args, **kwargs):
    
    serializer = ProductSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.data
        print(data)    
        return Response(data)

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.save()
        # instance = form.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400)
