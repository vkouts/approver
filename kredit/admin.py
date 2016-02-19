#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Kredit

@admin.register(Kredit)
class KreditAdmin(admin.ModelAdmin):
    pass