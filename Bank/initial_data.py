# -*- coding: utf-8 -*-
__author__ = 'kvn'
from django.contrib.auth.models import User, Group
from django.conf import settings

def load_data():
    create_default_users()
    create_default_groups()

def create_default_users():
    if User.objects.filter(username='admin').count() == 0:
        admin = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@user.net'
        )
        admin.save()

def create_default_groups():
    gr, res = Group.objects.get_or_create(name=settings.CREATOR_GROUP)
    gr, res = Group.objects.get_or_create(name=settings.ADMIN_CREATOR_GROUP)
    gr, res = Group.objects.get_or_create(name=settings.FIRST_LINE_APPROVER)
    gr, res = Group.objects.get_or_create(name=settings.SECOND_LINE_APPROVER)
    gr, res = Group.objects.get_or_create(name=settings.SECURITY_APPROVER_PREFIX)
    gr, res = Group.objects.get_or_create(name=settings.ADMIN_APPROVER)


