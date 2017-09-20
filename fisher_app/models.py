from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_extensions.db import fields as extension_fields
from geoposition.fields import GeopositionField
from rest_framework.authtoken.models import Token
import uuid as _uuid
from django.apps import apps


class AuthToken(Token):
    client_address = CharField(max_length=255, verbose_name='Client IP Adresi', blank=True)


class MailList(models.Model):
    # Fields
    name = models.CharField(max_length=255, verbose_name='İsim')
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    csv = models.FileField(upload_to="files/csv/", verbose_name='Hedef Mailler Listesi -CSV-', blank=True)
    is_started = models.BooleanField(default=False)

    # Relationship Fields
    senders = models.ManyToManyField('fisher_app.SenderMail', verbose_name='Gönderici Mailler')
    template = models.ForeignKey('fisher_app.MailTemplate', verbose_name='Şablon')
    targets = models.ManyToManyField('fisher_app.TargetMail', verbose_name='Hedef Mailler', blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Mail Listesi'
        verbose_name_plural = 'Mail Listeleri'

    def get_queue_count(self):
        TargetMail = apps.get_model(app_label='fisher_app', model_name='TargetMail')
        return TargetMail.objects.filter(mail_list=self, is_read=False)

    def get_processed_queue_count(self):
        TargetMail = apps.get_model(app_label='fisher_app', model_name='TargetMail')
        return TargetMail.objects.filter(mail_list=self, is_read=True)

    def get_senders(self):
        count = self.senders.count()

        if count <= 3:
            return ", ".join([sender.email for sender in self.senders.all()])
        else:
            return "{} adet gönderici.".format(count)

    def get_target_count(self):
        TargetMail = apps.get_model(app_label='fisher_app', model_name='TargetMail')
        return TargetMail.objects.filter(mail_list=self).count()

    def get_absolute_url(self):
        return reverse('maillist_update', kwargs={'slug': self.slug})

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
    use_tls = models.BooleanField(default=False, blank=True, verbose_name='TLS Kullan')
    use_ssl = models.BooleanField(default=True, blank=True, verbose_name='SSL Kullan')
    host = models.CharField(max_length=255)
    port = models.IntegerField(blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Gönderici Mail'
        verbose_name_plural = 'Gönderici Mailler'

    def get_absolute_url(self):
        return reverse('sendermail_update', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name or self.email


class TargetMail(models.Model):
    # Fields
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='İsim')
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    email = models.EmailField(blank=True)
    uuid = models.UUIDField(default=_uuid.uuid4, unique=True, blank=True, null=True)
    is_read = models.BooleanField(default=False, verbose_name='Okundu', blank=True)

    # Relationship Fields
    mail_list = models.ForeignKey('fisher_app.MailList', blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Hedef Mail'
        verbose_name_plural = 'Hedef Mailler'

    def get_absolute_url(self):
        return reverse('targetmail_update', kwargs={'slug': self.slug})

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
    file = models.FileField(upload_to="files/templates/", verbose_name='Şablon Dosyası')
    attachment = models.FileField(upload_to="files/attachments/", verbose_name='Attachment')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Mail Şablonu'
        verbose_name_plural = 'Mail Şablonları'

    def __str__(self):
        return self.name or self.title

    def get_absolute_url(self):
        return reverse('mailtemplate_update', kwargs={'slug': self.slug})


class CatchedData(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yakalanma Tarihi', editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    ip = models.GenericIPAddressField(blank=True, null=True)

    user_agent = models.CharField(max_length=500, blank=True, null=True, verbose_name='Browser')
    location = GeopositionField(blank=True, verbose_name='Lokasyon', null=True)

    # Relationship Fields
    city = models.ForeignKey('fisher_app.City', blank=True, null=True, verbose_name='Şehir')
    country = models.ForeignKey('fisher_app.Country', blank=True, null=True, verbose_name='Ülke')
    victim = models.ForeignKey('fisher_app.TargetMail', verbose_name='Hedef')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Yakalanan Veri'
        verbose_name_plural = 'Yakalanan Veriler'

    def __str__(self):
        return "{} - {}".format(self.victim.email, self.victim.name)

    def get_city_n_country(self):
        if self.city and self.country:
            return "{} / {}".format(self.city.name, self.country.name)
        elif self.city and not self.country:
            return self.city.name
        elif self.country and not self.city:
            return self.country.name
        else:
            return '-'

    def get_ip(self):
        return self.ip or '-'

    def get_absolute_url(self):
        return reverse('catcheddata_detail', kwargs={'pk': self.pk})


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
