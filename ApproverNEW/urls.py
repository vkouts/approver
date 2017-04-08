#-*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from core.views import MainView
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^kredit/', include('kredit.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main_view'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
