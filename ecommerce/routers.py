from rest_framework.routers import DefaultRouter
from ecommerce.apps.products.viewsets import ProductViewSet, ProductGenericViewSet

router = DefaultRouter()
router.register('', ProductGenericViewSet, basename='products')

urlpatterns = router.urls