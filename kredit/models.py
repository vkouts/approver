#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from Bank.models import Office
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver



@python_2_unicode_compatible
class Kredit(models.Model):
    COMPLECT1 = ['kredit_user', 'kredit_approver']
    COMPLECT2 = ['kredit_user', 'kredit_approver', ['DB_Dagestan', 'DB_Moscow', 'DB_SKFO'], 'kredit_dskp']

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
    groups = models.ManyToManyField(Group, blank=True, null=True, verbose_name=_('Groups'))

    sess = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Session'))

    def get_cur_route(self):
        return KreditRoute.objects.filter(kredit=self).order_by('-id').last()

    class Meta:
        verbose_name = _('Kredit')
        verbose_name_plural = _('Kredits')

    def __str__(self):
        return '{surn} {name} {second}'.format(surn=self.surname, name=self.name, second=self.secondname)

@python_2_unicode_compatible
class KreditRoute(models.Model):
    color = models.CharField(max_length=16, verbose_name=_('Color'), default="black")
    kredit = models.ForeignKey(Kredit)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    stage = models.IntegerField(verbose_name=_('Stage'), default=0)
    prev_group = models.ForeignKey(Group, related_name='kreditroute_prevgroup', null=True, blank=True,
                                   verbose_name=_('Previous group'))
    cur_group = models.ForeignKey(Group, related_name='kreditroute_curgroup', null=True, blank=True,
                                  verbose_name=_('Current group'))
    next_group = models.ForeignKey(Group, related_name='kreditroute_nextgroup', null=True, blank=True,
                                   verbose_name=_('Next group'))
    cur_user = models.ForeignKey(User, related_name='kreditroute_curuser', null=True, blank=True,
                                 verbose_name=_('Current user'))
    comment = models.TextField(verbose_name=_('Comment'), null=True, blank=True)
    blinded_comment = models.TextField(verbose_name=_('Blinded comment'), null=True, blank=True)
    hide_comment = models.BooleanField(verbose_name=_('Hide comment'), default=False)
    session = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return '{id}_{date}'.format(date=self.creation_date.strftime('%d.%m.%Y %H:%M'), id=self.kredit.id)

    class Meta:
        verbose_name = _('Kredit route')
        verbose_name_plural = _('Kredit routes')

class SessionFiles(models.Model):
    sess = models.CharField(max_length=64, null=True, blank=True)
    path_to = models.FileField(upload_to='files/%Y/%m/%d/', null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)


    def extension(self):
        name, extension = os.path.splitext(self.path_to.name)
        return extension[1:] if len(extension) > 1 else extension

    def __unicode__(self):
        return str(self.id)


@receiver(post_save, sender=Kredit)
def kredit_post_init(instance, **kwargs):
    if instance.doc_complect == Kredit.FIRST_COMPLECT:
        my_complect = Kredit.COMPLECT1
    else:
        my_complect = Kredit.COMPLECT2
    my_route,res = KreditRoute.objects.get_or_create(
        kredit=instance,
        cur_group=Group.objects.get(name=my_complect[0]),
        next_group=Group.objects.get(name=my_complect[1]),
        comment=_('New credit was created'),
        cur_user=instance.user,
    )
    my_route.save()