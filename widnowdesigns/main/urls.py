from django.urls import path, include
from rest_framework import routers

from . import views
from .views import ProductViewSet

app_name = 'main'

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)


urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/category/<slug:category_slug>', views.product_list, name='product_list_by_category'),
    path('api/v1/', include(router.urls)),
]