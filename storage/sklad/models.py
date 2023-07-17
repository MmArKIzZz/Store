from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin



class Products_in_storage(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=50)
    discription =  models.CharField(max_length=500,blank=True)

    def __str__(self):
        return f'{self.name}  {self.amount}'
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # для суперпользователя отображаются все записи

        # Для обычных пользователей отображаются только их собственные записи
        return qs.filter(user=request.user)
class OrderOut(models.Model):
    OPTIONS = (
        ('На рассмотрении', 'На рассмотрении'),
        ('Подготовка к отправке', 'Подготовка к отправке'),
        ('В пути', 'В пути'),
        ('Прибыл в пункт назначения', 'Прибыл в пункт назначения'),
    )
    product = models.ForeignKey(Products_in_storage, on_delete=models.SET_NULL, null=True, related_name="order_out_product")
    amount = models.IntegerField()
    worker = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="order_out_worker")  # Поле worker для выбора пользователей из группы "work"
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="order_out_user")  # Поле user для выбора пользователя
    status = models.CharField(max_length=50, choices=OPTIONS)

    def clean(self):
        if self.amount > self.product.amount:
            raise ValidationError("Выбранное количество превышает количество продукта на складе.")

    def __str__(self):
        return f'{self.product}  {self.user} {self.status}'

# Сигналы для автоматического уменьшения количества товара при изменении статуса заказа


@receiver(post_save, sender=OrderOut)
def update_product_amount(sender, instance, **kwargs):
    if instance.status == 'Подготовка к отправке':
        product = instance.product
        product.amount -= instance.amount
        product.save()
class Delivers(models.Model):
    amount = models.IntegerField()
    OPTIONS = (
        ('Подготовка к отправке', 'Подготовка к отправке'),
        ('В пути', 'В пути'),
        ('Прибыл в пункт назначения', 'Прибыл в пункт назначения'),
    )
    product = models.ForeignKey(Products_in_storage, on_delete=models.SET_NULL, null=True, related_name="deliver_product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, choices=OPTIONS)

    def __str__(self):
        return f'{self.product}  {self.user}  {self.status}'


# Сигналы для автоматического изменения количества товара при изменении статуса доставки


@receiver(post_save, sender=Delivers)
def update_product_amount(sender, instance, **kwargs):
    if instance.status == 'Прибыл в пункт назначения':
        product = instance.product
        product.amount += instance.amount
        product.save()