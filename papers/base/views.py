# coding: utf-8


import os
from django.shortcuts import render, get_object_or_404, redirect
from .base import PapersParamsValidatorMixin, PapersBaseView


class PapersArticleListView(PapersBaseView, PapersParamsValidatorMixin):
    """ Article List View.

        ARTICLE_MODEL - class of db "article" model.
        TEMPLATE - class of db "template" model.
    """
    ARTICLE_MODEL = None

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'article_set': None,
            'app_title': None
        }
        super(PapersArticleListView, self).__init__(*args, **kwargs)

    def _article_s_query(self, ):
        self.article_set = self.ARTICLE_MODEL.objects.filter(show=True).all()

    def get(self, *args, **kwargs):
        self._article_s_query()
        self._aggregate()
        return self._render()


class PapersArticleInsideView(PapersBaseView, PapersParamsValidatorMixin):

    """ Article Inside View. Receives get params
        and response neither arguments in get
        request params.

        ARTICLE_MODEL - class of db "category" model.
    """

    ARTICLE_MODEL = None

    kwargs_params_slots = {
        'article_slug_title': [None, '']
    }

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'post': None
        }
        super(PapersArticleInsideView, self).__init__(*args, **kwargs)

    def _article_set(self):
        slug_title = self.params_storage['chunk_slug_title']
        self.post = self.ARTICLE_MODEL.objects.get(slug_title=slug_title)

    def _get(self):
        self._article_set()
        self._aggregate()
        return self._render()
