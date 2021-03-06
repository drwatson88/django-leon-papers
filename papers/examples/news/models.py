# coding: utf-8


from django.db import models
from samples.container.models import Chunk, ChunkAttachment, ChunkSettings


class News(Chunk):

    class Meta:
        verbose_name = 'новости'
        verbose_name_plural = 'новости'


class NewsAttachment(ChunkAttachment):

    chunk = models.ForeignKey(News, verbose_name='новости',
                              related_name='chunk_attachment')

    class Meta:
        verbose_name = 'Дополнительный файл (изображение)'
        verbose_name_plural = 'Дополнительные файлы (изображения)'


class NewsSettings(ChunkSettings):

    class Meta:
        verbose_name = 'Настройка раздела новости'
        verbose_name_plural = 'Настройки раздела новости'
