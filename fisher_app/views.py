import csv

from django.contrib.auth import logout
from django.contrib.gis.geoip2 import GeoIP2
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, DetailView, RedirectView

from fisher import settings
from fisher_app.forms import MailListForm, SenderMailForm, MailTemplateForm, TargetMailForm, CatchedDataForm
from .models import TargetMail, CatchedData, Country, City, MailList, SenderMail, MailTemplate
from django_user_agents.utils import get_user_agent


# Logout and redirect to login
class LogoutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


# File Serve for tracking
class FileServeView(View):
    def get(self, request, *args, **kwargs):
        if 'uuid' in self.kwargs:
            uuid = self.kwargs['uuid']
            try:
                mail = TargetMail.objects.get(uuid__exact=uuid)
                mail.is_read = True
                mail.save()

                catched_data = CatchedData()

                _user_agent = get_user_agent(request)

                location_data, ip = self.get_location(request)

                if location_data:
                    catched_data.country = Country.objects.get_or_create(code__exact=location_data['country_code'],
                                                                         name__exact=location_data['country_name'])

                    catched_data.city = City.objects.get_or_create(name__exact=location_data['city_name'],
                                                                   region__exact=location_data['region'])

                    catched_data.location.latitude = location_data['latitude']
                    catched_data.location.longitude = location_data['longtitude']

                catched_data.victim = mail
                catched_data.ip = ip

                catched_data.user_agent = "{0} {1}".format(_user_agent.browser.family,
                                                           _user_agent.browser.version_string)
                catched_data.save()

                return redirect('/media/image.png')

            except TargetMail.DoesNotExist:
                raise Http404('File Not Found')
        else:
            raise Http404('Missing Url')

    def get_location(self, request):
        """
            beklenen return:
            {'city': 'Mountain View',
               'country_code': 'US',
               'country_name': 'United States',
               'dma_code': 807,
               'latitude': 37.419200897216797,
               'longitude': -122.05740356445312,
               'postal_code': '94043',
               'region': 'CA'}
        """
        g = GeoIP2()
        ip = self.request.META.get('REMOTE_ADDR', None)
        if ip and ip != '127.0.0.1':
            return g.city(ip), ip
        else:
            return None, None


# SenderMail Views
class SenderMailListView(ListView):
    model = SenderMail
    paginate_by = 20
    template_name = 'SenderMail/list.html'


class SenderMailCreateView(CreateView):
    model = SenderMail
    form_class = SenderMailForm
    template_name = 'SenderMail/create.html'


class SenderMailUpdateView(UpdateView):
    model = SenderMail
    form_class = SenderMailForm
    template_name = 'SenderMail/update.html'


class SenderMailDeleteView(DeleteView):
    model = SenderMail
    success_url = reverse_lazy('sendermail_list')


# TargetMail Views
class TargetMailListView(ListView):
    model = TargetMail
    paginate_by = 20
    template_name = 'TargetMail/list.html'


class TargetMailCreateView(CreateView):
    model = TargetMail
    form_class = TargetMailForm
    template_name = 'TargetMail/create.html'


class TargetMailUpdateView(UpdateView):
    model = TargetMail
    form_class = TargetMailForm
    template_name = 'TargetMail/update.html'


class TargetMailDeleteView(DeleteView):
    model = TargetMail
    success_url = reverse_lazy('targetmail_list')


# MailTemplate Views
class MailTemplateListView(ListView):
    model = MailTemplate
    paginate_by = 20
    template_name = 'MailTemplate/list.html'


class MailTemplateCreateView(CreateView):
    model = MailTemplate
    form_class = MailTemplateForm
    template_name = 'MailTemplate/create.html'


class MailTemplateUpdateView(UpdateView):
    model = MailTemplate
    form_class = MailTemplateForm
    template_name = 'MailTemplate/update.html'


class MailTemplateDeleteView(DeleteView):
    model = SenderMail
    success_url = reverse_lazy('mailtemplate_list')


# CatchedData Views
class CatchedDataListView(ListView):
    model = CatchedData
    paginate_by = 20
    template_name = 'CatchedData/list.html'


class CatchedDataDetailView(UpdateView):
    model = CatchedData
    template_name = 'CatchedData/detail.html'
    form_class = CatchedDataForm


class CatchedDataDeleteView(DeleteView):
    model = CatchedData
    success_url = reverse_lazy('catcheddata_list')


# MailList Views
class MailListListView(ListView):
    model = MailList
    template_name = 'MailList/list.html'


class MailListCreateView(CreateView):
    model = MailList
    form_class = MailListForm
    template_name = 'MailList/create.html'

    def form_valid(self, form):
        mail_list_object = form.save()  # gelen veri, dbye kaydedildi

        if mail_list_object.csv:
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
                    # CSV dosyasında email isimli bir field yoksa kaydedilen veriyi silip exception atıyor.
                    if not data['email']:
                        mail_list_object.delete()
                        raise AssertionError("Yüklenen CSV dosyası 'email' isimli bir field içermemektedir.")
                    else:
                        target_mail = TargetMail(**data)
                        target_mail.save()

        return super(MailListCreateView, self).form_valid(form)


class MailListUpdateView(UpdateView):
    model = MailList
    form_class = MailListForm
    template_name = 'MailList/update.html'


class MailListDeleteView(DeleteView):
    model = SenderMail
    success_url = reverse_lazy('maillist_list')


# Index
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        maillists = MailList.objects.all()

        context['maillists'] = maillists

        return context
