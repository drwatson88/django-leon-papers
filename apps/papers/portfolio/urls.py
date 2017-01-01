# coding: utf-8


from django.conf.urls import patterns, url
from portfolio.views import PortfolioCategoryListView, PortfolioListView, PortfolioInsideView


urlpatterns = patterns(
    'portfolio.views',

    url(r'^$', PortfolioCategoryListView.as_view(), name='category_list'),
    url(r'category/(?P<category_slug_title>.*)/$', PortfolioListView.as_view(),
        name='portfolio_list'),
    url(r'portfolio/(?P<chunk_slug_title>.*)/$', PortfolioInsideView.as_view(),
        name='portfolio_inside'),
)
