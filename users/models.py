from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    """Расширяем и переопределяем модель User. Добавлем поле фотографии пользователя"""
    images = models.ImageField(upload_to='users', verbose_name='Фотография пользователя')
    is_verified_email = models.BooleanField(default=False)  # Подтверждение почты

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = reverse('users:email', kwargs={'email': self.user.email, 'code': self.code})
        ver_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждения учетной записи для {self.user.username}'
        message = f'Для подтверждения учетной записи {self.user.username} перейдите по ссылке {ver_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
