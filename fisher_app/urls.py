from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers
from fisher_app import api
from django.conf.urls.static import static

from fisher import settings
from fisher_app.api import AuthTokenViewSet, SendMailView
from fisher_app.views import FileServeView

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
    url(r'^api/v1/send-mail/$', SendMailView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^file/(?P<uuid>[0-9A-Fa-f-]+)', FileServeView.as_view()),
    url(r'^.*/', TemplateView.as_view(template_name="base.html"), name='base')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
