# coding: utf-8


from django.conf.urls import url, patterns
from .views import NewsDetail, NewsList


urlpatterns = patterns('news.views',
                       url(r'(.*)/$', NewsDetail.as_view(), name='news_inside'),
                       url(r'$', NewsList.as_view(), name='news_list'),
                       )
