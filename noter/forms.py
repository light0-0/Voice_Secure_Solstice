from django.forms import ModelForm
from .models import  *
from django import forms

class note_form(ModelForm):
    note_name = forms.CharField(max_length=50)
    note = forms.CharField(max_length=100)

    class Meta:
        model = note
        fields = '__all__'