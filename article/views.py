# coding: utf-8

from django.views.generic import DetailView, ListView
from .models import Article


class ArticleView(DetailView):

    model = Article


class ArticleList(ListView):

    template = 'news/news_inside.html'
    model = Article
    fields = ['title', 'slug_title', 'preview', 'image',
              'pub_date', 'content', 'show']
