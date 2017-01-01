# -*- coding: utf-8 -*-


from samples.rack.views import CategoryListView, ChunkListView, ChunkInsideView
from .base import PortfolioBaseView, PortfolioParamsValidatorMixin
from .models import PortfolioCategory, Portfolio


GENERAL_LINK = 'pages:main_page'
GENERAL_LABEL = 'Главная'
APP_NAME = 'portfolio'
APP_LABEL = 'Портфолио'


class PortfolioCategoryListView(CategoryListView, PortfolioParamsValidatorMixin):

    """ Category List View.
    """

    CATEGORY_MODEL = PortfolioCategory

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL


class PortfolioListView(ChunkListView, PortfolioParamsValidatorMixin):

    """ Portfolio List View.
    """

    CATEGORY_MODEL = PortfolioCategory
    CHUNK_MODEL = Portfolio

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL


class PortfolioInsideView(ChunkInsideView, PortfolioParamsValidatorMixin):

    """ Portfolio Inside View.
    """

    CATEGORY_MODEL = PortfolioCategory
    CHUNK_MODEL = Portfolio

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL
