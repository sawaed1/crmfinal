from django.urls import path
from .views import \
    OrdersListCreateView, \
    OrdersRetrieveUpdateDeleteView, \
    OrderProductListCreateView, \
    OrderProductRetrieveUpdateDeleteView

urlpatterns = [
    path('', OrdersListCreateView.as_view(), name='orders_api_list'),
    path('<int:pk>/', OrdersRetrieveUpdateDeleteView.as_view(), name='orders_api_detail'),
    path('<int:order_pk>/order_product/', OrderProductListCreateView.as_view(), name='order_product_api_list'),
    path('<int:order_pk>/order_product/<int:pk>/', OrderProductRetrieveUpdateDeleteView.as_view(), name='order_product_api_detail'),
]