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

    var dom_image_zoom = ' .image-zoom';
    var dom_image_selected = ' ul li img';

    /**
    * General class of block
    *
    * */
    function CenterController (block_cl,
                               storage_el,
                               image_zoom,
                               image_selected_el) {

        this.block_cl = block_cl;
        this.storage_el = storage_el;
        this.image_zoom = image_zoom;
        this.image_selected_el = image_selected_el;

        this.initialize = function () {

            //this.bindMsg(this.block_cl + this.add_button, 'click', this.tabsEventHandler, true);
            $(this.block_cl + this.image_zoom).WMZoom();
        };
    }

    var channel_node = new ChannelNode ();
    var data_storage = new DataStorage (block_class, dom_storage);
    var center_controller = new CenterController (block_class,
                                                  dom_storage,
                                                  dom_image_zoom,
                                                  dom_image_selected);
    $.extend(true, center_controller, channel_node, data_storage);
    center_controller.initialize();

})(jQuery);