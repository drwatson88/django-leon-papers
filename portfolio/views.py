# -*- coding: utf-8 -*-


from sample.views import CategoryListView, ChunkListView, ChunkInsideView
from .base import PortfolioBaseView, PortfolioParamsValidatorMixin
from .models import PortfolioCategory, Portfolio


class PortfolioCategoryListView(CategoryListView, PortfolioParamsValidatorMixin):

    """ Category List View.
    """

    CATEGORY_MODEL = PortfolioCategory

    def _set_labels(self):
        self.labels = {}
        self.labels.update({
            'app_label': 'Портфолио',
            'general_label': 'Главная',
        })

    def _set_dispatcher(self):
        self.dispatcher = {}
        self.dispatcher.update({
            'general': 'pages:main_page',
            'category_list': 'portfolio:category_list',
            'chunk_list': 'portfolio:portfolio_list',
            'chunk_inside': 'portfolio:portfolio_inside',
        })


class PortfolioListView(ChunkListView, PortfolioParamsValidatorMixin):

    """ Portfolio List View.
    """

    CATEGORY_MODEL = PortfolioCategory
    CHUNK_MODEL = Portfolio

    def _set_labels(self):
        self.labels = {}
        self.labels.update({
            'app_label': 'Портфолио',
            'general_label': 'Главная',
        })

    def _set_dispatcher(self):
        self.dispatcher = {}
        self.dispatcher.update({
            'general': 'pages:main_page',
            'category_list': 'portfolio:category_list',
            'chunk_list': 'portfolio:portfolio_list',
            'chunk_inside': 'portfolio:portfolio_inside',
        })


class PortfolioInsideView(ChunkInsideView, PortfolioParamsValidatorMixin):

    """ Portfolio Inside View.
    """

    CATEGORY_MODEL = PortfolioCategory
    CHUNK_MODEL = Portfolio

    def _set_labels(self):
        self.labels = {}
        self.labels.update({
            'app_label': 'Портфолио',
            'general_label': 'Главная',
        })

    def _set_dispatcher(self):
        self.dispatcher = {}
        self.dispatcher.update({
            'general': 'pages:main_page',
            'category_list': 'portfolio:category_list',
            'chunk_list': 'portfolio:portfolio_list',
            'chunk_inside': 'portfolio:portfolio_inside',
        })
