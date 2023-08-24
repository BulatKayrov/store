import uuid
from datetime import timedelta

from celery import shared_task
from celery.schedules import crontab
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from products.models import Product
from store.celery import app
from .models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()


@shared_task
def spam_sale():
    res = ''
    product = Product.objects.all()
    for item in product:
        res += f'Product name: {item.name} new price - {item.price}\n'
    for user in User.objects.all():
        send_mail(
            subject='Sale products',
            message=res,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


app.conf.beat_schedule = {
    'send_spam_every_1_min': {
        'task': 'users.tasks.spam_sale',
        'schedule': crontab()
    }
}

# celery -A store beat ## Запускает Celery Beat, чтобы он следил за расписанием
