# coding: utf-8


from django.conf.urls import patterns, url

from portfolio.views import CategoryListView, PortfolioListView, PortfolioInsideView


urlpatterns = patterns(
    'portfolio.views',

    url(r'^$', CategoryListView.as_view(), name='category_list'),
    url(r'category/(?P<catalog_slug_title>.*)/$', PortfolioListView.as_view(),
        name='portfolio_list'),
    # url(r'product/calc/$', ProductCalcView.as_view(), name='product_calc'),
    # url(r'product/cart/$', ProductCartView.as_view(), name='product_cart'),
    url(r'portfolio/(?P<portfolio_slug_title>.*)/$', PortfolioInsideView.as_view(),
        name='portfolio_inside'),
)
