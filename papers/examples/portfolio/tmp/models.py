# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from treebeard.mp_tree import MP_Node
import os
from pytils.translit import slugify

class Category(MP_Node):
  def path_for_object(instance,filename):
    filename1, fileext1 = os.path.splitext(unicode(filename))
    return 'upload_category/' + slugify(filename1)+fileext1

  parent = models.ForeignKey('self', verbose_name = 'Категория', blank = True, null = True,editable=False)
  title = models.CharField('Заголовок', max_length = 255)
  slug_title = models.SlugField('Имя для ссылки', unique = True)
  preview = models.CharField('Краткое описание', max_length = 2550)    
  content = models.TextField('Описание', blank = True, null = True)
  image = models.ImageField('Изображение', upload_to = path_for_object, blank = True, null = True)
  show = models.BooleanField('Показывать', default = True)

  title_seo = models.CharField('Заголовок для SEO', max_length = 255, blank = True, null = True)
  metakey = models.CharField('Meta key', max_length = 255, blank = True, null = True)
  metades = models.CharField('Meta des', max_length = 255, blank = True, null = True)

  def imgsize140x124(self):
    if self.image:
      if self.image.width*1000/self.image.height >= 140*1000/124:
        return "140"
    return "x124"  

  def imgmargintop140x124(self):
    if self.image:
      if self.image.width*1000/self.image.height >= 140*1000/124:
        return "margin-top:%spx;" % ( (124-(self.image.height*140/self.image.width))/2 ) 
    return "margin:auto;" 
    
  
  def getchildrens(self):
    return Category.get_children(self).filter(show=True)
  
  def gettovar(self):
    return Portfolio.objects.filter(category=self,show=True).order_by('position')
          
  class Meta:
    verbose_name = 'Категорию' 
    verbose_name_plural = 'Категории'

  def __unicode__(self):
    return (self.depth-1)*"---"+self.title

class Portfolio(models.Model):
  def path_for_object(instance,filename):
    filename1, fileext1 = os.path.splitext(unicode(filename))
    return 'upload_portfolio/' + slugify(filename1)+fileext1
  title = models.CharField('Заголовок', max_length = 128)
  slug_title = models.SlugField('Имя для ссылки', unique = True)
  category = models.ForeignKey(Category, verbose_name = 'Категория')  
  preview = models.CharField('Анонс', max_length = 2550)
  #client = models.URLField('Клиент (ссылка на сайт)', verify_exists=False, max_length = 256)
  image = models.ImageField('Изображение', upload_to = path_for_object, blank = True, null = True)
  #image1 = models.ImageField('Доп. изображение1', upload_to = 'upload_portfolio', blank = True, null = True)  
  #image2 = models.ImageField('Доп. изображение2', upload_to = 'upload_portfolio', blank = True, null = True)  
  #image3 = models.ImageField('Доп. изображение3', upload_to = 'upload_portfolio', blank = True, null = True)  
  #image4 = models.ImageField('Доп. изображение4', upload_to = 'upload_portfolio', blank = True, null = True)  
  #image5 = models.ImageField('Доп. изображение5', upload_to = 'upload_portfolio', blank = True, null = True)  
  #image6 = models.ImageField('Доп. изображение6', upload_to = 'upload_portfolio', blank = True, null = True)  
  pub_date = models.DateField('Дата публикации')
  content = models.TextField('Содержание')
  show = models.BooleanField('Показывать', default = True)
  position = models.IntegerField('Позиция', blank = True, null = True) 
  metatitle = models.CharField('Заголовок для SEO', max_length = 1000, blank = True, null = True)
  metakey = models.CharField('Meta key', max_length = 5000, blank = True, null = True)
  metades = models.CharField('Meta des', max_length = 5000, blank = True, null = True)
  
  def __unicode__(self):
    return self.title
  
  def imgsize200x150(self):
    if self.image:
      if self.image.width*1000/self.image.height >= 200*1000/150:
        return "200"
    return "x150"  

  def imgmargintop200x150(self):
    if self.image:
      if self.image.width*1000/self.image.height >= 200*1000/150:
        return "margin-top:%spx;" % ( (150-(self.image.height*200/self.image.width))/2 ) 
    return "margin:auto;" 
    
        
  def save(self):
        model = self.__class__
        if self.position is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.position = last.position + 1
            except:
                # First row
                self.position = 0
        if not self.id:
          self.slug_title = slugify(self.slug_title)
        super(Portfolio, self).save()

  class Meta:
    ordering = ('position', )
    verbose_name = 'Работа в портфолио'
    verbose_name_plural = 'Работы в портфолио'

class MSettings(models.Model):
  title = models.CharField('Заголовок раздела', max_length = 128)
  content = models.TextField('Контент основной страницы раздела', blank = True, null = True)
  metatitle = models.CharField('Заголовок для SEO', max_length = 1000, blank = True, null = True)
  metakey = models.CharField('Meta key', max_length = 5000, blank = True, null = True)
  metades = models.CharField('Meta des', max_length = 5000, blank = True, null = True)       
  class Meta:
    verbose_name = 'Настройка раздела Портфолио'
    verbose_name_plural = 'Настройки раздела Портфолио'