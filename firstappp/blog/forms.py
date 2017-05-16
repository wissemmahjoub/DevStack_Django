from django import forms
from . import models
class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(max_length=100)
    envoyeur = forms.EmailField(label="Votre adresse mail")

class ImageeForm(forms.Form):
    document = forms.FileField()
    #name = forms.CharField(max_length=100)



class ImggForm(forms.Form):
    name = forms.CharField(max_length=100)
    container = forms.CharField(max_length=100)
    disk = forms.CharField(max_length=100)
    visibility = forms.CharField(max_length=100)


class GetVolumeForm(forms.Form):
    name = forms.CharField(max_length=100).required=False
    description = forms.CharField(max_length=100).required=False
    size = forms.CharField(max_length=100).required=False


class VolumeForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    size = forms.CharField(max_length=100)


