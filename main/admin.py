# Register your models here.

from django.contrib import admin
from main.models import User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
