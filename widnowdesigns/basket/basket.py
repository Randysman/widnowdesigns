from decimal import Decimal
from django.conf import settings
from main.models import Product


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket


    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()


    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item["total_price"] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())


    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]


    def get_total_price(self):
        total = sum((Decimal(item['price']) - (Decimal(item['price'])
                    * Decimal(item['product'].discount / 100))) * item['quantity']
                    for item in self.basket.values())
        return format(total, '.2f')