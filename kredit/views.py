#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import render
from django.conf import settings
import uuid
from django.contrib.auth.models import User, Group
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from models import Kredit, SessionFiles, KreditRoute
from django.contrib import messages
from core.abstract import SettingsToContext, LoginRequiredMixin
from forms import KreditForm, SessionFilesForm, KreditControlForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy, reverse

class BagesMixin(View):

    def get_context_data(self, **kwargs):
        context = super(BagesMixin, self).get_context_data(**kwargs)
        if Group.objects.get(name=settings.ADMIN_APPROVER) in self.request.user.groups.all() or \
            Group.objects.get(name=settings.FIRST_LINE_APPROVER) in self.request.user.groups.all() or \
            Group.objects.get(name=settings.SECOND_LINE_APPROVER) in self.request.user.groups.all():
            context['all_requests'] = Kredit.objects.all().count()
            context['new_requests'] = Kredit.objects.filter(
                groups__name=settings.FIRST_LINE_APPROVER
            ).filter(status__in=[Kredit.STATUS_NEW, Kredit.STATUS_DONE]).count()
        elif Group.objects.get(name=settings.CREATOR_GROUP) in self.request.user.groups.all():
            context['my_requests'] = Kredit.objects.filter(user=self.request.user).count()
        return context


class KreditList(LoginRequiredMixin, SettingsToContext, BagesMixin, ListView):
    template_name = 'kredit_list.html'
    model = Kredit
    paginate_by = settings.UNITS_PER_PAGE


