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

                            var params = null;
                            if (arguments)
                                params = arguments;
                            callback.call(obj, event, this, params);
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
         * @param block {string} block_cl
         * @param storage {string} storage_el
         *
         * @return {null} null
         * */
        this.storageSet = function (key, value, block, storage) {
            var block_cl = this.block_cl;
            var storage_el = this.storage_el;

            if (block) {
                block_cl   = block;
                storage_el = storage;
            }

            $(block_cl + storage_el).each(
                function (index, object) {
                    $.data(object, key, value);
                }
            );
        };

        /**
         * Get value from storage.
         *
         * @param key {string} key pushed
         * @param block {string} block_cl
         * @param storage {string} storage_el
         *
         * @return value {string}
         * */
        this.storageGet = function (key, block, storage) {
            var block_cl = this.block_cl;
            var storage_el = this.storage_el;

            if (block) {
                block_cl   = block;
                storage_el = storage;
            }

            var value = null;
            $(block_cl + storage_el).each(
                function (index, object) {
                    value = $.data(object, key);
                }
            );
            return value;
        };

        /**
         * Remove all data from storage.
         *
         * @return value {string}
         * */
        this.storageRemoveAll = function (block, storage) {
            var block_cl = this.block_cl;
            var storage_el = this.storage_el;

            if (block) {
                block_cl   = block;
                storage_el = storage;
            }
            $(block_cl + storage_el).removeData();
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
    var block_class = '';
    var center_block_class = ' .main-catalog-center-wrapper';
    var filter_block_class = ' .main-catalog-filter-wrapper';
    var menu_block_class = ' .main-catalog-menu-wrapper';
    var block_storage = ' .main-catalog-storage';
    var node_storage = ' .storage';


    /**
    * General class of block
    *
    * */
    function MainController (center_block_cl,
                             filter_block_cl,
                             menu_block_cl,
                             node_storage_el) {

        this.center_block_cl = center_block_cl;
        this.filter_block_cl = filter_block_cl;
        this.menu_block_cl = menu_block_cl;
        this.node_storage_el = node_storage_el;

        this.initialize = function () {

            this.bindMsg (document, 'catalog_reload', this.nodeCollectHandler, true);
            this.bindMsg (document, 'catalog_node_storage', this.eventsCounterHandler, true);

        };


        this.nodeCollectHandler = function (event, target) {
            this.publishMsg ([this.menu_block_cl, this.filter_block_cl, this.center_block_cl],
                             'catalog_node_collect',
                             null);
        };


        this.eventsCounterHandler = function (event, target, params) {
            var block = null;
            if (params)
                block = params[1];
            this.storageSet (block, 1);

            var center = this.storageGet ('center');
            var filter = this.storageGet ('filter');
            var menu = this.storageGet ('menu');

            if (center && filter && menu) {
                this.reloadPage(false, null);
                this.storageRemoveAll();
            }
        };


        this.reloadPage = function (ajax_load, ajax_response) {

            // Collect data from all zone catalog in area site
            var data = this.collectData();

            if (!ajax_load) {
                var data_ajax = this.addAjaxType(data);
                this.getProductList(data_ajax);
            } else {
                var data_browser = data;
                this.setBrowserLink(data_browser);
                this.setProductList(ajax_response);

                this.publishMsg (this.center_block_cl, 'catalog_reload_center');
                this.publishMsg (this.filter_block_cl, 'catalog_reload_filter');
                this.publishMsg (this.menu_block_cl, 'catalog_reload_menu');
            }
        };


        /**
        * Collect data from the objects:
        * 1. page - page in pagination list
        * 2. display_type - type of display products (grid|list)
        * 3. order - order of products (by name , by name desc, etc...)
        * 4. row_count - count of products in row (when grid display_type)
        *
        * @return {{page_no: null, page_start: null, page_stop: null, order: null, grid: null, price_from: null, price_to: null, stock_from: null, stock_to: null, brand_id_s: null, link: null}} null
        * */
        this.collectData = function () {

            var page_no = this.storageGet ('page_no',
                this.center_block_cl, this.node_storage_el);
            var page_start = this.storageGet ('page_start',
                this.center_block_cl, this.node_storage_el);
            var page_stop = this.storageGet ('page_stop',
                this.center_block_cl, this.node_storage_el);
            var order = this.storageGet ('order',
                this.center_block_cl, this.node_storage_el);
            var grid = this.storageGet ('grid',
                this.center_block_cl, this.node_storage_el);

            var price_from = this.storageGet ('price_from',
                this.filter_block_cl, this.node_storage_el);
            var price_to = this.storageGet ('price_to',
                this.filter_block_cl, this.node_storage_el);
            var stock_from = this.storageGet ('stock_from',
                this.filter_block_cl, this.node_storage_el);
            var stock_to = this.storageGet ('stock_to',
                this.filter_block_cl, this.node_storage_el);
            var brand_id_s = this.storageGet ('brand_id_s',
                this.filter_block_cl, this.node_storage_el);

            var link = this.storageGet ('link',
                this.menu_block_cl, this.node_storage_el);

            //noinspection JSValidateTypes
            return {
                'page_no': page_no,
                'page_start': page_start,
                'page_stop': page_stop,
                'order': order,
                'grid': grid,

                'price_from': price_from,
                'price_to': price_to,
                'stock_from': stock_from,
                'stock_to': stock_to,
                'brand_id_s': brand_id_s,

                'link': link
            };
        };


        /**
         * Adding request type for server, than server will know
         * what request it receive (browser, ajax)
         *
         * @param {object} data Data object of options to GET request
         * @return {object} Data object of new options.
         * */
        this.addAjaxType = function (data) {
            return $.extend({'ajax': 1}, data);
        };


        /**
         * Get Product List from server.
         *
         * @param {object} options Params for send in GET method.
         *
         * @return {object} return node_list.
         * */
        this.getProductList = function (options) {

            var link = options.link;
            delete options.link;

            $.ajax(
                {
                    context: this,
                    url: link,
                    method: 'GET',
                    async: true,
                    data: options,
                    complete: function (response) {
                        if (response.status === 200) {
                            this.reloadPage(true, $.parseHTML(response.responseText));
                        }
                        else {
                            throw 'Not get response: ' + response.status;
                        }
                    }
                }
            );
        };

        /**
         * Set Product List into DOM.
         *
         * @param {object} node_list Object of fragments with keys
         * center, sidebar, filter.
         *
         * @return {null}
         * */
        this.setProductList = function (node_list) {
            $(this.center_block_cl).html($(node_list).
                filter(this.center_block_cl).children());

            $(this.filter_block_cl).html($(node_list).
                filter(this.filter_block_cl).children());
        };

        /**
         * Set browser link for request on server
         * without ajax and has same data
         *
         * @param {object} options object of data to set in link
         * */
        this.setBrowserLink = function (options) {
            delete options.link;
            window.history.replaceState({}, '', '?' + $.param(options));
        }
    }

    var channel_node = new ChannelNode ();
    var data_storage = new DataStorage (block_class, block_storage);
    var main_controller = new MainController (
        center_block_class, filter_block_class, menu_block_class, node_storage);
    $.extend(true, main_controller, channel_node, data_storage);
    main_controller.initialize();

})(jQuery);