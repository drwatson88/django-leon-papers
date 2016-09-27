# coding: utf-8


from django.conf.urls import url, patterns
from .views import ContactView


urlpatterns = patterns('main.views',
                       url(r'$', ContactView.as_view(), name='main'),
)
