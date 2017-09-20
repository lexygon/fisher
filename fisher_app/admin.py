from django.contrib import admin
from django import forms
from .models import MailList, SenderMail, TargetMail, MailTemplate, CatchedData, Country, City


class MailListAdminForm(forms.ModelForm):
    class Meta:
        model = MailList
        fields = '__all__'


class MailListAdmin(admin.ModelAdmin):
    form = MailListAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'csv']
    readonly_fields = ['slug', 'created', 'last_updated']


admin.site.register(MailList, MailListAdmin)


class SenderMailAdminForm(forms.ModelForm):
    class Meta:
        model = SenderMail
        fields = '__all__'


class SenderMailAdmin(admin.ModelAdmin):
    form = SenderMailAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']


admin.site.register(SenderMail, SenderMailAdmin)


class TargetMailAdminForm(forms.ModelForm):
    class Meta:
        model = TargetMail
        fields = '__all__'


class TargetMailAdmin(admin.ModelAdmin):
    form = TargetMailAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'email', 'uuid', 'is_read']
    readonly_fields = ['slug', 'last_updated']


admin.site.register(TargetMail, TargetMailAdmin)


class MailTemplateAdminForm(forms.ModelForm):
    class Meta:
        model = MailTemplate
        fields = '__all__'


class MailTemplateAdmin(admin.ModelAdmin):
    form = MailTemplateAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'file']
    readonly_fields = ['slug', 'created', 'last_updated']


admin.site.register(MailTemplate, MailTemplateAdmin)


class CatchedDataAdminForm(forms.ModelForm):
    class Meta:
        model = CatchedData
        fields = '__all__'


class CatchedDataAdmin(admin.ModelAdmin):
    form = CatchedDataAdminForm
    list_display = ['created', 'last_updated', 'ip', 'user_agent', 'location']
    readonly_fields = ['created', 'last_updated']


admin.site.register(CatchedData, CatchedDataAdmin)


class CountryAdminForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class CountryAdmin(admin.ModelAdmin):
    form = CountryAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'code']
    readonly_fields = ['slug', 'created', 'last_updated']


admin.site.register(Country, CountryAdmin)


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'


class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'region']
    readonly_fields = ['slug', 'created', 'last_updated']


admin.site.register(City, CityAdmin)
