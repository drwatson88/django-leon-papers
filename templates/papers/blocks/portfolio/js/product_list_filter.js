;(function () {
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
    *   - dom_button: submit button in form
    *
    *   Inputs:
    *   - input_price_from - price from input
    *   - input_price_to - price to input
    *   - input_stock_from - stock from input
    *   - input_stock_to - stock to input
    *
    * */
    var block_class = ' .main-catalog-filter-wrapper';
    var dom_storage = ' .storage';
    var dom_button = ' .filter-button';
    var input_price_from = ' input[name="price-from"]';
    var input_price_to = ' input[name="price-to"]';
    var input_stock_from = ' input[name="edition-from"]';
    var input_stock_to = ' input[name="edition-to"]';
    var input_brands = ' input[name="makers"]';


    /**
    * General class of block
    *
    * */
    function FilterController (block_cl,
                               storage_el,
                               button,
                               price_from,
                               price_to,
                               stock_from,
                               stock_to,
                               brands) {

        this.block_cl = block_cl;
        this.brands = brands;
        this.storage_el = storage_el;
        this.button = button;
        this.price_from = price_from;
        this.price_to = price_to;
        this.stock_from = stock_from;
        this.stock_to = stock_to;


        this.initialize = function () {
            this.setupEvents();
            this.bindMsg (document, 'catalog_reload_filter', this.setupEventsHandler, false);
            this.bindMsg (this.block_cl, 'catalog_node_collect', this.collectData, true);
        };


        this._buttonEventHandler = function (event, target) {
            this.publishMsg (document, 'catalog_reload');
        };


        /**
        * Set events handlers in catalog_filter interface
        * elements.
        *
        * @return {null} null
        * */
        this.setupEvents = function () {
            //Button event
            this.bindMsg (this.block_cl + this.button, 'click', this._buttonEventHandler, true);
        };


        this.setupEventsHandler = function (event, target) {
            this.setupEvents();
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
        this.collectData = function () {

            // Price variables
            var price_from = $($(this.block_cl + this.price_from)[0]).val();
            var price_to = $($(this.block_cl + this.price_to)[0]).val();

            // stock variables
            var stock_from = $($(this.block_cl + this.stock_from)[0]).val();
            var stock_to = $($(this.block_cl + this.stock_to)[0]).val();

            // Brands variables
            var brand_id_s = [];
            var brands_nodes = $(this.block_cl + this.brands);
            $.each(brands_nodes, function(index, obj){
                if ($(obj).prop('checked')) {
                    brand_id_s.push(obj.value);
                }
            });

            this.storageSet ('price_from', price_from);
            this.storageSet ('price_to', price_to);
            this.storageSet ('stock_from', stock_from);
            this.storageSet ('stock_to', stock_to);
            this.storageSet ('brand_id_s', JSON.stringify(brand_id_s));

            this.publishMsg (document, 'catalog_node_storage', ['filter']);
        };
    }

    var channel_node = new ChannelNode ();
    var data_storage = new DataStorage (block_class, dom_storage);
    var filter_controller = new FilterController (block_class,
                                                  dom_storage,
                                                  dom_button,
                                                  input_price_from,
                                                  input_price_to,
                                                  input_stock_from,
                                                  input_stock_to,
                                                  input_brands);
    $.extend(true, filter_controller, channel_node, data_storage);
    filter_controller.initialize();

})(jQuery);