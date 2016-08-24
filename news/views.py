# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import News, MSettings


def news_inside(request, slug_title):

    return render_to_response('news/news_inside.html',
    {
        'new': get_object_or_404(News, slug_title=slug_title, show=True),
    }, context_instance=RequestContext(request), )


def news_list(request):

    return render_to_response('news/news_list.html',
    {
        'news': News.objects.filter(show=True).order_by('-pub_date'),
        'settingsp': MSettings.objects.get(id=1),
    }, context_instance=RequestContext(request), )


class NewsList(ListView):

    template = 'news/news_list.html'
    model = News


class NewsDetail(DetailView):

    template = 'news/news_inside.html'
    model = News
    fields = ['title', 'slug_title', 'preview', 'image',
              'pub_date', 'content', 'show']
