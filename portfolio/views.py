# -*- coding: utf-8 -*-


from sample.views import CategoryListView, ChunkListView, ChunkInsideView
from .base import PortfolioBaseView, PortfolioParamsValidatorMixin
from .models import PortfolioCategory, Portfolio


class PortfolioCategoryListView(CategoryListView, PortfolioParamsValidatorMixin):

    """ Category List View.
    """

    CATEGORY_MODEL = PortfolioCategory


class PortfolioListView(ChunkListView, PortfolioParamsValidatorMixin):

    """ Portfolio List View.
    """

    CATEGORY_MODEL = PortfolioCategory
    CHUNK_MODEL = Portfolio


class PortfolioInsideView(ChunkInsideView, PortfolioParamsValidatorMixin):

    """ Portfolio Inside View.
    """

    CATEGORY_MODEL = PortfolioCategory
    CHUNK_MODEL = Portfolio
