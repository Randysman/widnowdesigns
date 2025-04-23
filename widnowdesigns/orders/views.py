from django.shortcuts import render, redirect
from .models import OrderItem
from django.urls import reverse
from .forms import OrderCreateForm
from basket.basket import Basket


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


