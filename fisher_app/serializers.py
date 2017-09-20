from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, ExtractDay
from rest_framework.fields import SerializerMethodField

from fisher_app import models

from rest_framework import serializers

from fisher_app.models import CatchedData, TargetMail, MailList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', )


class MailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MailList
        fields = (
            'pk',
            'name', 
            'created', 
            'last_updated', 
            'csv', 
            'senders',
            'owner',
            'templates'
        )


class SenderMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SenderMail
        fields = (
            'pk',
            'name',
            'email', 
            'password', 
        )


class TargetMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TargetMail
        fields = (
            'pk',
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'email',
            'uuid'

        )


class MailTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MailTemplate
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'file', 
        )


class CatchedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CatchedData
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'ip', 
            'headers', 
            'user_agent', 
            'location', 
        )


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'code', 
        )


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'region', 
        )


class StatisticsSerializer(serializers.ModelSerializer):
    by_day = SerializerMethodField()
    by_user_agent = SerializerMethodField()
    by_city = SerializerMethodField()
    by_country = SerializerMethodField()
    by_location = SerializerMethodField()
    total_read = SerializerMethodField()
    total_unread = SerializerMethodField()
    total_victim = SerializerMethodField()
    total_senders = SerializerMethodField()

    def get_by_day(self, obj):
        return CatchedData.objects.filter(victim__in=obj.targetmail_set.all())\
            .annotate(date=ExtractDay('created')).values('date').annotate(count=Count('id')).values('date', 'count').order_by()

    def get_by_user_agent(self, obj):
        return CatchedData.objects.filter(victim__in=obj.targetmail_set.all())\
            .values('user_agent').annotate(count=Count('user_agent')).order_by()

    def get_by_city(self, obj):
        qs = CatchedData.objects.filter(victim__in=obj.targetmail_set.all())\
            .values('city__name').annotate(count=Count('city')).order_by()[:10]
        return qs

    def get_by_country(self, obj):
        return CatchedData.objects.filter(victim__in=obj.targetmail_set.all())\
            .values('country__name').annotate(count=Count('country')).order_by()[:10]

    def get_by_location(self, obj):
        x = CatchedData.objects.filter(victim__in=obj.targetmail_set.all())\
            .values('location', 'victim__email').annotate(count=Count('location')).order_by()

        for y in x:
            y['latitude'] = y['location'].latitude
            y['longitude'] = y['location'].longitude
            del y['location']
        return x

    def get_total_read(self, obj):
        return TargetMail.objects.filter(is_read=True, mail_list=obj).count()

    def get_total_unread(self, obj):
        return TargetMail.objects.filter(is_read=False, mail_list=obj).count()

    def get_total_victim(self, obj):
        return obj.targetmail_set.count() + obj.targets.count()

    def get_total_senders(self, obj):
        return obj.senders.count()

    class Meta:
        model = models.MailList
        fields = (
            'by_day',
            'by_user_agent',
            'by_city',
            'by_country',
            'by_location',
            'total_read',
            'total_unread',
            'total_victim',
            'total_senders',
        )
