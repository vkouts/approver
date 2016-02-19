#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView

class KreditList(TemplateView):
    template_name = 'list_kredits.html'

    def get_context_data(self, **kwargs):
        context = super(KreditList, self).get_context_data()
        context['settings'] = settings
        return context


class KreditRequest(View):
    pass


class MyKredits(View):
    pass


class SearchKredit(View):
    pass