from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AdminPasswordChangeForm
from django_recaptcha.fields import ReCaptchaField
from .models import Component


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ('picture', 'name', 'component_id', 'is_active')
        labels = {
            'name': '',
            'component_id': '',
            'is_active': '',
            'picture': 'Pictures'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Component Name'}),
            'component_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Component ID'}),
            'is_active': forms.CheckboxInput(),
            'picture': forms.FileInput()
        }