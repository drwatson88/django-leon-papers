# coding: utf-8


import os

from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib

from django.db import models


class BaseMixin(object):

    """ Base Mixin
    """

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True)
    preview = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    pub_date = models.DateField(verbose_name='Дата публикации')


class ShowMixin(object):

    """ Show Mixin
    """

    show = models.BooleanField(verbose_name='Показывать', default=True)


class PositionMixin(object):

    """ Position Mixin
    """

    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)


class SeoMixin(object):

    """ Main Seo fields Mixin
    """

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True, null=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True,
                                 null=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True,
                                null=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True,
                                null=True)


class ImageUploadMixin(object):

    """ Image Upload Mixin - use upload_directory 
        for set DIR, where save images
    """

    upload_image_directory = ''

    def image_upload_path(self, instance):
        return os.path.join(self.upload_image_directory, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).
                                   hexdigest(), '.jpg'))

    image = models.ImageField(verbose_name='Путь к файлу картинки',
                              blank=True, max_length=255,
                              upload_to=image_upload_path)


class FileUploadMixin(object):

    """ File Upload Mixin - use upload_directory 
        for set DIR, where save files
    """

    upload_file_directory = ''

    def file_upload_path(self, instance):
        return os.path.join(self.upload_file_directory, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).
                                   hexdigest(), '.jpg'))

    file = models.FileField(verbose_name='URL доп.файла',
                            upload_to=file_upload_path,
                            blank=True)


class Category(MP_Node, BaseMixin, SeoMixin, ImageUploadMixin, ShowMixin, PositionMixin):

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


class Chunk(models.Model, BaseMixin, SeoMixin, ImageUploadMixin, ShowMixin, PositionMixin):

    """ Sample model for "chunk".

        Redefined model fields:
        category - FK for category
    """

    def default_slug_title(self):
        return slugify('{}'.format(self.title))[:255]

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = self.default_slug_title()
        super(Chunk, self).save()

    class Meta:
        ordering = ('position',)
        abstract = True

    def __str__(self):
        return self.title


class ChunkAttachment(models.Model, ImageUploadMixin, FileUploadMixin):

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


class ChunkSettings(models.Model, SeoMixin, BaseMixin, PositionMixin, ShowMixin):

    """ Sample model for "setting".
    """

    class Meta:
        abstract = True
