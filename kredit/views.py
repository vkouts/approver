#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import render
from django.conf import settings
import uuid
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView, CreateView
from models import Kredit, SessionFiles
from django.contrib import messages
from core.abstract import SettingsToContext, LoginRequiredMixin
from forms import KreditForm, SessionFilesForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy

class KreditList(LoginRequiredMixin, SettingsToContext, ListView):
    template_name = 'kredit_list.html'
    model = Kredit
    paginate_by = settings.UNITS_PER_PAGE


class KreditDetail(LoginRequiredMixin, DetailView):
    template_name = 'kredit_detail.html'
    model = Kredit

    def get_context_data(self, **kwargs):
        context = super(KreditDetail, self).get_context_data(**kwargs)
        context['files'] = SessionFiles.objects.filter(sess=self.object.sess)
        return context


class KreditRequest(LoginRequiredMixin, CreateView):
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
            messages.success(request, 'Kredit data successfully saved')
            return HttpResponseRedirect(reverse_lazy('kredit_detail', kwargs={'pk': kredit.id}))
        form2 = self.form2(data=request.POST, files=request.FILES, prefix=self.form2_pref)
        if form2.is_valid() and request.FILES:
            my_file = SessionFiles(path_to=request.FILES.get('file'), sess=request.POST.get('files-sess'))
            my_file.save()
            return super(KreditRequest, self).post(request, *args, **kwargs)
        return super(KreditRequest, self).post(request, *args, **kwargs)


class MyKredits(LoginRequiredMixin, TemplateView):
    template_name = 'my_kredits.html'


class SearchKredit(LoginRequiredMixin, TemplateView):
    template_name = 'search_kredit.html'


class GroupKredits(LoginRequiredMixin, TemplateView):
    template_name = 'by_group.html'

