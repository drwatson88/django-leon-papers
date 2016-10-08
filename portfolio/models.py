# coding: utf-8


from django.db import models
from sample.models import Category, Chunk, ChunkAttachment, ChunkSettings


class PortfolioCategory(Category):

    class Meta:
        verbose_name = 'Категория портфолио на сайте'
        verbose_name_plural = 'Категории портфолио на сайте'


class Portfolio(Chunk):

    category = models.ForeignKey(PortfolioCategory, verbose_name='Категория портфолио')

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'


class PortfolioAttachment(ChunkAttachment):

    chunk = models.ForeignKey(Portfolio, verbose_name='Портфолио')

    class Meta:
        verbose_name = 'Дополнительный файл (изображение)'
        verbose_name_plural = 'Дополнительные файлы (изображения)'


class PortfolioSettings(ChunkSettings):

    class Meta:
        verbose_name = 'Настройка раздела Портфолио'
        verbose_name_plural = 'Настройки раздела Портфолио'
