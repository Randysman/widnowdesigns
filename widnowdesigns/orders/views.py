from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderItem
from django.urls import reverse
from .forms import OrderCreateForm
from basket.basket import Basket
from .serializers import OrderCreateSerializer


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in basket:
                discounted_price = item['product'].sell_price()
                OrderItem.objects.create(order=order, product=item['product'], price=discounted_price, quantity=item['quantity'])
            basket.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm(request=request)
    return render(request, 'order/create.html', {'basket': basket, 'form':form})


#------------------------API------------------------


class OrderCreateView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request):
        basket = Basket(request)
        if not basket:
            return Response(
                {"error": "Корзина пуста"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['user'] = request.user.id if request.user.is_authenticated else None

        serializer = OrderCreateSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()

            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].sell_price(),
                    quantity=item['quantity']
                )

            basket.clear()
            request.session['order_id'] = order.id

            response_data = {
                'order_id': order.id,
                'payment_url': reverse('payment:process', request=request),
                'total_cost': order.get_total_cost()
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

