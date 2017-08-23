# coding: utf-8


import os

from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib
from django.db import models

from leon.base.models import ImageUploadMixin, FileUploadMixin, SeoMixin


class BaseChunkMixin(models.Model):

    """ Base Mixin
    """

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True)
    preview = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    pub_date = models.DateField(verbose_name='Дата публикации')

    class Meta:
        abstract = True


class Category(MP_Node, BaseChunkMixin):

    """ Sample model for "category".
    """

    def count(self):
        return len(getattr(self, '{}_set'.format(self.Options.child_label)).all())

    def get_show_children(self):
        return self.get_children().filter(show=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.title)
        super(Category, self).save(**kwargs)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}{}'.format((self.depth - 1) * '---', self.title)


class Chunk(BaseChunkMixin):

    """ Sample model for "chunk".

        Redefined model fields:
        category - FK for category
    """

    def default_slug_title(self):
        return slugify('{}'.format(self.title))[:255]

    def save(self, **kwargs):
        if not self.id and not self.slug_title:
            self.slug_title = self.default_slug_title()
        super(Chunk, self).save()

    class Meta:
        ordering = ('position',)
        abstract = True

    def __str__(self):
        return self.title


class ChunkAttachment(ImageUploadMixin, FileUploadMixin):

    """ Sample model for "chunk attachment".

        Redefined model fields:
        chunk - FK for "chunk" model
    """

    MEANINGS = (
        (0, 'Изображение'),
        (1, 'Файл')
    )

    meaning = models.IntegerField(verbose_name='Тип файла', choices=MEANINGS)
    desc = models.CharField(verbose_name='Описание доп.файла или картинки',
                            max_length=255)

    def save(self, **kwargs):
        super(ChunkAttachment, self).save()

    class Meta:
        unique_together = ('chunk', 'meaning', 'desc')
        verbose_name = 'Дополнительный файл (изображение)'
        verbose_name_plural = 'Дополнительные файлы (изображения)'
        abstract = True

    def __str__(self):
        return self.desc


class ChunkSettings(SeoMixin, BaseChunkMixin, ImageUploadMixin):

    """ Sample model for "setting".
    """

    class Meta:
        abstract = True
