from django.contrib.auth import get_user_model

from fisher_app import models

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', )


class MailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MailList
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'csv', 
        )


class SenderMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SenderMail
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'email', 
            'password', 
        )


class TargetMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TargetMail
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'email', 
            'uuid', 
            'is_read', 
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


