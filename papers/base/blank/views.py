# coding: utf-8


from django.shortcuts import render, \
    get_object_or_404, redirect

from .base import ChunkBaseView, ChunkParamsValidatorMixin


class ExtraMixin:

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


class ChunkCategoryListView(ChunkBaseView, ChunkParamsValidatorMixin, ExtraMixin):

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
        self.output_context = {
            'root_category_s': None,
            'dispatcher': None,
            'labels': None,
        }
        super(ChunkCategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.root_category_s = list()
        category_s_prev = self.CATEGORY_MODEL.get_root_nodes().filter(show=True).all()

        p = 0
        while p < len(category_s_prev):
            self.root_category_s.append(category_s_prev[p:p+self.CATEGORY_GRID_COUNT])
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


class ChunkListView(ChunkBaseView, ChunkParamsValidatorMixin, ExtraMixin):

    """ Chunk List View.

        BREADCRUMB_TITLE - title for breadcrumb
        CHUNK_GRID_COUNT - count of grid chunks.
        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    BREADCRUMB_TITLE = 'Блог'
    CHUNK_GRID_COUNT = 2
    CATEGORY_MODEL = None
    CHUNK_MODEL = None
    TEMPLATE = None

    kwargs_params_slots = {
        'category_slug_title': [None, ''],
        'use_category': [None, True]
    }

    request_params_slots = {
    }

    class CenterChunkNode(object):

        def __init__(self, node_obj):
            self.title = node_obj.title
            self.preview = node_obj.preview
            self.date = node_obj.pub_date
            self.comments_count = None
            self.image = {
                'src': node_obj.image
            }

    class MenuSidebarNode(object):
        """
        Class for MainMenu objects-nodes
        """
        name = None
        link = {
            'href': None
        }
        options = {}
        children = []

        def __init__(self, node_obj, active):
            self.name = node_obj.title
            self.link['href'] = '/{}/{}/{}/'.format(
                    'articles', 'category', node_obj.slug_title)
            self.options.update({'count': node_obj.count,
                                 'active': active})

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'menu_sidebar': None,
            'paper_list': None,
            'breadcrumb_page': None,
        }
        super(ChunkListView, self).__init__(*args, **kwargs)
        self.category_input_s = list()
        self.category_s = list()
        self.menu_sidebar = {}
        self.paper_list = {}
        self.breadcrumb_page = {}
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
            self.chunk_obj_s = self.CHUNK_MODEL.objects.\
                filter(category__in=self.category_input_s).\
                order_by('position').all()
        else:
            self.chunk_obj_s = self.CHUNK_MODEL.objects.\
                order_by('position').all()

    def _format_breadcrumbs(self):
        self.breadcrumb_page.update({'title': self.BREADCRUMB_TITLE})
        self.breadcrumb_page.update({'path_links': []})
        self.breadcrumb_page['path_links'].append({'title': self.GENERAL_LABEL,
                                                   'href': self.GENERAL_LINK, 'active': False})
        self.breadcrumb_page['path_links'].append({'title': self.APP_LABEL,
                                                   'href': '/{}/'.format(self.APP_NAME),
                                                   'active': False})

        if self.parent_current_category:
            self.breadcrumb_page['path_links'].append({'title': self.parent_current_category.title,
                                                       'href': '/{}/{}/{}/'.
                                                       format(self.APP_NAME,
                                                              'category',
                                                              self.parent_current_category.slug_title),
                                                       'active': False})

        if self.current_category:
            self.breadcrumb_page['path_links'].append({'title': self.current_category.title,
                                                       'href': '/{}/{}/{}/'.
                                                       format(self.APP_NAME,
                                                              'category',
                                                              self.current_category.slug_title),
                                                       'active': False})

        self.breadcrumb_page['path_links'][-1]['active'] = True

    def _format_sidebar(self):
        """
        Method for format data from Django ORM format to widget format
        :return:
        """
        main_menu_storage = []
        for item in self.category_s:
            self._recursive_node_append(item, main_menu_storage)
        self.menu_sidebar.update({
            'title': 'Категории раздела {}'.format(self.APP_LABEL),
            'menu': main_menu_storage
        })

    def _recursive_node_append(self, node_obj, storage):
        active = False
        if (node_obj.pk == self.parent_current_category) or \
                (node_obj.pk == self.current_category):
            active = True
        node = self.MenuSidebarNode(node_obj, active)
        storage.append(node)
        for item in node_obj.get_show_children():
            self._recursive_node_append(item, node.children)

    def _format_center(self):

        chunk_node_s = []
        for item in self.chunk_obj_s:
            node = self.CenterChunkNode(item)
            chunk_node_s.append(node)

        self.paper_list = [chunk_node_s[k: k + self.CHUNK_GRID_COUNT]
                           for k in range(0, len(chunk_node_s)//self.CHUNK_GRID_COUNT)]

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._chunk_obj_s_query()

        self._set_dispatcher()
        self._set_labels()

        self._format_breadcrumbs()
        self._format_sidebar()
        self._format_center()

        self._aggregate()
        return render(
            self.request,
            self.TEMPLATE,
            self.output_context)


class ChunkInsideView(ChunkBaseView, ChunkParamsValidatorMixin, ExtraMixin):

    """ Portfolio Inside View. Receives get params
        and response neither arguments in get
        request params.

        CATEGORY_MODEL - class of db "category" model.
        CHUNK_MODEL - class of db "chunk" model.
        TEMPLATE - class of db "template" model.
    """

    CATEGORY_MODEL = None
    CHUNK_MODEL = None

    TEMPLATE = None

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'chunk': None,
            'category_s': None,
            'current_category': None,
            'dispatcher': None,
            'labels': None,
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
        self.chunk.attach_images = self.chunk.chunk_attachment.filter(meaning=1).all()

    def _set_chunk_attach_file_s(self):
        self.chunk.attach_files = self.chunk.chunk_attachment.filter(meaning=0).all()

    def _get_amount(self):
        self.total_price = 0

    def _format_breadcrumbs(self):
        pass

    def _format_sidebar(self):
        pass

    def _format_center(self):
        pass

    def get(self, *args, **kwargs):
        self._set_chunk(self.kwargs['chunk_slug_title'])
        self._set_chunk_image()
        self._set_chunk_attach_image_s()
        self._set_chunk_attach_file_s()
        self._category_s_query()
        self._get_amount()
        self._set_dispatcher()
        self._set_labels()
        self._format_breadcrumbs()
        self._format_sidebar()
        self._format_center()
        self._aggregate()
        return render(
            self.request,
            self.TEMPLATE,
            self.output_context)
