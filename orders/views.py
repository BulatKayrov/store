from django.urls import reverse_lazy
from django.views import generic

from products.models import Basket

from .forms import OrderForm
from .models import Order


class OrderCreateView(generic.CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        order_user = super(OrderCreateView, self).post(request, *args, **kwargs)
        order = Order.objects.filter(initial=self.request.user).last()
        baskets = Basket.objects.filter(user=order.initial)
        order.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': round(float(baskets.total_sum()), 2),
        }
        baskets.delete()
        order.save()

        return order_user

    def form_valid(self, form):
        form.instance.initial = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        return context


class OrdersView(generic.ListView):
    template_name = 'orders/orders.html'
    model = Order
    
    def get_queryset(self):
        queryset = super(OrdersView, self).get_queryset()
        print(queryset)
        return queryset.filter(initial=self.request.user)


class OrderDetailView(generic.DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Заказ № {self.object.pk}'
        return context
