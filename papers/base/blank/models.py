# coding: utf-8


import os

from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib

from django.db import models


class Category(MP_Node):

    """ Sample model for "category".

    """

    upload_directory = ''

    def chunk_upload_path(self, instance):
        return os.path.join(self.upload_directory, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).
                                   hexdigest(), '.jpg'))

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True)
    preview = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    image = models.ImageField(verbose_name='Путь к файлу картинки',
                              blank=True, max_length=255,
                              upload_to=chunk_upload_path)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True, null=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True,
                                 null=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True,
                                null=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True,
                                null=True)

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


class Chunk(models.Model):

    """ Sample model for "chunk".

        Redefined model fields:
        category - FK for category
    """

    upload_directory = ''

    def default_slug_title(self):
        return slugify('{}'.format(self.title))[:255]

    def default_code(self):
        return hashlib.md5(slugify(self.title).
                           encode(encoding='utf-8')).\
            hexdigest()

    def chunk_upload_path(self, instance):
        return os.path.join(self.upload_directory, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).
                                   hexdigest(), '.jpg'))

    title = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', max_length=255,
                                  blank=True, unique=True)

    preview = models.TextField(verbose_name='Описание', blank=True)
    content = models.TextField(verbose_name='Полное описание', blank=True)
    pub_date = models.DateField(verbose_name='Дата публикации')
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    image = models.ImageField(verbose_name='Путь к файлу картинки',
                              blank=True, max_length=255,
                              upload_to=chunk_upload_path)
    show = models.BooleanField(verbose_name='Показывать', default=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255,
                                 blank=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = self.default_slug_title()
        super(Chunk, self).save()

    class Meta:
        ordering = ('position',)
        abstract = True

    def __str__(self):
        return self.title


class ChunkAttachment(models.Model):

    """ Sample model for "chunk attachment".

        Redefined model fields:
        chunk - FK for "chunk" model
    """

    MEANINGS = (
        (0, 'Изображение'),
        (1, 'Файл')
    )

    upload_directory = ''

    def chunk_attachment_upload_path(self):
        return os.path.join(self.upload_directory, '{}{}'.
                            format(hashlib.md5(slugify(self.desc).
                                               encode(encoding='utf-8')).
                                   hexdigest(), '.jpg'))

    meaning = models.IntegerField(verbose_name='Тип файла', choices=MEANINGS)
    file = models.FileField(verbose_name='URL доп.файла',
                            upload_to=chunk_attachment_upload_path,
                            blank=True)
    image = models.ImageField(verbose_name='URL доп.картинки',
                              upload_to=chunk_attachment_upload_path,
                              blank=True)
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


class ChunkSettings(models.Model):

    """ Sample model for "setting".
    """

    title = models.CharField(verbose_name='Заголовок раздела', max_length=128)
    content = models.TextField(verbose_name='Контент основной страницы раздела',
                               blank=True, null=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=1000,
                                 blank=True, null=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=5000,
                                blank=True, null=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=5000,
                                blank=True, null=True)

    class Meta:
        abstract = True
