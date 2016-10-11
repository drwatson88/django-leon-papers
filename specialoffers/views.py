# -*- coding: utf-8 -*-


from samples.rack.views import CategoryListView, ChunkListView, ChunkInsideView
from .base import SpecialoffersBaseView, SpecialoffersParamsValidatorMixin
from .models import SpecialoffersCategory, Specialoffers


GENERAL_LINK = 'pages:main_page'
GENERAL_LABEL = 'Главная'
APP_NAME = 'specialoffers'
APP_LABEL = 'Новости'


class SpecialoffersCategoryListView(CategoryListView, SpecialoffersParamsValidatorMixin):

    """ Category List View.
    """

    CATEGORY_MODEL = SpecialoffersCategory

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL


class SpecialoffersListView(ChunkListView, SpecialoffersParamsValidatorMixin):

    """ Specialoffers List View.
    """

    CATEGORY_MODEL = SpecialoffersCategory
    CHUNK_MODEL = Specialoffers

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL


class SpecialoffersInsideView(ChunkInsideView, SpecialoffersParamsValidatorMixin):

    """ Specialoffers Inside View.
    """

    CATEGORY_MODEL = SpecialoffersCategory
    CHUNK_MODEL = Specialoffers

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL
