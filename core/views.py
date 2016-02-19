#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.conf import settings
from abstract import SettingsToContext, LoginRequiredMixin


class MainView(LoginRequiredMixin, SettingsToContext, TemplateView):
    template_name = 'main_view.html'

