#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Office(models.Model):
     name = models.CharField(verbose_name=_('Name'), max_length=512)

     def __str__(self):
         return self.name

     class Meta:
         ordering = ['name']
         verbose_name = _('Office')
         verbose_name_plural = _('Offices')

