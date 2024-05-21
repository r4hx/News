from django.contrib import admin
from django.contrib.auth.models import Group

from Account.models import CustomGroup


class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_display_links = ["pk"]


admin.site.unregister(Group)
admin.site.register(CustomGroup, CustomGroupAdmin)
