from django.contrib.auth.models import update_last_login
from django.core.mail import get_connection, EmailMessage, EmailMultiAlternatives
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from fisher import settings
from fisher_app import models, permissions as perm
from fisher_app import serializers
from rest_framework import viewsets, permissions

from fisher_app.models import AuthToken, MailList, TargetMail
from fisher_app.permissions import AjaxOnly, DomainOnly, AuthenticatedUserOnly
from fisher_app.serializers import UserSerializer, StatisticsSerializer
import csv


class MailListViewSet(viewsets.ModelViewSet):
    """ViewSet for the MailList class"""

    queryset = models.MailList.objects.all()
    serializer_class = serializers.MailListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        mail_list_object = serializer.save()  # gelen veri, dbye kaydedildi

        with open('{0}/{1}'.format(settings.MEDIA_ROOT, str(mail_list_object.csv))) as csvfile:
            # kaydedilen verideki csv dosyasını okuyor
            reader = csv.DictReader(csvfile)
            # okunan verinin içindeki name-email fieldlarını collect edip TargetMail tablosuna kaydediyor.
            for row in reader:
                data = {
                    'name': row['name'] if 'name' in row else None,
                    'email': row['email'] if 'email' in row else None,
                    'mail_list': mail_list_object
                }
                if not data['email']:
                    return
                else:
                    target_mail = TargetMail(**data)
                    target_mail.save()


class SenderMailViewSet(viewsets.ModelViewSet):
    """ViewSet for the SenderMail class"""
    queryset = models.SenderMail.objects.all()
    serializer_class = serializers.SenderMailSerializer
    permission_classes = [perm.AuthenticatedUserOnly]


class TargetMailViewSet(viewsets.ModelViewSet):
    """ViewSet for the TargetMail class"""

    queryset = models.TargetMail.objects.all()
    serializer_class = serializers.TargetMailSerializer
    permission_classes = [permissions.IsAuthenticated]


class MailTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for the MailTemplate class"""

    queryset = models.MailTemplate.objects.all()
    serializer_class = serializers.MailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CatchedDataViewSet(viewsets.ModelViewSet):
    """ViewSet for the CatchedData class"""

    queryset = models.CatchedData.objects.all()
    serializer_class = serializers.CatchedDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Country class"""

    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for the City class"""

    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthTokenViewSet(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        update_last_login(None, user)

        token, created = AuthToken.objects.get_or_create(user=user)
        token.client_address = self.get_ip_address(request)
        token.save()

        return Response({'token': token.key, 'user': UserSerializer(user).data})

    def get_ip_address(self, request):
        try:
            client_address = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError as e:
            try:
                client_address = request.META['REMOTE_ADDR']
            except KeyError as e:
                client_address = None
        return client_address


class StatisticsAPIView(RetrieveAPIView):
    queryset = MailList.objects.all()
    serializer_class = StatisticsSerializer
    lookup_field = 'slug'


class StartMailListView(RetrieveDestroyAPIView):
    queryset = MailList.objects.all()

    permission_classes = (AjaxOnly, DomainOnly, AuthenticatedUserOnly)

    def get_object(self):
        slug = self.kwargs.get('slug', None)
        if slug:
            return MailList.objects.get(slug__exact=slug)
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        mail_list_object = self.get_object()

        if mail_list_object.is_started:
            return Response({'status': 'working'})
        else:

            mails_to_send = {}
            senders = mail_list_object.senders.all()
            target_list = mail_list_object.targetmail_set.all()
            targets_count = target_list.count()
            senders_count = senders.count()

            for sender in senders:
                mails_to_send[sender.email] = []

            lower_bound = 0
            step = int(targets_count / senders_count)
            upper_bound = step

            for key, targets in mails_to_send.items():
                targets.extend(target_list[lower_bound:upper_bound])
                lower_bound = upper_bound
                if upper_bound + step > targets_count:
                    upper_bound = targets_count - upper_bound
                else:
                    upper_bound += step

            for key, targets in mails_to_send.items():
                # sender_mail = senders.get(email__exact=key).username
                sender_mail = senders.get(email__exact=key)
                for target in targets:
                    print('targ', target)
                    with get_connection(
                            host=sender_mail.host,
                            port=sender_mail.port,
                            username=sender_mail.email,
                            password=sender_mail.password,
                            use_tls=sender_mail.use_tls,
                            use_ssl=sender_mail.use_ssl
                    ) as connection:
                        # mail şablonunun içindeki {{ image_url }} kısmına urli gönderip stringe render ediyor
                        # image_url = "http://{0}/file/{1}".format(settings.DOMAIN, target.uuid)
                        image_url = request.build_absolute.uri(reverse('file_view', args=(target.uuid, )))
                        str_template = render_to_string(template_name='{0}/{1}'.format(settings.MEDIA_ROOT,
                                                                                       str(
                                                                                           mail_list_object.template.file)),
                                                        context={'image': image_url})
                        # email objesi yaratılıyor
                        msg = EmailMultiAlternatives(subject=mail_list_object.template.title,
                                                     body=str_template,

                                                     from_email=sender_mail.email,
                                                     to=[target.email],
                                                     connection=connection)
                        # attachment
                        msg.attach_file(
                            '{0}/{1}'.format(settings.MEDIA_ROOT, str(mail_list_object.template.attachment)))
                        msg.attach_alternative(str_template, "text/html")
                        # sonraki iki satır django-mailer üzerinde yaptığım değişikliklerden sonra, henüz gideremediğim
                        # bir bugı gidermek için eklendi. bugı yakında düzelteceğim.
                        # https://github.com/lexygon/django-mailer adresinden geliştirmeye devam edeceğim
                        # django-mailer'ın farklı smtp ayarlarından da mail atabilen versiyonunu takip edebilirsiniz.

                        msg.username = sender_mail.email
                        msg.password = sender_mail.password
                        msg.host = sender_mail.host
                        msg.port = sender_mail.port
                        msg.use_tls = sender_mail.use_tls
                        msg.use_ssl = sender_mail.use_ssl
                        msg.send()

            return Response(data={'status': 'sent', }, status=200)