class KreditDetail(LoginRequiredMixin,  SingleObjectMixin, SettingsToContext, BagesMixin, FormView):
    template_name = 'kredit_detail.html'
    model = Kredit
    form_class = KreditControlForm


    def get_context_data(self, **kwargs):
        self.object = self.model.objects.get(pk=self.kwargs.get('pk'))
        context = super(KreditDetail, self).get_context_data(**kwargs)
        # self.obj = self.model.objects.get(pk=self.kwargs.get('pk'))
        my_sess = uuid.uuid1()
        context['files'] = SessionFiles.objects.filter(sess=self.object.sess)
        context['routes'] = KreditRoute.objects.filter(kredit=self.object).order_by('id')
        context['settings'] = settings
        context['form'] = KreditControlForm(initial={'sess': my_sess})
        if self.object.status in (Kredit.STATUS_DISCARD, Kredit.STATUS_APPROVE):
            context['finish'] = True
        else:
            context['finish'] = False
        return context

    def post(self, request, *args, **kwargs):
        if request.FILES:
            my_file = SessionFiles(path_to=request.FILES.get('file'), sess=request.POST.get('sess'))
            my_file.save()


        self.object = self.get_object()
        prev_route = self.object.get_cur_route()

        # Просто комментарий
        if 'commentButton' in request.POST.keys():
            my_route = KreditRoute.objects.create(
                color='#32c8de',
                kredit=self.object,
                stage=prev_route.stage,
                prev_group=prev_route.prev_group,
                cur_group=prev_route.cur_group,
                next_group=prev_route.next_group,
                cur_user=request.user,
                comment=request.POST.get('comment', ''),
                session=request.POST.get('sess', '')
            )
            my_route.save()
        elif 'takeButton' in request.POST.keys():
            my_route = KreditRoute.objects.create(
                color='#32c8de',
                kredit=self.object,
                stage=prev_route.stage,
                prev_group=prev_route.cur_group,
                cur_group=prev_route.next_group,
                next_group=prev_route.next_group,
                cur_user=request.user,
                blinded_comment=_('User from group %s take credit for review') % prev_route.next_group.name,
                comment=_('User %s take credit for review') % request.user.get_full_name(),
                session=request.POST.get('sess', '')
            )
            my_route.save()
        elif 'improveButton' in request.POST.keys():
            pass
        elif 'acceptButton' in request.POST.keys():
            if self.object.doc_complect == self.object.FIRST_COMPLECT:
                self.object.status = self.object.STATUS_APPROVE
                my_route = KreditRoute.objects.create(
                    color='#5cb85c',
                    kredit=self.object,
                    stage=0,
                    prev_group=prev_route.cur_group,
                    cur_group=prev_route.cur_group,
                    next_group=prev_route.next_group,
                    cur_user=request.user,
                    comment=request.POST.get('comment', ''),
                    session=request.POST.get('sess', '')
                )
                my_route.save()
                self.object.save(update_fields=['status'])
        elif 'declineButton' in request.POST.keys():
            if self.object.doc_complect == self.object.FIRST_COMPLECT:
                self.object.status = self.object.STATUS_DISCARD
                my_route = KreditRoute.objects.create(
                    color='#d9534f',
                    kredit=self.object,
                    stage=0,
                    prev_group=prev_route.cur_group,
                    cur_group=prev_route.cur_group,
                    next_group=prev_route.next_group,
                    cur_user=request.user,
                    comment=request.POST.get('comment', ''),
                    session=request.POST.get('sess', '')
                )
                my_route.save()
                self.object.save(update_fields=['status'])
        return super(KreditDetail, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('kredit_detail', kwargs={'pk': self.object.pk})


class KreditRequest(LoginRequiredMixin, SettingsToContext, BagesMixin, CreateView):
    template_name = 'kredit_request.html'
    model = Kredit
    form_class = KreditForm
    form2 = SessionFilesForm
    form_class_pref = 'kred'
    form2_pref = 'files'

    def get_context_data(self, **kwargs):
        context = super(KreditRequest, self).get_context_data(**kwargs)
        my_sess = uuid.uuid1()
        context['form'] = self.form_class(prefix=self.form_class_pref, initial={'sess': my_sess})
        context['form2'] = self.form2(prefix=self.form2_pref, initial={'sess': my_sess})
        return context

    def post(self, request, *args, **kwargs):
        form1 = self.form_class(data=request.POST,  prefix=self.form_class_pref)
        if form1.is_valid():
            kredit = form1.save(commit=False)
            kredit.user = request.user
            kredit.status = Kredit.STATUS_NEW
            kredit.save()
            if kredit.doc_complect == Kredit.FIRST_COMPLECT and len(Kredit.COMPLECT1) > 1:
                kredit.groups.add(Group.objects.get(name=Kredit.COMPLECT1[1]))
            if kredit.doc_complect == Kredit.SECOND_COMPLECT and len(Kredit.COMPLECT2) > 1:
                kredit.groups.add(Group.objects.get(name=Kredit.COMPLECT2[1]))
            kredit.save()
            messages.success(request, 'Kredit data successfully saved')
            return HttpResponseRedirect(reverse_lazy('kredit_detail', kwargs={'pk': kredit.id}))
        form2 = self.form2(data=request.POST, files=request.FILES, prefix=self.form2_pref)
        if form2.is_valid() and request.FILES:
            my_file = SessionFiles(path_to=request.FILES.get('file'), sess=request.POST.get('files-sess'))
            my_file.save()
            return super(KreditRequest, self).post(request, *args, **kwargs)
        return super(KreditRequest, self).post(request, *args, **kwargs)


class MyKredits(LoginRequiredMixin, SettingsToContext, BagesMixin, ListView):
    template_name = 'kredit_list.html'
    model = Kredit

    def get_queryset(self):
        qs = None
        if self.kwargs.get('group', '') == settings.CREATOR_GROUP:
            qs = self.model.objects.filter(user=self.request.user)
        return qs


class SearchKredit(LoginRequiredMixin, SettingsToContext, BagesMixin, ListView):
    model = Kredit
    template_name = 'kredit_list.html'
    paginate_by = settings.UNITS_PER_PAGE

    def get_queryset(self):
        search_str = self.request.GET.get('searchstr', '')
        if search_str.isdigit():
            my_creds = self.model.objects.filter(id=search_str)
        else:
            my_creds = self.model.objects.filter(Q(name__istartswith=search_str)|Q(surname__istartswith=search_str))
        return my_creds

class GroupKredits(LoginRequiredMixin, SettingsToContext, BagesMixin, ListView):
    template_name = 'kredit_list.html'
    model = Kredit

    def get_queryset(self):
        my_group = self.kwargs.get('group')
        return self.model.objects.filter(groups__name=my_group).filter(status__in=[Kredit.STATUS_NEW, Kredit.STATUS_DONE])

