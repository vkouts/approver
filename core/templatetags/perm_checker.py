# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'kvn'

from django import template
from django.conf import settings
from django.contrib.auth.models import Group


register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

# @register.filter(name='is_current')
# def is_current(user):
#     my_employ = Employee.objects.get(user=user)
#     return True
#
@register.filter(name='is_security_approver')
def is_security_approver(user):
    all_user_groups = user.groups.all()
    my_flag = False
    for im in all_user_groups:
        if im.name.startswith(u'DB'):
            my_flag = True
            break
    return my_flag

