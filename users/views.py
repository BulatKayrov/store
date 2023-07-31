from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from products.models import Basket
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):
    """Вью авторизации пользователя"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request=request, user=user)
                return HttpResponseRedirect(redirect_to=reverse('products:index'))
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context=context)


def register(request):
    """Вью регистрации пользователя. Перенаправлении на логин"""
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)


@login_required
def profile(request):
    """Вью обновление данных пользователя"""
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    # baskets = Basket.objects.filter(user=request.user)
    context = {
        'form': form,
        'title': 'Store - профиль',
        'baskets': Basket.objects.filter(user=request.user),
        # 'total_sum': sum(i.product_sum() for i in baskets),  # считаем общую сумму
        # 'total_quantity': sum(i.quantity for i in baskets),  # считаем общее кол-во товаров
    }
    return render(request, 'users/profile.html', context=context)


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(redirect_to=reverse('products:index'))

