from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширяем и переопределяем модель User. Добавлем поле фотографии пользователя"""
    images = models.ImageField(upload_to='users', verbose_name='Фотография пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
