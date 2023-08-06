from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    STATUSES = (
        (0, 'Создан'),
        (1, 'Оплачен'),
        (2, 'В пути'),
        (3, 'Доставлен'),
    )

    first_name = models.CharField(verbose_name='Имя', max_length=100)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    email = models.CharField(verbose_name='Почта', max_length=255)
    address = models.CharField(verbose_name='Адресс', max_length=255)
    basket_history = models.JSONField(verbose_name='История закозов', default=dict)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    initial = models.ForeignKey(User, verbose_name='Инициатор', on_delete=models.CASCADE)
    status = models.SmallIntegerField(verbose_name='Статус', default=0, choices=STATUSES)

    def __str__(self):
        return f'Order #{self.id} {self.first_name} {self.last_name}'

    def get_status_display(self):
        for i in self.STATUSES:
            if i[0] == self.status:
                return i[1]
