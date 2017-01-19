# -*- coding: utf-8 -*-

from leon.site_base import BaseView, BaseParamsValidatorMixin


class ChunkParamsValidatorMixin(BaseParamsValidatorMixin):

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


class ChunkBaseView(BaseView):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    pass
