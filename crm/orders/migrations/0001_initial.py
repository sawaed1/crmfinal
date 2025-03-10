# Generated by Django 5.1.6 on 2025-02-28 22:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за единицу')),
                ('price_purchase', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Закупочная цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='Продукт')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата/время создания')),
                ('ready_time', models.DateTimeField(verbose_name='Дата/время готовности на кухне')),
                ('pickup_time', models.DateTimeField(verbose_name='Дата/время выдачи клиенту')),
                ('order_type', models.CharField(choices=[('Pickup', 'Pickup'), ('Delivery', 'Delivery')], max_length=10, verbose_name='Тип выдачи заказа')),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Zelle', 'Zelle')], max_length=10, verbose_name='Способ оплаты')),
                ('payment_status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], max_length=15, verbose_name='Статус оплаты')),
                ('delivery_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена доставки')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий заказа')),
                ('delivery_type', models.CharField(blank=True, choices=[('Uber', 'Uber'), ('Local courier', 'Local courier')], max_length=20, null=True, verbose_name='Тип доставки')),
                ('order_status', models.CharField(choices=[('New', 'New'), ('Making', 'Making'), ('Made and packed', 'Made and packed'), ('Out of delivery', 'Out of delivery'), ('Handed', 'Handed'), ('Deleted', 'Deleted')], default='Новый', max_length=30, verbose_name='Статус заказа')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.customers', verbose_name='Клиент')),
                ('products', models.ManyToManyField(through='orders.OrderProduct', to='products.products', verbose_name='Проданные товары')),
            ],
            options={
                'verbose_name': 'Orders',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders', verbose_name='Заказ'),
        ),
    ]
