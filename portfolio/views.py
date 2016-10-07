# -*- coding: utf-8 -*-


from django.shortcuts import render_to_response, \
    get_object_or_404, HttpResponse
from django.template import RequestContext

from .base import PortfolioBaseView, PortfolioParamsValidatorMixin
from .models import Category, Portfolio


CATEGORY_GRID_COUNT = 4
PORTFOLIO_GRID_COUNT = 3


class CategoryListView(PortfolioBaseView, PortfolioParamsValidatorMixin):

    """ Category List View.

    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'root_category_s': None
        }
        super(CategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.root_category_s = list()
        category_s_prev = Category.get_root_nodes().filter(show=True).all()

        p = 0
        while p < len(category_s_prev):
            self.root_category_s.append(category_s_prev[p:p+CATEGORY_GRID_COUNT])
            p += CATEGORY_GRID_COUNT

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._aggregate()
        return render_to_response(
            'papers/blocks/portfolio/category_list_general.html',
            self.output_context,
            context_instance=RequestContext(self.request), )


class PortfolioListView(PortfolioBaseView, PortfolioParamsValidatorMixin):

    """ Portfolio List View.
    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'category_s': None,
            'current_category': None,
            'portfolio_s': None,
        }
        super(PortfolioListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, catalog_slug_title):
        self.category_s = Category.get_root_nodes()
        self.current_category = Category.objects.filter(
                slug_title=catalog_slug_title)[0]

        for cat in self.category_s:
            cat.selected = True if cat.id == self.current_category.id else False

    def _portfolio_s_query(self, ):
        portfolio_obj_s = Portfolio.objects.order_by('position').all()
        self.portfolio_s = [portfolio_obj_s[k: k + PORTFOLIO_GRID_COUNT]
                            for k in range(0, len(portfolio_obj_s)//PORTFOLIO_GRID_COUNT)]

    def _aggregate(self):
        for item in self.output_context:
            self.output_context[item] = getattr(self, item)

    def get(self, *args, **kwargs):
        self._category_s_query(self.kwargs['catalog_slug_title'])
        self._portfolio_s_query()
        self._aggregate()
        return render_to_response(
            'papers/blocks/portfolio/portfolio_list_general.html',
            self.output_context,
            context_instance=RequestContext(self.request), )


class PortfolioInsideView(PortfolioBaseView, PortfolioParamsValidatorMixin):

    """ Portfolio Inside View. Receives get params
        and response neither arguments in get
        request params.

        ALL PARAMS put in params_storage after validate
    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'portfolio': None,
            'category_s': None,
            'current_category': None,
        }
        super(PortfolioInsideView, self).__init__(*args, **kwargs)

    def _set_portfolio(self, portfolio_slug_title):
        self.portfolio = get_object_or_404(Portfolio, slug_title=portfolio_slug_title)

    def _category_s_query(self):
        self.category_s = Category.get_root_nodes()
        self.current_category = self.portfolio.category

        for cat in self.category_s:
            cat.selected = True if cat.id == self.current_category.id else False

    def _set_portfolio_image(self):
        self.portfolio.image_current = self.portfolio.image

    def _set_portfolio_attach_image_s(self):
        self.portfolio.attach_images = self.portfolio.portfolioattachment_set.filter(meaning=1)

    def _set_portfolio_attach_file_s(self):
        self.portfolio.attach_files = self.portfolio.portfolioattachment_set.filter(meaning=0)

    def _get_amount(self):
        self.total_price = 0

    def get(self, *args, **kwargs):
        self._set_portfolio(self.kwargs['portfolio_slug_title'])
        self._set_portfolio_image()
        self._set_portfolio_attach_image_s()
        self._set_portfolio_attach_file_s()
        self._category_s_query()
        self._get_amount()
        self._aggregate()
        return render_to_response(
            'papers/blocks/portfolio/portfolio_inside_general.html',
            self.output_context,
            context_instance=RequestContext(self.request), )