# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local Django
from .models import Account


# Register your  models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "last_login",
        "date_joined",
        "is_active",
    )
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",)

    filter_horizontal = ()  # for making password read only
    list_filter = ()  # for making password read only
    fieldsets = ()  # for making password read only


admin.site.register(Account, AccountAdmin)
