# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'kvn'
def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
