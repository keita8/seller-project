from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.ListProductView.as_view(), name='home'),
    path('article/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    
    
    
    
    
    
    
    path("", views.ProductListCreateAPIView.as_view(), name="all-article"),
    # path("", views.ProductsMixinAPIView.as_view(), name="all-article"),
    path("create/", views.ProductListCreateAPIView.as_view(), name="product-create"),
    # path("create/", views.ProductsMixinAPIView.as_view(), name="product-create"),
    path("detail/<str:slug>/", views.ProductDetailAPIView.as_view(), name="product-detail"),
    # path("detail/<str:slug>/", views.ProductsMixinAPIView.as_view(), name="product-detail"),
    #path("update/<str:slug>/", views.ProductUpdateAPIView.as_view(), name="product-update"),
    path("update/<str:slug>/", views.ProductsMixinAPIView.as_view(), name="product-update"),
    path("delete/<str:slug>/", views.ProductDestroyAPIView.as_view(), name="product-delete"),
    # path("delete/<str:slug>/", views.ProductsMixinAPIView.as_view(), name="product-delete"),
]
