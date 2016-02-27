#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Kredit, SessionFiles, KreditRoute

@admin.register(Kredit)
class KreditAdmin(admin.ModelAdmin):
    pass

@admin.register(SessionFiles)
class SessionFilesAdmin(admin.ModelAdmin):
    pass

@admin.register(KreditRoute)
class KreditRouteAdmin(admin.ModelAdmin):
    pass
