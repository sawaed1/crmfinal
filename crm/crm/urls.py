from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/products/', include('products.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/orders/', include('orders.urls')),
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('customers/', include('customers.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)