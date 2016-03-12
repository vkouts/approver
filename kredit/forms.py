# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.conf import settings
import embedded_media as emb
from models import Kredit, SessionFiles
from ckeditor.widgets import CKEditorWidget

__author__ = 'kvn'

class SessionFilesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SessionFilesForm, self).__init__(*args, **kwargs)
        self.fields['sess'].required = True

    class Media:
        js = (
            emb.JS("""
            $(document).ready(function(){
                Dropzone.options.myDropzone={
                    paramName: "files-path_to",
                }
            });"""),
            'js/dropzone.js',
        )
        css = {'all': ('css/dropzone.css', ) }

    class Meta:
        model = SessionFiles
        fields = ('sess', 'path_to' )
        widgets = {'sess': forms.HiddenInput()}

class KreditForm(forms.ModelForm):
    #comment = forms.CharField(widget=TinyMCE(attrs={'cols': 120, 'rows': 10}))
    kred_link = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Kredit
        fields = ('sess', 'office', 'name', 'surname', 'secondname', 'kred_mode', 'doc_complect',
                  'sum', 'kred_comment', 'kred_link')
        widgets = {'sess': forms.HiddenInput()}

    class Media:
        js = (
            'js/show_kredits.js',
            'js/dropzone.js',
        )


    def __init__(self, *args, **kwargs):
        super(KreditForm, self).__init__(*args, **kwargs)
        self.fields['office'].widget.attrs.update({'required': True, 'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'required': True, 'class': 'form-control'})
        self.fields['surname'].widget.attrs.update({'required': True, 'class': 'form-control'})
        self.fields['secondname'].widget.attrs.update({'required': True, 'class': 'form-control'})
        self.fields['sum'].widget.attrs.update({'required': True, 'class': 'form-control'})
        self.fields['doc_complect'].widget.attrs.update({'onChange': 'ShowKredits(this)', 'class': 'form-control'})
        self.fields['kred_link'].widget.attrs.update({'id': 'kredit_query', 'name': 'q', 'class': 'form-control'})
        self.fields['kred_mode'].widget.attrs.update({'class': 'form-control'})
        self.fields['kred_comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['sess'].required = True


class KreditControlForm(forms.Form):
    comment = forms.CharField(widget=CKEditorWidget())
    sess = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(KreditControlForm, self).__init__(*args, **kwargs)
        self.fields['sess'].required = True

    class Media:
        css = {'all': (
            'css/dropzone.css',
        )}
        js = (
            'js/dropzone.js',
        )