from __future__ import unicode_literals

from django import forms

from .models import StoredFiles


class FileUpForm(forms.ModelForm):
    class Meta:
        model = StoredFiles
        fields = ('owner', 'content', 'thumnail', 'description', )