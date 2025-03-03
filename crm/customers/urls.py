from django.urls import path
from .views import CustomersListCreateView, CustomersRetrieveUpdateDeleteView

urlpatterns = [
    path('', CustomersListCreateView.as_view(), name='customers_api_list'),
    path('<int:pk>/', CustomersRetrieveUpdateDeleteView.as_view(), name='customers_api_detail'),
]