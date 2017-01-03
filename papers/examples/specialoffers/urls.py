# coding: utf-8


from django.conf.urls import patterns, url
from specialoffers.views import SpecialoffersCategoryListView, SpecialoffersListView, SpecialoffersInsideView


urlpatterns = patterns(
    'specialoffers.views',

    url(r'^$', SpecialoffersCategoryListView.as_view(), name='category_list'),
    url(r'category/(?P<category_slug_title>.*)/$', SpecialoffersListView.as_view(),
        name='specialoffers_list'),
    url(r'specialoffers/(?P<chunk_slug_title>.*)/$', SpecialoffersInsideView.as_view(),
        name='specialoffers_inside'),
)
