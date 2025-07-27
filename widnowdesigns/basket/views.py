from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Product
from .basket import Basket
from .forms import BasketAddProductForm
from .serializers import BasketItemSerializer, BasketAddProductSerializer


@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('basket:basket_detail')


@require_POST
def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product)
    return redirect('basket:basket_detail')


def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html', {'basket': basket})


#------------------------API------------------------


class BasketDetail(APIView):
    # permission_classes = (IsAuthenticated, )

    def get(self, request):
        basket = Basket(request)
        serializer = BasketItemSerializer(list(basket.__iter__()), many=True)

        return Response({
            'items': serializer.data,
            'total_items': len(basket),
            'total_price': basket.get_total_price()
        })


class BasketAddView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, product_id):
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)

        serializer = BasketAddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        basket.add(
            product=product,
            quantity=serializer.validated_data['quantity'],
            override_quantity=serializer.validated_data.get('override', False)
        )

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)


class BasketRemoveView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, product_id):
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.remove(product)
        return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)