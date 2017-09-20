from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import ModelForm, Select, FileInput, TextInput, PasswordInput, CharField

from .models import MailList, SenderMail, MailTemplate, TargetMail, CatchedData


class BaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, FileInput):
                field.widget.attrs['class'] = 'form-control'

            if isinstance(field.widget, Select):
                field.widget.attrs['class'] = 'form-control select-dropdown'


class MailListForm(BaseModelForm):
    class Meta:
        model = MailList
        fields = (
            'name',
            'csv',
            'senders',
            'template',
            'targets',
        )


class SenderMailForm(BaseModelForm):
    class Meta:
        model = SenderMail
        fields = (
            'name',
            'host',
            'port',
            'email',
            'password',
            'use_ssl',
            'use_tls'
        )


class MailTemplateForm(BaseModelForm):
    class Meta:
        model = MailTemplate
        fields = (
            'title',
            'name',
            'file',
            'attachment'
        )


class TargetMailForm(BaseModelForm):
    class Meta:
        model = TargetMail
        fields = (
            'name',
            'email',
            'mail_list',
        )


class SiteLoginForm(AuthenticationForm):
    username = UsernameField(
        label='Kullanıcı Adı',
        max_length=254,
        help_text='Kullanıcı Adı',
        widget=TextInput(attrs={'autofocus': '',
                                'class': 'form-control',
                                'placeholder': 'Kullanıcı Adı'}),
    )

    password = CharField(
        label="Şifre",
        strip=False,
        help_text='Şifre',
        widget=PasswordInput(attrs={'class': 'form-control',
                                    'placeholder': 'Şifre'}),
    )


class CatchedDataForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, FileInput):
                field.widget.attrs['disabled'] = True

    class Meta:
        model = CatchedData
        fields = (
            'victim',
            'ip',
            'user_agent',
            'location',
            'country',
            'city',
        )
