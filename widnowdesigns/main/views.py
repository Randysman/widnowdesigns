from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Category
from basket.forms import BasketAddProductForm
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer


def popular_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'main/index/index.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    basket_product_form = BasketAddProductForm
    return render(request, 'main/product/detail.html', {'product': product, 'basket_product_form': basket_product_form})


def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 5)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        paginator = Paginator(products.filter(category=category), 5)
        current_page = paginator.page(int(page))
    return render(request, 'main/product/list.html', {'category': category, 'categories': categories, 'products': current_page, 'slug': category_slug})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )

    @action(methods=['get', 'post'], detail=True)
    def category(self, request, pk):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})