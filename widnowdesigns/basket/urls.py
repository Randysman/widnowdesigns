from django.urls import path, include
from . import views
from rest_framework import routers

from .views import *

app_name = 'basket'


urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:product_id>', views.basket_remove, name='basket_remove'),
    path('api/v1/', BasketDetail.as_view(), name='api_basket_detail'),
    path('api/v1/add/<int:product_id>/', BasketAddView.as_view(), name='api_basket_add'),
    path('api/v1/delete/<int:product_id>/', BasketRemoveView.as_view(), name='api_basket_remove'),
]