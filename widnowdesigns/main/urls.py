from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views
from .views import ProductViewSet, CategoryViewSet

app_name = 'main'

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)


urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/category/<slug:category_slug>', views.product_list, name='product_list_by_category'),
    path('api/v1/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]