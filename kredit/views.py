#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from models import Kredit
from core.abstract import SettingsToContext, LoginRequiredMixin

class KreditList(LoginRequiredMixin, SettingsToContext, ListView):
    template_name = 'kredit_list.html'
    model = Kredit


class KreditDetail(LoginRequiredMixin, DetailView):
    template_name = 'kredit_detail.html'
    model = Kredit

class KreditRequest(LoginRequiredMixin, TemplateView):
    template_name = 'kredit_request.html'


class MyKredits(LoginRequiredMixin, TemplateView):
    template_name = 'my_kredits.html'


class SearchKredit(LoginRequiredMixin, TemplateView):
    template_name = 'search_kredit.html'


class GroupKredits(LoginRequiredMixin, TemplateView):
    template_name = 'by_group.html'

