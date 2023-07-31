from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class UserLoginView(views.LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(generic.CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')


class UserLogoutView(views.LogoutView):
    next_page = reverse_lazy('users:login')


class ProfileUpdateView(generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        """Переопределяем перенаправление, в args передаем id пользователя"""

        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(generic.TemplateView):
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(redirect_to=reverse('products:index'))

# def login(request):
#     """Вью авторизации пользователя"""
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request=request, user=user)
#                 return HttpResponseRedirect(redirect_to=reverse('products:index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'users/login.html', context=context)


# def register(request):
#     """Вью регистрации пользователя. Перенаправлении на логин"""
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(redirect_to=reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'users/register.html', context=context)


# @login_required
# def profile(request):
#     """Вью обновление данных пользователя"""
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(redirect_to=reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     # baskets = Basket.objects.filter(user=request.user)
#     context = {
#         'form': form,
#         'title': 'Store - профиль',
#         'baskets': Basket.objects.filter(user=request.user),
#         # 'total_sum': sum(i.product_sum() for i in baskets),  # считаем общую сумму
#         # 'total_quantity': sum(i.quantity for i in baskets),  # считаем общее кол-во товаров
#     }
#     return render(request, 'users/profile.html', context=context)


# def user_logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(redirect_to=reverse('products:index'))
