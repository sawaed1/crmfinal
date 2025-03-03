from .models import Customers
from rest_framework import generics, filters
from .serializers import CustomersSerializer

class CustomersListCreateView(generics.ListCreateAPIView):
    queryset = Customers.objects.all().order_by('created_at')
    serializer_class = CustomersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone']

class CustomersRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customers.objects.all().order_by('created_at')
    serializer_class = CustomersSerializer