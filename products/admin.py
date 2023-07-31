from django.contrib import admin

from .models import Basket, Product, ProductCategory

# class ProductCategoryInline(admin.TabularInline):
#     model = ProductCategory
#     fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (('name', 'image'), 'description', ('price', 'quantity'), 'category',)
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name', 'description', 'category')
    list_filter = ('name', 'price', 'quantity', 'category')
    ordering = ('name', 'price', 'quantity', 'category')


@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fields = ('name', 'description')


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'create_at')
    readonly_fields = ('create_at',)
    extra = 0
