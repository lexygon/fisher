"""
views.py dosyasındaki açıklamaya binaen burası da gereksiz ve yazıldı.
"""
from django import forms
from .models import MailList, SenderMail, TargetMail, MailTemplate, CatchedData, Country, City


class MailListForm(forms.ModelForm):
    class Meta:
        model = MailList
        fields = ['name', 'csv', 'senders', 'templates', 'targets']


class SenderMailForm(forms.ModelForm):
    class Meta:
        model = SenderMail
        fields = ['email', 'password']


class TargetMailForm(forms.ModelForm):
    class Meta:
        model = TargetMail
        fields = ['name', 'email', 'uuid', 'is_read', 'mail_list']


class MailTemplateForm(forms.ModelForm):
    class Meta:
        model = MailTemplate
        fields = ['name', 'file']


class CatchedDataForm(forms.ModelForm):
    class Meta:
        model = CatchedData
        fields = ['ip', 'headers', 'user_agent', 'location', 'city', 'country', 'victim']


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'code']


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'region']


