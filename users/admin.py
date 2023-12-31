from django.contrib import admin

from products.admin import BasketAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # fields = ('password', 'first_name', 'last_name')
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
