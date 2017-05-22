# coding: utf-8


import os
from django.shortcuts import render, \
    get_object_or_404, redirect

from .base import ChunkBaseView, ChunkParamsValidatorMixin
from .converters import ConverterMixin


class ExtraMixin(object):
    """ Class for additional methods, params.
    """

    GENERAL_LINK = 'sample_pages:general_view'
    GENERAL_LABEL = 'Главная'
    APP_NAME = 'sample'
    APP_LABEL = 'Пример'

    def _set_dispatcher(self):
        self.dispatcher = {}
        self.dispatcher.update({
            'general': self.GENERAL_LINK,
            'category_list': '{app}:category_list'.format(app=self.APP_NAME),
            'chunk_list': '{app}:{app}_list'.format(app=self.APP_NAME),
            'chunk_inside': '{app}:{app}_inside'.format(app=self.APP_NAME),
        })

    def _set_labels(self):
        self.labels = {}
        self.labels.update({
            'app_label': self.APP_LABEL,
            'general_label': self.GENERAL_LABEL,
        })


class ChunkCategoryListView(ChunkBaseView, ChunkParamsValidatorMixin, ExtraMixin, ConverterMixin):
    """ Category List View.

        CATEGORY_GRID_COUNT - count of grid category's
        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """
    CATEGORY_GRID_COUNT = 4
    CATEGORY_MODEL = None
    CHUNK_MODEL = None
    TEMPLATE = None

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {}
        super(ChunkCategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.root_category_s = list()
        category_s_prev = self.CATEGORY_MODEL.get_root_nodes().filter(show=True).all()

        p = 0
        while p < len(category_s_prev):
            self.root_category_s.append(category_s_prev[p:p + self.CATEGORY_GRID_COUNT])
            p += self.CATEGORY_GRID_COUNT

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._set_dispatcher()
        self._set_labels()
        self._aggregate()
        return render(
                self.request,
                self.TEMPLATE,
                self.output_context)


class ChunkListView(ChunkBaseView, ChunkParamsValidatorMixin):

    """ Chunk List View.

        BREADCRUMB_TITLE - title for breadcrumb
        CHUNK_GRID_COUNT - count of grid chunks.
        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    BREADCRUMB_TITLE = ''
    CHUNK_GRID_COUNT = 2
    CATEGORY_MODEL = None
    CHUNK_MODEL = None
    SETTINGS_MODEL = None
    TEMPLATE = None

    kwargs_params_slots = {
        'category_slug_title': [None, ''],
        'use_category': [None, True]
    }

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {}
        super(ChunkListView, self).__init__(*args, **kwargs)
        self.category_input_s = list()
        self.category_s = list()

        self.current_category = None
        self.parent_current_category = None

    def _category_s_query(self, ):
        if self.params_storage['use_category']:

            self.category_s = self.CATEGORY_MODEL.get_root_nodes()
            self.current_category = self.CATEGORY_MODEL.objects.filter(
                    slug_title=self.params_storage['category_slug_title'])[0] \
                if self.params_storage['category_slug_title'] else None

            self.parent_current_category = self.current_category.get_parent() \
                if self.current_category else None
            if not self.parent_current_category:
                self.parent_current_category = self.current_category

    def _chunk_obj_s_query(self, ):
        if self.params_storage['use_category'] and self.current_category:
            self.category_input_s.extend([self.current_category.pk])
            self.category_input_s.extend(self.current_category.get_children().
                                         values_list('id', flat=True))
            self.chunk_obj_s = self.CHUNK_MODEL.objects. \
                filter(category__in=self.category_input_s). \
                order_by('position').all()
        else:
            self.chunk_obj_s = self.CHUNK_MODEL.objects. \
                order_by('position').all()

    def _chunk_settings(self):
        self.chunk_settings_obj = self.SETTINGS_MODEL.objects.first() \
            if self.SETTINGS_MODEL.objects.all() else None

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._chunk_obj_s_query()
        self._chunk_settings()

        self._format_mixin_s()

        self._aggregate()
        return render(
                self.request,
                self.TEMPLATE,
                self.output_context)


class ChunkInsideBaseView(ChunkBaseView, ChunkParamsValidatorMixin):

    """ Portfolio Inside View. Receives get params
        and response neither arguments in get
        request params.

        BREADCRUMB_TITLE - title for breadcrumb
        CHUNK_GRID_COUNT - count of grid chunks.
        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    BREADCRUMB_TITLE = ''
    CATEGORY_MODEL = None
    CHUNK_MODEL = None
    TEMPLATE = None

    kwargs_params_slots = {
        'chunk_slug_title': [None, ''],
        'use_category': [None, True]
    }

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {}
        super(ChunkInsideBaseView, self).__init__(*args, **kwargs)
        self.category_input_s = list()
        self.category_s = list()
        self.current_category = None
        self.parent_current_category = None

    def _set_chunk(self):
        self.chunk = get_object_or_404(self.CHUNK_MODEL,
                                       slug_title=self.kwargs['chunk_slug_title'])

    def _category_s_query(self):
        if self.params_storage['use_category']:
            self.category_s = self.CATEGORY_MODEL.get_root_nodes()
            self.current_category = self.chunk.category
            self.parent_current_category = self.current_category.get_parent()

    def _set_chunk_image(self):
        self.chunk.image_current = self.chunk.image

    def _set_chunk_attach_image_s(self):
        self.chunk.attach_images = self.chunk.chunk_attachment.filter(meaning=1).all()

    def _set_chunk_attach_file_s(self):
        self.chunk.attach_files = self.chunk.chunk_attachment.filter(meaning=0).all()


class ChunkInsideView(ChunkInsideBaseView, ChunkParamsValidatorMixin):

    """ Chunk Inside View. Receives get params
        and response neither arguments in get
        request params.
    """

    def get(self, *args, **kwargs):
        self._set_chunk()
        self._set_chunk_image()
        self._set_chunk_attach_image_s()
        self._set_chunk_attach_file_s()

        self._category_s_query()

        self._format_mixin_s()
        self._aggregate()
        return render(
                self.request,
                self.TEMPLATE,
                self.output_context)


class ChunkInsideTemplateView(ChunkInsideBaseView, ChunkParamsValidatorMixin):
    """ Chunk Template Inside View. Receives 
        get params and response neither 
        arguments in get request params.
    """

    TEMPLATE_PATH = None
    TEMPLATE_NAME = None

    def _set_template(self):
        slug_title = self.kwargs['chunk_slug_title']
        template_path = os.path.join(self.TEMPLATE_PATH,
                                     '{}__inside.html'.format(slug_title
                                                              if slug_title
                                                              else self.TEMPLATE_NAME))
        self.template = template_path if os.path.exists(template_path) \
            else os.path.join(self.TEMPLATE_PATH, self.TEMPLATE_NAME)

    def get(self, *args, **kwargs):
        self._set_chunk()
        self._set_chunk_image()
        self._set_chunk_attach_image_s()
        self._set_chunk_attach_file_s()

        self._set_template()

        self._category_s_query()

        self._format_mixin_s()
        self._aggregate()
        return render(
                self.request,
                self.template,
                self.output_context)
