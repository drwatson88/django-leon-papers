# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from .base import PagesBaseView, PagesParamsValidatorMixin
from .models import Slider


class MainPageView(PagesBaseView, PagesParamsValidatorMixin):

    """ Main Page View.
    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'active_slide': None,
            'nonactive_slides': None,
        }
        super(MainPageView, self).__init__(*args, **kwargs)

    def _slide_s_query(self):
        self.active_slide = Slider.objects.all()[0]
        self.nonactive_slides = Slider.objects.all()[1:]

    def get(self, *args, **kwargs):
        self._slide_s_query()
        self._aggregate()
        return render_to_response(
            'papers/blocks/pages/main_page.html',
            self.output_context,
            context_instance=RequestContext(self.request), )


class AboutPageView(PagesBaseView, PagesParamsValidatorMixin):

    """ About Page View.
    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
        }
        super(AboutPageView, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._aggregate()
        return render_to_response(
            'papers/blocks/pages/about_page.html',
            self.output_context,
            context_instance=RequestContext(self.request), )
