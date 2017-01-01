# coding: utf-8


from django.conf.urls import patterns, url
from articles.views import ArticlesListView, ArticlesInsideView


urlpatterns = patterns(
    'articles.views',

    url(r'category/(?P<category_slug_title>.*)/$', ArticlesListView.as_view(),
        name='articles_list'),
    url(r'articles/(?P<chunk_slug_title>.*)/$', ArticlesInsideView.as_view(),
        name='articles_inside'),
)
