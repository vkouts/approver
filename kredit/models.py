#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Bank.models import Office
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Kredit(models.Model):
    FIRST_COMPLECT = '1'
    SECOND_COMPLECT = '2'
    COMPLECT = (
        (FIRST_COMPLECT, 'первый'),
        (SECOND_COMPLECT, 'второй'),
    )
    KREDIT = (
        ('A', 'ЭКСПРЕСС-НАЛИЧНЫМИ'),
        ('B', 'НАШ ПЕНСИОНЕР'),
        ('C', 'НБКИ')
    )
    STATUS_NEW = 'N'
    STATUS_DISCARD = 'D'
    STATUS_APPROVE = 'A'
    STATUS_REVIEW = 'R'
    STATUS_TRANSFER = 'T'
    STATUS_REWRITE = 'B'
    STATUS_APPRREWRITE = 'C'
    STATUS_DONE = 'F'
    STATUS_MIDREWRITE = 'M'
    STATUS = (
        (STATUS_NEW, 'Новая'),
        (STATUS_DISCARD, 'Отклонена'),
        (STATUS_APPROVE, 'Одобрена'),
        (STATUS_REVIEW, 'На рассмотрении'),
        (STATUS_TRANSFER, 'В процессе передачи'),
        (STATUS_REWRITE, 'Отправлено на доработку'),
        (STATUS_APPRREWRITE, 'На доработку согласователю'),
        (STATUS_DONE, 'Доработано'),
        (STATUS_MIDREWRITE, 'Промежуточная доработка'),
    )
    APPR_STATUS = (
        ('0', 'Решения нет'),
        ('A', 'Одобрен'),
        ('R', 'Отклонен'),
    )
    LEVELS = (
        ('0', 'Кредитчики'),
        ('1', 'Согласователи'),
        ('2', 'Безопасность'),
        ('3', 'ДСКП Выдача'),
    )

    office = models.ForeignKey(Office, verbose_name=_('Office'))
    name = models.CharField(max_length=512, verbose_name=_('Name'), default='')
    surname = models.CharField(max_length=512, verbose_name=_('Surname'), default='')
    secondname = models.CharField(max_length=512, verbose_name=_('Second Name'), default='')
    user = models.ForeignKey(User, verbose_name=_('Employee'))
    sum = models.FloatField(verbose_name=_('Sum'), default=0)
    doc_complect = models.CharField(max_length=1, choices=COMPLECT, default='1', verbose_name=_('Complect'))
    kred_mode = models.CharField(max_length=1, choices=KREDIT, default='A', verbose_name=_('Kredit kind'))
    kred_comment = models.TextField(null=True, blank=True, verbose_name=_('Comment'))
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation data'))
    status = models.CharField(max_length=1, choices=STATUS, default='N', verbose_name=_('Kredit status'))
    link = models.ForeignKey('self', null=True, blank=True, verbose_name=_('Link to other complect'))
    current_level = models.CharField(max_length=1, choices=LEVELS, default='0', verbose_name=_('Level'))
    db_status = models.CharField(max_length=1, choices=APPR_STATUS, default='0', verbose_name=_('DB status'))
    dskp_status = models.CharField(max_length=1, choices=APPR_STATUS, default='0', verbose_name=_('DSKP status'))

    sess = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Session'))

    class Meta:
        verbose_name = _('Kredit')
        verbose_name_plural = _('Kredits')

    def __str__(self):
        return '{surn} {name} {second}'.format(surn=self.surname, name=self.name, second=self.secondname)



class SessionFiles(models.Model):
    sess = models.CharField(max_length=64, null=True, blank=True)
    path_to = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)