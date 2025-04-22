from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from basket.basket import Basket


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in basket:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            basket.clear()
            return render(request, 'order/created.html', {'order': order, 'form': form})
    else:
        form = OrderCreateForm(request=request)
    return render(request, 'order/create.html', {'basket': basket, 'form':form})


