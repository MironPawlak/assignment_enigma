from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderCreateView, CommonProductsListView

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
app_name = 'products'
urlpatterns = [
    path('', include(router.urls)),
    path('order/', OrderCreateView.as_view(), name='order'),
    path('common_product/', CommonProductsListView.as_view(), name='common_product'),
]
