from rest_framework import serializers
from .models import Customers
from django.utils import timezone

class CustomersSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%m/%d/%Y, %I:%M %p", default=timezone.now, read_only=True)

    class Meta:
        model = Customers
        fields = '__all__'  # Выводим все поля