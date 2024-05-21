from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ["pk", "username", "is_staff", "is_superuser"]
    list_display_links = ["pk"]
    readonly_fields = []
    list_filter = []
    ordering = ["-pk"]
    verbose_name = "User"
    verbose_name_plural = "Users"

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "feeds",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
