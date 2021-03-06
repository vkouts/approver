# -*- coding: utf-8 -*-
__author__ = 'kvn'
from django.conf.urls import url
from views import KreditList, KreditRequest, MyKredits, SearchKredit, GroupKredits,KreditDetail

urlpatterns = [
    url(r'^group/(?P<group>\w+)/', GroupKredits.as_view(), name='by_group'),
    url(r'^search/', SearchKredit.as_view(), name='search'),
    url(r'^my/(?P<group>\w+)/', MyKredits.as_view(), name='my_kredits'),
    url(r'^request/', KreditRequest.as_view(), name='kredit_request'),
    url(r'^list/$', KreditList.as_view(), name='kredit_list'),
    url(r'^detail/(?P<pk>\d+)/$', KreditDetail.as_view(), name='kredit_detail'),
]
