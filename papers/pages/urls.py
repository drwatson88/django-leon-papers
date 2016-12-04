# coding: utf-8


from django.conf.urls import url, patterns
from .views import MainPageView


urlpatterns = patterns('pages.views',
                       url(r'$', MainPageView.as_view(), name='main_page'),
)
