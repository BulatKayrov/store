from django.urls import path

from .views import OrderCreateView, OrderDetailView, OrdersView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrdersView.as_view(), name='orders'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
