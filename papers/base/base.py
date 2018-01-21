# -*- coding: utf-8 -*-

from leon.apps.base import BaseView, BaseParamsValidatorMixin


class PapersParamsValidatorMixin(BaseParamsValidatorMixin):

    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _use_category_validator(value, default):
        return value

    @staticmethod
    def _category_slug_title_validator(value, default):
        if value:
            return value
        return default

    @staticmethod
    def _chunk_slug_title_validator(value, default):
        if value:
            return value
        return default


class PapersBaseView(BaseView):

    """ Class Base for all Papers Class Views
        When request is received, then
    """

    pass
