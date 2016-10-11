# coding: utf-8


from django.conf.urls import patterns, url
from news.views import NewsCategoryListView, NewsListView, NewsInsideView


urlpatterns = patterns(
    'news.views',

    url(r'^$', NewsCategoryListView.as_view(), name='category_list'),
    url(r'category/(?P<category_slug_title>.*)/$', NewsListView.as_view(),
        name='news_list'),
    url(r'news/(?P<chunk_slug_title>.*)/$', NewsInsideView.as_view(),
        name='news_inside'),
)
