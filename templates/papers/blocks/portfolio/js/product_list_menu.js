;(function ($) {

    "use strict";


    /**
    * Class of interface message
    * */
    function ChannelNode () {

        this.bindMsg = function (receivers, msg, callback, prevent) {
            var obj = this;
            $(function () {
                if (!(receivers instanceof Array))
                    receivers = [receivers];
                for (var i in receivers) {
                    $(receivers[i]).bind(
                        msg,
                        function (event) {
                            if (prevent)
                                event.preventDefault();
                            callback.call(obj, event, this);
                        }
                    );
                }
            });
        };

        this.publishMsg = function (listeners, msg, params) {
            $(function () {
                if (!(listeners instanceof Array))
                    listeners = [listeners];
                for (var i in listeners) {
                    $(listeners[i]).trigger(msg, params);
                }
            });
        };
    }


    /**
    * Class of storage node.
    *
    * @param block_cl {string} block class
    * @param storage_el {string} storage element
    * */
    function DataStorage (block_cl, storage_el) {
        this.block_cl   = block_cl;
        this.storage_el = storage_el;

        /**
         * Push value in storage.
         *
         * @param key {string} key pushed
         * @param value {string} value pushed
         *
         * @return {null} null
         * */
        this.storageSet = function (key, value) {
            $(this.block_cl + this.storage_el).each(
                function (index, object) {
                    $.data(object, key, value);
                }
            );
        };

        /**
         * Get value from storage.
         *
         * @param key {string} key pushed
         *
         * @return value {string}
         * */
        this.storageGet = function (key) {
            var value = null;
            $(this.block_cl + this.storage_el).each(
                function (index, object) {
                    value = $.data(object, key);
                }
            );
            return value;
        };
    }


    /**
    * Global DOM variables and prefixes:
    *
    *   Variables:
    *   - block_class: class in DOM object, that
    *       directly get this block
    *   - dom_storage: storage element
    *   - dom_page_inst: 'li' instance of pagination line
    *   - dom_grid_inst: '.display a' instance of grid choice
    *   - dom_order_inst: 'select option' instance of order choice
    *
    *
    *   Prefixes:
    *   - page_active_pfx - prefix for active page
    *   - order_select_pfx - prefix 'select' for order list
    *
    * */
    var block_class = ' .main-catalog-menu-wrapper';
    var dom_storage = ' .storage';

    var dom_menu_head = ' .menu-head';
    var dom_menu_root = ' .menu-root-list';
    var dom_link_selected = ' .menu-current-list .list-group a.selected';


    /**
    * General class of block
    *
    * */
    function MenuController (block_cl,
                             storage_el,
                             menu_head,
                             menu_root,
                             link_selected) {

        this.block_cl = block_cl;
        this.storage_el = storage_el;
        this.menu_head = menu_head;
        this.menu_root = menu_root;
        this.link_selected = link_selected;


        this.initialize = function () {
            this.rootListHandler();
            this.bindMsg (this.block_cl, 'catalog_node_collect', this.collectData, true);
        };

        /**
         * Function control hide-show catalog root-list
         * */
        this.rootListControl = function (el, menu_root) {

            var menuRootListHide = function() {
                $(el).find(menu_root).each(function(){
                    var $child = $(this);
                    $child.hide();
                });
            };

            var menuRootListShow = function() {
                $(el).find(menu_root).each(function(){
                    var $child = $(this);
                    $child.show();
                });
            };

            var $this = $(el);
            $this.hoverIntent({
                over: menuRootListShow,
                out: menuRootListHide,
                timeout: 100
            });
        };


        this.rootListHandler = function () {
            var obj = this;
            $(this.block_cl + this.menu_head).each(
                function (index, el) {
                    obj.rootListControl (el, obj.menu_root)
                }
            );

        };


        /**
        * Collect data from the objects in filter:
        * 1. link - link catalog
        *
        * and save all data in filter storage DOM object.
        *
        * @return {null} null
        * */
        this.collectData = function (event, target) {

            // Link variables
            var link = $($(this.block_cl + this.link_selected)[0]).attr('href');

            this.storageSet ('link', link);

            this.publishMsg (document, 'catalog_node_storage', ['menu']);
        };
    }

    var channel_node = new ChannelNode ();
    var data_storage = new DataStorage (block_class, dom_storage);
    var menu_controller = new MenuController (block_class,
                                              dom_storage,
                                              dom_menu_head,
                                              dom_menu_root,
                                              dom_link_selected);
    $.extend(true, menu_controller, channel_node, data_storage);
    menu_controller.initialize();

})(jQuery);



