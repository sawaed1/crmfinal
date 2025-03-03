from django.urls import path
from . import views
from .views import ProductsListCreateView, ProductsRetrieveUpdateDeleteView

urlpatterns = [

    path('', ProductsListCreateView.as_view(), name='products_api_list'),
    path('<int:pk>/', ProductsRetrieveUpdateDeleteView.as_view(), name='products_api_detail'),
]