# -*- coding: utf-8 -*-


import json


class ConverterMixin(object):

    class CenterChunk(object):

        def __init__(self, node_obj):
            self.title = node_obj.title
            self.preview = node_obj.preview
            self.content = node_obj.content
            self.pub_date = node_obj.pub_date
            self.image = {
                'src': node_obj.image
            }
            self.extra = json.loads(node_obj.extra.extra_field) \
                if node_obj.extra.check() else {}
            for k, v in self.extra:
                setattr(self, k, v)

    class CenterChunkNode(object):

        def __init__(self, node_obj):
            self.title = node_obj.title
            self.preview = node_obj.preview
            self.date = node_obj.pub_date
            self.comments_count = None
            self.link = {'href': '/{}/{}/{}/'.format('articles', 'article', node_obj.slug_title)}
            self.image = {
                'src': node_obj.image
            }
            self.extra = json.loads(node_obj.extra.extra_field) \
                if node_obj.extra.check() else {}
            for k, v in self.extra:
                setattr(self, k, v)

    class MenuSidebarNode(object):
        """
        Class for MainMenu objects-nodes
        """
        def __init__(self, node_obj, active):
            self.name = node_obj.title
            self.link = {'href': '/{}/{}/{}/'.format(
                    'articles', 'category', node_obj.slug_title)}
            self.options = {'count': node_obj.count(),
                            'active': active}
            self.children = []

    def _format_breadcrumbs(self):
        """
        Breadcrumb converter
        :return:
        """
        self.breadcrumb_page.update({'title': self.BREADCRUMB_TITLE})
        self.breadcrumb_page.update({'path_links': []})
        self.breadcrumb_page['path_links'].append({'title': self.GENERAL_LABEL,
                                                   'href': self.GENERAL_LINK, 'active': False})
        self.breadcrumb_page['path_links'].append({'title': self.APP_LABEL,
                                                   'href': '/{}/category/'.format(self.APP_NAME),
                                                   'active': False})

        if self.parent_current_category:
            self.breadcrumb_page['path_links'].append({'title': self.parent_current_category.title,
                                                       'href': '/{}/{}/{}/'.
                                                       format(self.APP_NAME,
                                                              'category',
                                                              self.parent_current_category.slug_title),
                                                       'active': False})

        if self.current_category and self.current_category != self.parent_current_category:
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
        for item in self.category_s.order_by('-numchild'):
            self.__recursive_node_append(item, main_menu_storage)
        self.menu_sidebar.update({
            'title': 'Категории раздела {}'.format(self.APP_LABEL),
            'menu': main_menu_storage
        })

    def __recursive_node_append(self, node_obj, storage):
        active = False
        if (node_obj.pk == self.parent_current_category) or \
                (node_obj.pk == self.current_category):
            active = True
        node = self.MenuSidebarNode(node_obj, active)
        storage.append(node)
        for item in node_obj.get_show_children():
            self.__recursive_node_append(item, node.children)

    def _format_center_chunk(self):
        self.center_chunk = self.CenterChunk(self.chunk)

    def _format_center_list(self):

        chunk_node_s = []
        for item in self.chunk_obj_s:
            node = self.CenterChunkNode(item)
            chunk_node_s.append(node)

        self.paper_list = [chunk_node_s[k: k + self.CHUNK_GRID_COUNT]
                           for k in range(0, len(chunk_node_s) // self.CHUNK_GRID_COUNT +
                                          (1 if len(chunk_node_s) % self.CHUNK_GRID_COUNT else 0))]
