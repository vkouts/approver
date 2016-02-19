# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
__author__ = 'kvn'

class SettingsToContext(View):

    def get_context_data(self, **kwargs):
        context = super(SettingsToContext, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context


class LoginRequiredMixin(object):
    """
    Mixin for common based views for authorization check
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        print context
        return JsonResponse(
            context,
            **response_kwargs
        )

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

