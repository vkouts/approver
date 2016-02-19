#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Office

# Register your models here.
@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    pass