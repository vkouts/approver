# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.contrib.auth.models import Group
__author__ = 'kvn'


register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='in_group')
def in_group(user, groups):
    for im in groups:
        if im in user.groups.all():
            return True
    return False

