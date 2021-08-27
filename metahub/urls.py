# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .core import views as core_views

urlpatterns = i18n_patterns(
    prefix_default_language=False,
)

if settings.DEBUG:
    # serve /favicon.ico accessed directly (in production this is handled by nginx)
    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('images/favicons/favicon.ico')))
    ]

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', core_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', core_views.permission_denied, kwargs={'exception': Exception('Permission Denied!')}),
        url(r'^404/$', core_views.page_not_found, kwargs={'exception': Exception('Page Not Found!')}),
        url(r'^500/$', core_views.server_error),
    ]

    # render by name for frontend (static) templates.
    urlpatterns += [url(r'^frontend/$', core_views.FrontendTemplateView.as_view()), ]
    urlpatterns += [url(r'^frontend/(?P<template>.*).html$', core_views.FrontendTemplateView.as_view()), ]


urlpatterns += [
    url(r'^django-admin/', admin.site.urls),
    # url(r'^api/', include('metahub.api.urls')),
    url(r'^collection/', include('metahub.collection.urls')),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(wagtail_urls)),
]


# this only does something when DEBUG is True
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = core_views.bad_request
handler403 = core_views.permission_denied
handler404 = core_views.page_not_found
handler500 = core_views.server_error


