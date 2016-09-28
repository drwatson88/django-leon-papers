# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from .base import MainBaseView, MainParamsValidatorMixin
from .models import Slider


class MainPageView(MainBaseView, MainParamsValidatorMixin):

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
            'active_slide': None,
            'nonactive_slides': None,
        }
        super(MainPageView, self).__init__(*args, **kwargs)

    def _aggregate(self):
        for item in self.output_context:
            self.output_context[item] = getattr(self, item)

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