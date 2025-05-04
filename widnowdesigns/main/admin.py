from django.contrib import admin
from .models import Product, Category, ProductImaga


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',) }


class ProductImageInline(admin.TabularInline):
    model = ProductImaga
    extra = 3



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available', 'price', 'discount', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'discount']
    prepopulated_fields = {'slug': ('name',) }
    inlines = [ProductImageInline]
