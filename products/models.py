import msilib

from django.db import models

from users.models import User


class ProductCategory(models.Model):
    """Модель котегории"""
    name = models.CharField(verbose_name='Название', max_length=255, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товаров связь с котегорией"""
    name = models.CharField(verbose_name='Название', max_length=255, unique=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена', max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    image = models.ImageField(verbose_name='Изображение', upload_to='product')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Название: {self.name} | Категория: {self.category.name}'

    def short_description(self):
        if len(self.description) > 50:
            return self.description[:50] + '...'
        return self.description


class BasketQuerySet(models.QuerySet):
    """Добавляем методы в objects"""
    def total_sum(self):
        return sum(basket.product_sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    """Корзина товаров пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def product_sum(self):
        """Выводит сумму отпределенного товара корзины"""
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.product.name} for {self.user.username}'
