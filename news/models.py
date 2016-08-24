# -*- coding: utf-8 -*-


from datetime import datetime
import os

from django.db import models
from django.template.defaultfilters import slugify


class News(models.Model):

    @staticmethod
    def path_for_object(ifile_name):
        file_name, file_ext = os.path.splitext(ifile_name)
        return 'upload_news/' + slugify(file_name) + file_ext

    title = models.CharField(verbose_name='Заголовок', max_length=128)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True)
    preview = models.CharField(verbose_name='Анонс', max_length=2550)
    image = models.ImageField(verbose_name='Миниатюра', upload_to=path_for_object,
                              blank=True, null=True)
    pub_date = models.DateField(verbose_name='Дата публикации', default=datetime.today())
    content = models.TextField(verbose_name='Содержание')
    show = models.BooleanField(verbose_name='Показывать', default=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255,
                                 blank=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.slug_title)
        super(News, self).save()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class MSettings(models.Model):

    title = models.CharField('Заголовок раздела', max_length=128)
    content = models.TextField('Контент основной страницы раздела', blank=True,
                               null=True)
    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255,
                                 blank=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Настройка раздела Новости'
        verbose_name_plural = 'Настройки раздела Новости'
