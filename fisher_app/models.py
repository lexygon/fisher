from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db import fields as extension_fields
from geoposition.fields import GeopositionField
from rest_framework.authtoken.models import Token
import uuid as _uuid


class AuthToken(Token):
    client_address = CharField(max_length=255, verbose_name='Client IP Adresi', blank=True)


class MailList(models.Model):
    # Fields
    name = models.CharField(max_length=255, verbose_name='İsim')
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    csv = models.FileField(upload_to="files/csv/", verbose_name='Hedef Mailler Listesi -CSV-')

    # Relationship Fields
    senders = models.ManyToManyField('fisher_app.SenderMail', verbose_name='Gönderecek Mailler')
    templates = models.ManyToManyField('fisher_app.MailTemplate', verbose_name='Şablonlar')
    targets = models.ManyToManyField('fisher_app.TargetMail', verbose_name='Hedef Mailler', blank=True)
    owner = ForeignKey(User, blank=True, null=True, verbose_name='Ekleyen')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Mail Listesi'
        verbose_name_plural = 'Mail Listeleri'

    def __str__(self):
        return self.name


class SenderMail(models.Model):
    # Fields
    name = models.CharField(max_length=255, verbose_name='İsim')
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=255, verbose_name='Şifre')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Gönderici Mail'
        verbose_name_plural = 'Gönderici Mailler'

    def __str__(self):
        return self.name or self.email


class TargetMail(models.Model):
    # Fields
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='İsim')
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    email = models.EmailField()
    uuid = models.UUIDField(default=_uuid.uuid4, unique=True, blank=True)
    is_read = models.BooleanField(default=False, verbose_name='Okundu')

    # Relationship Fields
    mail_list = models.ForeignKey('fisher_app.MailList', )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Hedef Mail'
        verbose_name_plural = 'Hedef Mailler'

    def get_name(self):
        return self.name or self.email or self.uuid

    def __str__(self):
        return self.get_name()


class MailTemplate(models.Model):
    # Fields
    title = models.CharField(max_length=255, verbose_name='Mail Başlığı')
    name = models.CharField(max_length=255, verbose_name='Şablon Adı')
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    file = models.FileField(upload_to="files/templates/", verbose_name='Mail Şablonu')
    attachment = models.FileField(upload_to="files/attachments/", verbose_name='Attachment')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Mail Şablonu'
        verbose_name_plural = 'Mail Şablonları'

    def __str__(self):
        return self.name or self.title


class CatchedData(models.Model):
    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    ip = models.GenericIPAddressField()

    user_agent = models.CharField(max_length=500)
    location = GeopositionField(blank=True, verbose_name='Lokasyon', null=True)

    # Relationship Fields
    city = models.ForeignKey('fisher_app.City', )
    country = models.ForeignKey('fisher_app.Country', )
    victim = models.ForeignKey('fisher_app.TargetMail', )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Yakalanan Veri'
        verbose_name_plural = 'Yakalanan Veriler'

    def __str__(self):
        return self.victim.name or self.victim.email


class Country(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    code = models.CharField(max_length=30)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Ülke'
        verbose_name_plural = 'Ülkeler'

    def __str__(self):
        return self.name


class City(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    region = models.CharField(max_length=30)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Şehir'
        verbose_name_plural = 'Şehirler'

    def __str__(self):
        return self.name
