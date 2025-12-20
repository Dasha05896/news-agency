from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Redactor, Newspaper, Topic


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):

