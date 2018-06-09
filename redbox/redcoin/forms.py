from __future__ import unicode_literals

from django import forms

from .models import StoredFiles

# User Sign Up function 구현
from django.contrib.auth.models import User


class FileUpForm(forms.ModelForm):
    class Meta:
        model = StoredFiles
        fields = ('owner', 'content', 'thumnail', 'description', )

# User Sign Up function 구현
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'email', 'password']