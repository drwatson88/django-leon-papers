# coding: utf-8


from django.db import models
from samples.rack.models import Category, Chunk, ChunkAttachment, ChunkSettings


class SpecialoffersCategory(Category):

    class Meta:
        verbose_name = 'Категория спецпредложения на сайте'
        verbose_name_plural = 'Категории спецпредложения на сайте'


class Specialoffers(Chunk):

    category = models.ForeignKey(SpecialoffersCategory, verbose_name='Категория спецпредложения')

    class Meta:
        verbose_name = 'спецпредложения'
        verbose_name_plural = 'спецпредложения'


class SpecialoffersAttachment(ChunkAttachment):

    chunk = models.ForeignKey(Specialoffers, verbose_name='спецпредложения',
                              related_name='chunk_attachment')

    class Meta:
        verbose_name = 'Дополнительный файл (изображение)'
        verbose_name_plural = 'Дополнительные файлы (изображения)'


class SpecialoffersSettings(ChunkSettings):

    class Meta:
        verbose_name = 'Настройка раздела спецпредложения'
        verbose_name_plural = 'Настройки раздела спецпредложения'
