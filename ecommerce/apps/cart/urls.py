from django.urls import path 
from . import views 

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='main'),
    path('add/<slug:slug>/', views.add_cart, name='add'),
]
