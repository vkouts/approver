# -*- coding: utf-8 -*-
__author__ = 'kvn'
from django.conf.urls import patterns, url
from views import KreditList, KreditRequest, MyKredits, SearchKredit

urlpatterns = patterns('',
    url(r'^search/', SearchKredit.as_view(), name='search'),
    url(r'^my/', MyKredits.as_view(), name='my_kredits'),
    url(r'^request/', KreditRequest.as_view(), name='kredit_request'),
    url(r'^list/$', KreditList.as_view(), name='kredit_list'),
)
