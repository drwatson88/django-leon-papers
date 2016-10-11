# -*- coding: utf-8 -*-


from samples.container.views import ChunkListView, ChunkInsideView
from .base import ArticlesBaseView, ArticlesParamsValidatorMixin
from .models import Articles


GENERAL_LINK = 'pages:main_page'
GENERAL_LABEL = 'Главная'
APP_NAME = 'articles'
APP_LABEL = 'Новости'


class ArticlesListView(ChunkListView, ArticlesParamsValidatorMixin):

    """ Articles List View.
    """

    CHUNK_MODEL = Articles

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL


class ArticlesInsideView(ChunkInsideView, ArticlesParamsValidatorMixin):

    """ Articles Inside View.
    """

    CHUNK_MODEL = Articles

    GENERAL_LINK = GENERAL_LINK
    GENERAL_LABEL = GENERAL_LABEL
    APP_NAME = APP_NAME
    APP_LABEL = APP_LABEL
