# coding: utf-8


from django.conf.urls import *
from .views import ArticleList, ArticleView


urlpatterns = patterns('article.views',
                       url(r'(.*)/$', ArticleList.as_view(), name='article_inside'),
                       url(r'$', ArticleView.as_view(), name='article_list'),
)
