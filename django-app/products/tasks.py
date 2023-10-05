import datetime
from django.core.mail import send_mail
from celery import shared_task
from products.models import Order


@shared_task()
def send_email_before_due_date():
    today = datetime.datetime.today()

    tommorow = today + datetime.timedelta(days=1)
    order = Order.objects.filter(due_date__gt=today, due_date__lte=tommorow)
    for o in order:
        send_mail(
            "Payment reminder",
            "Please pay",
            "e-commerce@e-commerce.com",
            [o.client.email],
            fail_silently=False,
        )
