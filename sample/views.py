# -*- coding: utf-8 -*-


from django.shortcuts import render_to_response, \
    get_object_or_404, HttpResponse
from django.template import RequestContext

from .base import ChunkBaseView, ChunkParamsValidatorMixin


CATEGORY_GRID_COUNT = 4
CHUNK_GRID_COUNT = 3


class CategoryListView(ChunkBaseView, ChunkParamsValidatorMixin):

    """ Category List View.

        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    CATEGORY_MODEL = None
    CHUNK_MODEL = None

    TEMPLATE = 'papers/blocks/sample/category_list_general.html'

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'root_category_s': None
        }
        super(CategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.root_category_s = list()
        category_s_prev = self.CATEGORY_MODEL.get_root_nodes().filter(show=True).all()

        p = 0
        while p < len(category_s_prev):
            self.root_category_s.append(category_s_prev[p:p+CATEGORY_GRID_COUNT])
            p += CATEGORY_GRID_COUNT

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._aggregate()
        return render_to_response(
            self.TEMPLATE,
            self.output_context,
            context_instance=RequestContext(self.request), )


class ChunkListView(ChunkBaseView, ChunkParamsValidatorMixin):

    """ Chunk List View.

        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    CATEGORY_MODEL = None
    CHUNK_MODEL = None

    TEMPLATE = 'papers/blocks/sample/sample_list_general.html'

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'category_s': None,
            'current_category': None,
            'portfolio_s': None,
        }
        super(ChunkListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, catalog_slug_title):
        self.category_s = self.CATEGORY_MODEL.get_root_nodes()
        self.current_category = self.CATEGORY_MODEL.objects.filter(
                slug_title=catalog_slug_title)[0]

        for cat in self.category_s:
            cat.selected = True if cat.id == self.current_category.id else False

    def _chunk_s_query(self, ):
        chunk_obj_s = self.CHUNK_MODEL.objects.order_by('position').all()
        self.chunk_s = [chunk_obj_s[k: k + CHUNK_GRID_COUNT]
                            for k in range(0, len(chunk_obj_s)//CHUNK_GRID_COUNT)]

    def _aggregate(self):
        for item in self.output_context:
            self.output_context[item] = getattr(self, item)

    def get(self, *args, **kwargs):
        self._category_s_query(self.kwargs['catalog_slug_title'])
        self._chunk_s_query()
        self._aggregate()
        return render_to_response(
            self.TEMPLATE,
            self.output_context,
            context_instance=RequestContext(self.request), )


class ChunkInsideView(ChunkBaseView, ChunkParamsValidatorMixin):

    """ Portfolio Inside View. Receives get params
        and response neither arguments in get
        request params.

        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    CATEGORY_MODEL = None
    CHUNK_MODEL = None

    TEMPLATE = 'papers/blocks/sample/sample_inside_general.html'

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'portfolio': None,
            'category_s': None,
            'current_category': None,
        }
        super(ChunkInsideView, self).__init__(*args, **kwargs)

    def _set_chunk(self, chunk_slug_title):
        self.chunk = get_object_or_404(self.CHUNK_MODEL, slug_title=chunk_slug_title)

    def _category_s_query(self):
        self.category_s = self.CATEGORY_MODEL.get_root_nodes()
        self.current_category = self.chunk.category

        for cat in self.category_s:
            cat.selected = True if cat.id == self.current_category.id else False

    def _set_chunk_image(self):
        self.chunk.image_current = self.chunk.image

    def _set_chunk_attach_image_s(self):
        self.chunk.attach_images = self.chunk.chunkattachment_set.filter(meaning=1)

    def _set_chunk_attach_file_s(self):
        self.chunk.attach_files = self.chunk.chunkattachment_set.filter(meaning=0)

    def _get_amount(self):
        self.total_price = 0

    def get(self, *args, **kwargs):
        self._set_chunk(self.kwargs['chunk_slug_title'])
        self._set_chunk_image()
        self._set_chunk_attach_image_s()
        self._set_chunk_attach_file_s()
        self._category_s_query()
        self._get_amount()
        self._aggregate()
        return render_to_response(
            self.TEMPLATE,
            self.output_context,
            context_instance=RequestContext(self.request), )


