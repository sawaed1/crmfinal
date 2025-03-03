from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from rest_framework import generics
from .serializers import OrdersSerializer, OrderProductSerializer
from .models import Orders, OrderProduct

class OrderProductListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        order_pk = self.kwargs.get('order_pk')
        if order_pk:
            return OrderProduct.objects.filter(order__id=order_pk)
        return OrderProduct.objects.all()

class OrderProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        order_pk = self.kwargs.get('order_pk')
        if order_pk:
            return OrderProduct.objects.filter(order__id=order_pk)
        return OrderProduct.objects.all()


class OrdersListCreateView(generics.ListCreateAPIView):
    queryset = Orders.objects.all().order_by('created_at')
    serializer_class = OrdersSerializer

class OrdersRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all().order_by('created_at')
    serializer_class = OrdersSerializer