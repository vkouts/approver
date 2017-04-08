#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from abstract import SettingsToContext, LoginRequiredMixin
from kredit.views import BagesMixin


class MainView(LoginRequiredMixin, SettingsToContext, BagesMixin, TemplateView):
    template_name = 'main_view.html'


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


