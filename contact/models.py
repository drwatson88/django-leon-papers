# -*- coding: utf-8 -*-

from django.db import models
import datetime


class Contact (models.Model):
    """ Контакт. """
    name = models.CharField(verbose_name='Имя', max_length=128)
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(verbose_name='Телефон', max_length=128)
    message = models.TextField(verbose_name='Сообщение')
    pub_date = models.DateTimeField(verbose_name="Дата и время сообщения", default=datetime.datetime.now())
    
    class Meta:
        ordering = ('-id', )
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    

class MSettings(models.Model):
    
    title = models.CharField(verbose_name='Заголовок раздела', max_length=128)
    content = models.TextField(verbose_name='Контент основной страницы раздела', blank=True, null = True)
    
    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255,
                                 blank=True)
    meta_key = models.CharField(verbose_name='Meta key', max_length=255, blank=True)
    meta_des = models.CharField(verbose_name='Meta des', max_length=255, blank=True)
    
    class Meta:
        verbose_name = 'Настройка раздела Контакты'
        verbose_name_plural = 'Настройки раздела Контакты'    