from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'KeyExchange.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'exchange.views.front_page' ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'exchange/', include('exchange.urls')), )
