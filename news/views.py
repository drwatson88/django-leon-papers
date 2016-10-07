# -*- coding: utf-8 -*-


from django.shortcuts import render_to_response, \
    get_object_or_404, HttpResponse
from django.template import RequestContext

from .base import PortfolioBaseView, PortfolioParamsValidatorMixin
from .models import Category


CATEGORY_GRID_COUNT = 4


class CategoryListView(PortfolioBaseView, PortfolioParamsValidatorMixin):

    """ Category List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.

        ALL PARAMS put in params_storage after validate
    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'category_s': None
        }
        super(CategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.category_s = list()
        category_s_prev = Category.get_root_nodes().filter(show=True).all()

        p = 0
        while p < len(category_s_prev):
            self.category_s.append(category_s_prev[p:p+CATEGORY_GRID_COUNT])
            p += CATEGORY_GRID_COUNT

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._aggregate()
        return render_to_response(
            'papers/blocks/portfolio/category_list.html',
            self.output_context,
            context_instance=RequestContext(self.request), )


