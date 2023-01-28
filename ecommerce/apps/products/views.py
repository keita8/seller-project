from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests import request
import requests
from ecommerce.apps.products.models import *
from django.views.generic import *
from ecommerce.apps.products.serializers import CategorieSerializer
from .permissions import *
from rest_framework import authentication, mixins, permissions
from rest_framework import generics, mixins, permissions, authentication
from ecommerce.apps.products.models import Product 
from ecommerce.apps.products.serializers import ProductSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ecommerce.apps.api.permissions import IsStaffEditorPermission
from ecommerce.apps.api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from ecommerce.apps.api.authentication import TokenAuthentication


class ListProductView(ListView):
    model = Product
    template_name = "layouts/index.html"
    context_object_name = "object_list"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        slug    = self.kwargs.get('slug')
        return Product.objects.all()




class ProductDetailView(DetailView):
    model = Product
    template_name = "layouts/detail.html"
    context_object_name = "detail"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        try:
            instance = Product.objects.get_by_slug(slug)
        except Product.DoesNotExist:
            raise Http404("Cet article n'existe pas.")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Aucun article trouvé...")
        return instance

    def get_queryset(self, *args, **kwargs):
        request = self.request
        slug    = self.kwargs.get('slug')
        pk    = self.kwargs.get('pk')
        return Product.objects.filter(slug=slug)



""" LES MIXINS """
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


    def get(self, request, *args, **kwargs): # HTT -> get
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

    def perform_create(self, serializer):
        name = serializer.validated_data.get("name")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = name
        serializer.save(content=content)



""" CREER OU LISTER LES ARTICLES """
class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication,
    # ]
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        quantity = serializer.validated_data.get("quantity")
        price = serializer.validated_data.get("price")
        # email = serializer.validated_data.pop("user")
        image = serializer.validated_data.pop("image")
        category = serializer.validated_data.pop("category")
        featured = serializer.validated_data.pop("featured")
        active = serializer.validated_data.pop("active")
        # print(email)
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return Product.objects.none()
        print(request.user)
        return qs.filter(user=request.user)


""" DETAILS D'UN ARTICLE """
class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    lookup_field = 'slug'



""" LISTER TOUS LES ARTICLES """
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


""" MODIFIER UN ARTICLE """
class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.name



""" SUPPRIMER UN ARTICLE """
class ProductDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]



    def perform_destroy(self, instance):
        super().perform_destroy(instance)



class ProductsMixinAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


    def perform_create(self, serializer):
        category = serializer.validated_data.get("category")
        quantity = serializer.validated_data.get("quantity")
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        price = serializer.validated_data.get("price")
        description = serializer.validated_data.get("description")
        image = serializer.validated_data.get("image")
        featured = serializer.validated_data.get("featured")
        active = serializer.validated_data.get("active")

        return super().perform_create(serializer)

    def perform_update(self, serializer):
        category = serializer.validated_data.get("category")
        quantity = serializer.validated_data.get("quantity")
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        price = serializer.validated_data.get("price")
        description = serializer.validated_data.get("description")
        image = serializer.validated_data.get("image")
        featured = serializer.validated_data.get("featured")
        active = serializer.validated_data.get("active")
        return super().perform_update(serializer)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("slug")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("slug")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CategorieListOrCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorieSerializer
    queryset = Categorie.objects.all()
    lookup_field = 'pk'
    
    def perform_create(self, serializer):
        categorie = serializer.validated_data.pop("categorie")
        featured = serializer.validated_data.pop("featured")
        active = serializer.validated_data.pop("active")
        serializer.save()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return Product.objects.none()
        print(request.user)
        return qs.filter(user=request.user)















""" Vue basée sur la fonction """
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        # afficher les details d'un object via sa clé primaire
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exist():
            #     raise Http404("Cet article n'existe pas")
            return Response(data)

        # lister tous les objets
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    # créer un objet
    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get("name")
            content = serializer.validated_data.get("content") or None
            price = serializer.validated_data.get("price") 
            if content is None:
                content = name
                serializer.save(content=content)
            return Response(serializer.data)
        return Response({'detail':'La méthode Get n\'est pas autorisée'}, status=400)
