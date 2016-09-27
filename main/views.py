# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from .models import Slider


def main_page(request):
    slides = Slider.objects.filter(show=True).order_by('position')
    return render_to_response(
        'firstpage/main_page.html',
        {
            'active_slide': slides[0],
            'nonactive_slides': slides[1:],
            }, context_instance=RequestContext(request),)