#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.conf import settings


class MainView(TemplateView):
    template_name = 'main_view.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context
