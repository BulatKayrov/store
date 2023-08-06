from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User

from .tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    """Форма авторизации"""
    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите пароль'}
    ))


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email']

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите пароль'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя'}
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}
    ))

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.pk)
        return user


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'images', 'username', 'email']

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4'}
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4'}
    ))
    images = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-label'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'readonly': True}
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control py-4', 'readonly': True}
    ))
