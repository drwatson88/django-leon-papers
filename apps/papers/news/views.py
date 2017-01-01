# -*- coding: utf-8 -*-


from samples.container.views import ChunkListView, ChunkInsideView
from .base import NewsBaseView, NewsParamsValidatorMixin
from .models import News


GENERAL_LINK = 'pages:main_page'
GENERAL_LABEL = 'Главная'
APP_NAME = 'news'
APP_LABEL = 'Новости'


class NewsListView(ChunkListView, NewsParamsValidatorMixin):

    """ News List View.
    """

    CHUNK_MODEL = News

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL


class NewsInsideView(ChunkInsideView, NewsParamsValidatorMixin):

    """ News Inside View.
    """

    CHUNK_MODEL = News

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL
