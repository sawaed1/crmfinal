from decimal import Decimal
from rest_framework import serializers
from .models import Orders, OrderProduct
from products.models import Products
from customers.models import Customers
from customers.serializers import CustomersSerializer
from datetime import datetime
from django.utils import timezone

class OrderProductSerializer(serializers.ModelSerializer):
    # Для чтения возвращаем название товара вместо его id
    product = serializers.CharField(source='product.title', read_only=True)
    # Для записи используем поле product_id
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(),
        source='product'
    )
    # Берем цены из связанной модели продукта
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    price_purchase = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # Дополнительные вычисляемые поля:
    retail_total = serializers.SerializerMethodField()
    purchase_total = serializers.SerializerMethodField()
    difference = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = [
            'id',
            'product',
            'product_id',
            'quantity',
            'price_purchase',
            'price',
            'retail_total',
            'purchase_total',
            'difference'
        ]

    def validate(self, data):
        """
        Проверяем, что price и price_purchase заполнены.
        Если они не указаны, берем из продукта.
        """
        product = data.get("product")

        if "price" not in data or data["price"] is None:
            data["price"] = product.retail_price

        if "price_purchase" not in data or data["price_purchase"] is None:
            data["price_purchase"] = product.cost_price

        return data
    def get_retail_total(self, obj):
        # Используем значение из связанного продукта
        retail_price = obj.product.retail_price
        if retail_price is None or obj.quantity is None:
            return None
        return retail_price * obj.quantity

    def get_purchase_total(self, obj):
        purchase_price = obj.product.cost_price
        if purchase_price is None or obj.quantity is None:
            return None
        return purchase_price * obj.quantity

    def get_difference(self, obj):
        retail_total = self.get_retail_total(obj)
        purchase_total = self.get_purchase_total(obj)
        if retail_total is None or purchase_total is None:
            return None
        return retail_total - purchase_total


class OrdersSerializer(serializers.ModelSerializer):
    ready_time = serializers.DateTimeField(format="%m/%d/%Y, %I:%M %p")
    pickup_time = serializers.DateTimeField(format="%m/%d/%Y, %I:%M %p")
    created_at = serializers.DateTimeField(format="%m/%d/%Y, %I:%M %p", default=timezone.now, read_only=True)
    # Вложенное поле для промежуточной модели
    order_products = OrderProductSerializer(many=True, source='orderproduct_set')
    # Для чтения возвращаем подробные данные клиента
    customer = CustomersSerializer()

    # Вычисляемые поля:
    products_retail_total = serializers.SerializerMethodField()
    products_purchase_total = serializers.SerializerMethodField()
    products_difference = serializers.SerializerMethodField()
    order_total_amount = serializers.SerializerMethodField()


    class Meta:
        model = Orders
        fields = [
            'id', 'created_at', 'ready_time', 'pickup_time', 'order_type',
            'payment_method', 'payment_status', 'delivery_price', 'comment',
            'delivery_type', 'order_status', 'customer', 'order_products',
            'products_retail_total', 'products_purchase_total', 'products_difference', 'order_total_amount'
        ]

    def to_internal_value(self, data):
        """
        Конвертирует дату перед сохранением в базу.
        """
        for field in ['ready_time', 'pickup_time', 'created_at']:
            if field in data and isinstance(data[field], str):
                try:
                    # Конвертируем строку в datetime объект
                    data[field] = datetime.strptime(data[field], "%m/%d/%Y, %I:%M %p")
                except ValueError:
                    raise serializers.ValidationError({field: "Invalid date format. Use MM/DD/YYYY, hh:mm AM/PM"})

        return super().to_internal_value(data)

    def create(self, validated_data):
        #Извлечение вложенных данных клиента
        customer_data = validated_data.pop('customer', None)
        if customer_data:
            phone = customer_data.get('phone')
            #попытка найти клиента по номеру телефона
            customer, created = Customers.objects.get_or_create(phone=phone, defaults=customer_data)
            validated_data['customer'] = customer

        order_products_data = validated_data.pop('orderproduct_set')
        order = Orders.objects.create(**validated_data)
        for op_data in order_products_data:
            OrderProduct.objects.create(order=order, **op_data)
        return order

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer', None)
        if customer_data:
            # Если клиент уже существует, обновляем его поля
            customer = instance.customer
            for attr, value in customer_data.items():
                setattr(customer, attr, value)
            customer.save()
            validated_data['customer'] = customer  # гарантируем, что в validated_data теперь объект Customers

        order_products_data = validated_data.pop('orderproduct_set', None)
        # Обновляем поля заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if order_products_data is not None:
            # Здесь можно добавить логику обновления вложенных записей
            instance.orderproduct_set.all().delete()
            for op_data in order_products_data:
                OrderProduct.objects.create(order=instance, **op_data)
        return instance

    def get_products_retail_total(self, obj):
        total = sum(
            (op.product.retail_price * op.quantity)
            for op in obj.orderproduct_set.all()
            if op.product and op.quantity and op.product.retail_price is not None
        )
        return total

    def get_products_purchase_total(self, obj):
        total = sum(
            (op.product.cost_price * op.quantity)
            for op in obj.orderproduct_set.all()
            if op.product and op.quantity and op.product.cost_price is not None
        )
        return total

    def get_products_difference(self, obj):
        return self.get_products_retail_total(obj) - self.get_products_purchase_total(obj)

    def get_order_total_amount(self, obj):
        delivery = obj.delivery_price if obj.delivery_price is not None else Decimal('0.00')
        return self.get_products_retail_total(obj) + delivery
