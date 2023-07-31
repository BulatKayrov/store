from django.contrib import admin
from .models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # fields = ('password', 'first_name', 'last_name')
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    inlines = (BasketAdmin,)
