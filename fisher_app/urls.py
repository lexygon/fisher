from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from fisher_app import api
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from fisher import settings
from fisher_app.api import AuthTokenViewSet, StartMailListView, StatisticsAPIView
from fisher_app.forms import SiteLoginForm
from fisher_app.views import FileServeView, IndexView, MailListCreateView, SenderMailListView, MailListListView, \
    SenderMailCreateView, SenderMailUpdateView, MailListUpdateView, SenderMailDeleteView, MailListDeleteView, \
    MailTemplateCreateView, MailTemplateUpdateView, MailTemplateListView, MailTemplateDeleteView, CatchedDataListView, \
    CatchedDataDetailView, CatchedDataDeleteView, LogoutView, TargetMailCreateView, TargetMailUpdateView, \
    TargetMailListView, TargetMailDeleteView

router = routers.DefaultRouter()
router.register(r'maillist', api.MailListViewSet)
router.register(r'sendermail', api.SenderMailViewSet)
router.register(r'targetmail', api.TargetMailViewSet)
router.register(r'mailtemplate', api.MailTemplateViewSet)
router.register(r'catcheddata', api.CatchedDataViewSet)
router.register(r'country', api.CountryViewSet)
router.register(r'city', api.CityViewSet)

urlpatterns = [
                  # urls for Django Rest Framework API
                  url(r'^api/v1/', include(router.urls)),
                  url(r'^api/v1/auth-token/$', AuthTokenViewSet.as_view()),
                  # url(r'^api/v1/send-mail/$', SendMailView.as_view()),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  url(r'^file/(?P<uuid>[0-9A-Fa-f-]+)', FileServeView.as_view(), name='file_view'),
                  url(r'^api/v1/statistics/(?P<slug>\S+)/$', StatisticsAPIView.as_view()),
                  # url(r'^.*/', TemplateView.as_view(template_name="base.html"), name='base')

                  url(r'^$', IndexView.as_view(), name='index'),

                  # MailTemplate
                  url(r'^mailtemplate-create', login_required(MailTemplateCreateView.as_view()),
                      name='mailtemplate_create'),
                  url(r'^mailtemplate-update/(?P<slug>\S+)/$', login_required(MailTemplateUpdateView.as_view()),
                      name='mailtemplate_update'),
                  url(r'^mailtemplate-list$', login_required(MailTemplateListView.as_view()), name='mailtemplate_list'),
                  url(r'^mailtemplate-delete/(?P<slug>\S+)/$', login_required(MailTemplateDeleteView.as_view()),
                      name='mailtemplate_delete'),

                  # SenderMail
                  url(r'^sendermail-create', login_required(SenderMailCreateView.as_view()), name='sendermail_create'),
                  url(r'^sendermail-update/(?P<slug>\S+)/$', login_required(SenderMailUpdateView.as_view()),
                      name='sendermail_update'),
                  url(r'^sendermail-list$', login_required(SenderMailListView.as_view()), name='sendermail_list'),
                  url(r'^sendermail-delete/(?P<slug>\S+)/$', login_required(SenderMailDeleteView.as_view()),
                      name='sendermail_delete'),

                  # TargetMail
                  url(r'^targetmail-create', login_required(TargetMailCreateView.as_view()), name='targetmail_create'),
                  url(r'^targetmail-update/(?P<slug>\S+)/$', login_required(TargetMailUpdateView.as_view()),
                      name='targetmail_update'),
                  url(r'^targetmail-list$', login_required(TargetMailListView.as_view()), name='targetmail_list'),
                  url(r'^targetmail-delete/(?P<slug>\S+)/$', login_required(TargetMailDeleteView.as_view()),
                      name='targetmail_delete'),

                  # CatchedData
                  url(r'^catcheddata-list$', login_required(CatchedDataListView.as_view()), name='catcheddata_list'),
                  url(r'^catcheddata-detail/(?P<pk>\d+)/$', login_required(CatchedDataDetailView.as_view()),
                      name='catcheddata_detail'),
                  url(r'^catcheddata-delete/(?P<pk>\d+)/$', login_required(CatchedDataDeleteView.as_view()),
                      name='catcheddata_delete'),

                  # MailList
                  url(r'^maillist-create$', login_required(MailListCreateView.as_view()), name='maillist_create'),
                  url(r'^maillist-update/(?P<slug>\S+)/$', login_required(MailListUpdateView.as_view()),
                      name='maillist_update'),
                  url(r'^maillist-list', login_required(MailListListView.as_view()), name='maillist_list'),
                  url(r'^maillist-delete', login_required(MailListDeleteView.as_view()), name='maillist_delete'),
                  url(r'^maillist-start/(?P<slug>\S+)/$', login_required(StartMailListView.as_view()),
                      name='maillist_start'),

                  # Login/Logout
                  url(r'^login/$', auth_views.login, {'template_name': 'login.html',
                                                      'authentication_form': SiteLoginForm,
                                                      'redirect_authenticated_user': True}, name='login'),
                  url(r'^logout/$', LogoutView.as_view(), name='logout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
