from django.urls import path


from . import views


app_name = 'orders'


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('api/v1/add/', views.OrderCreateView.as_view(), name='api_order_create'),
]