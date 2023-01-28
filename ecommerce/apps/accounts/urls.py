from django.urls import path 
from . import views 

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('reset-password/', views.reset_password, name='reset-password'),
]
