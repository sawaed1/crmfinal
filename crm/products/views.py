from django.shortcuts import render, redirect
from .models import Products
from django.views.generic import DetailView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework import filters
from .serializers import ProductsSerializer

# 📌 API: Получить список товаров и создать товар
class ProductsListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all().order_by('created_at')
    serializer_class = ProductsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

# 📌 API: Получить, обновить или удалить товар
class ProductsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all().order_by('created_at')
    serializer_class = ProductsSerializer