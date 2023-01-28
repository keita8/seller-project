from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    # path('', include('ecommerce.apps.products.urls')),
    path('', include("ecommerce.apps.products.urls")),
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include("ecommerce.apps.api.urls")),
    path('api/search/', include("ecommerce.apps.search.urls")),
    path('cart/', include("ecommerce.apps.cart.urls")),
    path('accounts/', include("ecommerce.apps.accounts.urls", namespace='accounts')),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
