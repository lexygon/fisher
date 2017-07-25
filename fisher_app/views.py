"""
Proje React.js ile API üzerinden alışveriş yaptığından dolayı FileServeView hariç hepsi gereksiz;
ancak daha sonra lazım olursa diye eklendiler
"""
from django.contrib.gis.geoip2 import GeoIP2
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import MailList, SenderMail, TargetMail, MailTemplate, CatchedData, Country, City
from .forms import MailListForm, SenderMailForm, TargetMailForm, MailTemplateForm, CatchedDataForm, CountryForm, CityForm
from django_user_agents.utils import get_user_agent


class FileServeView(View):
    def get(self, request, *args, **kwargs):
        if 'uuid' in self.kwargs:
            uuid = self.kwargs['kwargs']
            try:
                mail = TargetMail.objects.get(uuid__exact=uuid)
                mail.is_read = True
                mail.save()

                _user_agent = get_user_agent(request)
                location_data, ip = self.get_location(request)

                country = Country.objects.get_or_create(code__exact=location_data['country_data'],
                                                        name__exact=location_data['country_name'])

                city = City.objects.get_or_create(name__exact=location_data['city_name'],
                                                  region__exact=location_data['region'])

                catched_data = CatchedData()
                catched_data.victim = mail
                catched_data.ip = ip
                catched_data.location.latitude = location_data['latitude']
                catched_data.location.longitude = location_data['longtitude']
                catched_data.country = country
                catched_data.city = city
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
        if ip:
            return g.city(ip), ip
        else:
            return None, None


class MailListListView(ListView):
    model = MailList


class MailListCreateView(CreateView):
    model = MailList
    form_class = MailListForm


class MailListDetailView(DetailView):
    model = MailList


class MailListUpdateView(UpdateView):
    model = MailList
    form_class = MailListForm


class SenderMailListView(ListView):
    model = SenderMail


class SenderMailCreateView(CreateView):
    model = SenderMail
    form_class = SenderMailForm


class SenderMailDetailView(DetailView):
    model = SenderMail


class SenderMailUpdateView(UpdateView):
    model = SenderMail
    form_class = SenderMailForm


class TargetMailListView(ListView):
    model = TargetMail


class TargetMailCreateView(CreateView):
    model = TargetMail
    form_class = TargetMailForm


class TargetMailDetailView(DetailView):
    model = TargetMail


class TargetMailUpdateView(UpdateView):
    model = TargetMail
    form_class = TargetMailForm


class MailTemplateListView(ListView):
    model = MailTemplate


class MailTemplateCreateView(CreateView):
    model = MailTemplate
    form_class = MailTemplateForm


class MailTemplateDetailView(DetailView):
    model = MailTemplate


class MailTemplateUpdateView(UpdateView):
    model = MailTemplate
    form_class = MailTemplateForm


class CatchedDataListView(ListView):
    model = CatchedData


class CatchedDataCreateView(CreateView):
    model = CatchedData
    form_class = CatchedDataForm


class CatchedDataDetailView(DetailView):
    model = CatchedData


class CatchedDataUpdateView(UpdateView):
    model = CatchedData
    form_class = CatchedDataForm


class CountryListView(ListView):
    model = Country


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm


class CountryDetailView(DetailView):
    model = Country


class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm


class CityListView(ListView):
    model = City


class CityCreateView(CreateView):
    model = City
    form_class = CityForm


class CityDetailView(DetailView):
    model = City


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
