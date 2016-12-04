# coding: utf-8


from django import forms


class FormContact(forms.Form):

    name = forms.CharField()
    message = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
