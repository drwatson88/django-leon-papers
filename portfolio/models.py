# coding: utf-8


import os

from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib

from django.db import models


class Category(MP_Node):

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True)
    preview = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True, null=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True,
                                 null=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True,
                                null=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True,
                                null=True)

    def getchildrens(self):
        return Category.get_children(self).filter(show=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.title)
        super(Category, self).save(**kwargs)

    class Meta:
        verbose_name = 'Категория на сайте'
        verbose_name_plural = 'Категории на сайте'

    def __str__(self):
        return '{}{}'.format((self.depth - 1) * '---', self.slug_title)


class Portfolio(models.Model):

    def default_slug_title(self):
        return slugify('{}_{}_{}'.format(self.maker, self.title, self.code))[:255]

    def default_code(self):
        return hashlib.md5(slugify(self.title).encode(encoding='utf-8')).hexdigest()

    def portfolio_upload_path(self, instance):
        return os.path.join('upload_product', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).hexdigest(), '.jpg'))

    category = models.ForeignKey(Category, verbose_name='Категория')
    title = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', max_length=255,
                                  blank=True, unique=True)

    preview = models.TextField(verbose_name='Описание', blank=True)
    content = models.TextField(verbose_name='Полное описание', blank=True)
    pub_date = models.DateField(verbose_name='Дата публикации')
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    image = models.ImageField(verbose_name='Путь к файлу картинки',
                              blank=True, max_length=255,
                              upload_to=portfolio_upload_path)
    show = models.BooleanField(verbose_name='Показывать', default=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255,
                                 blank=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True)

    def save(self, **kwargs):
        if not self.id and not self.import_fl:
            self.slug_title = self.default_slug_title()
        super(Portfolio, self).save()

    class Meta:
        ordering = ('position',)
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'

    def __str__(self):
        return self.title


class PortfolioAttachment(models.Model):

    MEANINGS = (
        (0, 'Изображение'),
        (1, 'Файл')
    )

    def portfolio_attachment_upload_path(self):
        return os.path.join('upload_attachment', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.desc).
                                               encode(encoding='utf-8')).
                                   hexdigest(), '.jpg'))

    portfolio = models.ForeignKey(Portfolio, verbose_name='Портфолио')
    meaning = models.IntegerField(verbose_name='Тип файла', choices=MEANINGS)
    file = models.FileField(verbose_name='URL доп.файла',
                            upload_to=portfolio_attachment_upload_path,
                            blank=True)
    image = models.ImageField(verbose_name='URL доп.картинки',
                              upload_to=portfolio_attachment_upload_path,
                              blank=True)
    desc = models.CharField(verbose_name='Описание доп.файла или картинки',
                            max_length=255)

    def save(self, **kwargs):
        super(PortfolioAttachment, self).save()

    class Meta:
        unique_together = ('portfolio', 'meaning', 'desc')
        verbose_name = 'Дополнительный файл (изображение)'
        verbose_name_plural = 'Дополнительные файлы (изображения)'

    def __str__(self):
        return self.desc


class MSettings(models.Model):

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
        verbose_name = 'Настройка раздела Портфолио'
        verbose_name_plural = 'Настройки раздела Портфолио'
