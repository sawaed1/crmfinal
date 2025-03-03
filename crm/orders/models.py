from django.db import models
from django.urls import reverse
from products.models import Products
from customers.models import Customers
from datetime import datetime


class Orders(models.Model):

    ORDER_TYPE_CHOICES = (
        ("Pickup", "Pickup"),
        ("Delivery", "Delivery"),
    )
    PAYMENT_METHOD_CHOICES = (
        ("Cash", "Cash"),
        ("Zelle", "Zelle"),
    )
    PAYMENT_STATUS_CHOICES = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
    )
    ORDER_STATUS_CHOICES = (
        ("New", "New"),
        ("Making", "Making"),
        ("Made and packed", "Made and packed"),
        ("Out of delivery", "Out of delivery"),
        ("Handed", "Handed"),
        ("Deleted", "Deleted"),
    )
    DELIVERY_TYPE_CHOICES = (
        ("Uber", "Uber"),
        ("Local courier", "Local courier"),
    )

    created_at = models.DateTimeField('Дата/время создания', auto_now_add=True)
    ready_time = models.DateTimeField('Дата/время готовности на кухне')
    pickup_time = models.DateTimeField('Дата/время выдачи клиенту')
    order_type = models.CharField("Тип выдачи заказа", max_length=10, choices=ORDER_TYPE_CHOICES)
    payment_method = models.CharField("Способ оплаты", max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField("Статус оплаты", max_length=15, choices=PAYMENT_STATUS_CHOICES)
    delivery_price = models.DecimalField("Цена доставки", max_digits=10, decimal_places=2, blank=True, null=True)
    comment = models.TextField("Комментарий заказа", blank=True, null=True)
    delivery_type = models.CharField("Тип доставки", max_length=20, choices=DELIVERY_TYPE_CHOICES, blank=True, null=True)
    order_status = models.CharField("Статус заказа", max_length=30, choices=ORDER_STATUS_CHOICES, default="Новый")
    products = models.ManyToManyField(Products, through='OrderProduct', verbose_name="Проданные товары")
    customer = models.ForeignKey(
        Customers,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Клиент"
    )

    def __str__(self):
        created_at = self.created_at
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")  # Преобразуем строку в datetime
        return f"Order {self.id} - {self.order_status} - {created_at.strftime('%m/%d/%Y, %I:%M %p')}"

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'


class OrderProduct(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена за единицу", max_digits=10, decimal_places=2)
    price_purchase = models.DecimalField("Закупочная цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x{self.quantity} (Заказ {self.order.id})"

