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
    var block_class = ' .main-catalog-center-wrapper';
    var dom_storage = ' .storage';
    var dom_page_inst = ' .pagination li';
    var dom_grid_inst = ' .product-list-filter .display a';
    var dom_order_inst = ' .product-list-filter select.order-control';

    var page_active_pfx = ' .pagination .active';
    var order_select_pfx = ' .order-control [selected="selected"]';
    var grid_select_pfx = ' .display .active';


    /**
    * General class of block
    *
    * */
    function CenterController (block_cl,
                               storage_el,
                               page_inst,
                               grid_inst,
                               order_inst,
                               page_active,
                               order_active,
                               grid_active ) {

        this.block_cl = block_cl;
        this.storage_el = storage_el;
        this.page_inst = page_inst;
        this.grid_inst = grid_inst;
        this.order_inst = order_inst;
        this.page_active = page_active;
        this.order_active = order_active;
        this.grid_active = grid_active;


        this.initialize = function () {
            this.setupEvents();
            this.bindMsg (document, 'catalog_reload_center', this.setupEventsHandler, false);
            this.bindMsg (this.block_cl, 'catalog_node_collect', this.collectData, true);
        };


        this._pageEventHandler = function (event, target) {
            var page = $(target).attr('value');
            var page_start = $(target).data('page-start');
            var page_stop = $(target).data('page-stop');

            this.storageSet ('page_no', page);
            this.storageSet ('page_start', page_start);
            this.storageSet ('page_stop', page_stop);
            this.storageSet ('page_event', 1);

            this.publishMsg (document, 'catalog_reload');
        };


        this._orderEventHandler = function (event, target) {
            var order = target.value;

            this.storageSet ('order', order);
            this.storageSet ('order_event', 1);

            this.publishMsg (document, 'catalog_reload');
        };


        this._gridEventHandler = function (event, target) {
            var grid = $(target).data('grid');

            this.storageSet ('grid', grid);
            this.storageSet ('grid_event', 1);

            this.publishMsg (document, 'catalog_reload');
        };

        /**
        * Set events handlers in catalog_center interface
        * elements.
        *
        * @return {null} null
        * */
        this.setupEvents = function () {
            //Page event
            this.bindMsg (this.block_cl + this.page_inst, 'click', this._pageEventHandler, true);

            //Order event
            this.bindMsg (this.block_cl + this.order_inst, 'change', this._orderEventHandler, true);

            //Grid event
            this.bindMsg (this.block_cl + this.grid_inst, 'click', this._gridEventHandler, true);
        };


        this.setupEventsHandler = function (event, target) {
            this.setupEvents();
        };


        this._getExclude = function (items) {
            var exclude_node = null;
            for (var i in items) {
                if (this.storageGet(items[i]))
                    exclude_node = items[i];
            }
            return exclude_node;
        };

        /**
        * Collect data from the objects in filter:
        * 1. page - page in pagination list
        * 2. display_type - type of display products (grid|list)
        * 3. order - order of products (by name , by name desc, etc...)
        * 4. row_count - later - count of products in row (when grid display_type)
        *
        * and save all data in center storage DOM object.
        *
        * @return {null} null
        * */
        this.collectData = function (event, target) {

            var exclude_node = this._getExclude(['page_event', 'order_event', 'grid_event']);

            if (exclude_node !== 'page_event') {
                var page_no = null;
                var page_start = null;
                var page_stop = null;

                $(this.block_cl + this.page_active).each(
                    function(index, object){
                        page_no = $(object).attr('value');
                        page_start = $(object).data('page-start');
                        page_stop = $(object).data('page-stop');
                    }
                );

                this.storageSet('page_no', page_no);
                this.storageSet('page_start', page_start);
                this.storageSet('page_stop', page_stop);
            }

            if (exclude_node !== 'order_event') {
                var order = null;
                $(this.block_cl + this.order_active).each(
                    function(index, object){
                        order = $(object).val();
                    }
                );
                this.storageSet ('order', order);
            }

            if (exclude_node !== 'grid_event') {
                var grid = null;
                $(this.block_cl + this.grid_active).each(
                    function (index, object){
                        grid = $(object).data('grid');
                    }
                );
                this.storageSet ('grid', grid);
            }

            this.publishMsg (document, 'catalog_node_storage', ['center']);
        };
    }

    var channel_node = new ChannelNode ();
    var data_storage = new DataStorage (block_class, dom_storage);
    var center_controller = new CenterController (block_class,
                                                  dom_storage,
                                                  dom_page_inst,
                                                  dom_grid_inst,
                                                  dom_order_inst,
                                                  page_active_pfx,
                                                  order_select_pfx,
                                                  grid_select_pfx);
    $.extend(true, center_controller, channel_node, data_storage);
    center_controller.initialize();

})(jQuery);