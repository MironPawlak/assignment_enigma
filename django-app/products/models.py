import os
from django.db import models
from django.dispatch import receiver
from django_advance_thumbnail import AdvanceThumbnailField
from django.core.mail import send_mail
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    image = models.ImageField()
    thumbnail = AdvanceThumbnailField(source_field='image', upload_to='thumbnails/', null=True, blank=True,
                                      size=(200, 20000))

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    delivery_address = models.CharField(max_length=512)
    product_List = models.ManyToManyField(Product, through="ProductList", through_fields=("order", "product"))
    order_date = models.DateField()
    due_date = models.DateField()
    sum_price = models.DecimalField(decimal_places=2, max_digits=15)


class ProductList(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when
    Image is deleted e.g from Django admin
    """
    try:
        os.remove(instance.image.path)
        os.remove(instance.thumbnail.path)
    except FileNotFoundError:
        pass


@receiver(models.signals.post_save, sender=Order)
def send_confirmation_email(sender, instance, **kwargs):
    """
    Sends confirmation email after order is created
    """
    send_mail(
        "Order Confirmation",
        "I confirm order",
        "e-commerce@e-commerce.com",
        [instance.client.email],
        fail_silently=False,
    )
