/* ==========================================================================
 * Dropdown.js
 * ==========================================================================
 * Copyright 2021 Ajs.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ========================================================================== */

+function ($) {
    'use strict';

    // - Dropdown
    //
    //## Dropdown definition.

    $(window).on('load', function () {

        $('.dropdown [data-toggle="dropdown"]').click(function() {
            $(this).next('.dropdown-menu').toggle();
            return false;
        });

        $(document).click(function(e) {
            if (!$(e.target).is('.dropdown') && !$(e.target).parents().is('.dropdown')) {
                $('.dropdown-menu').hide();
            }
        });

    })

}(jQuery);


/* ==========================================================================
 * Copyable.js
 * ==========================================================================
 * Copyright 2021 Ajs.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ========================================================================== */

+function ($) {
    'use strict';

    // SCROLL CLASS DEFINITION
    // ======================

    const Copyable = function (element, options) {
        this.options = $.extend({}, {
            target: null
        }, options)

        this.$element = $(element)

        const self = this

        this.$element.on('click', function (e) {
            // stop event propagation
            e.stopPropagation();

            let $btn = $(this);

            // copy content to clipboard
            self.copy();

            $btn.html($btn.data('postActionText'));
            $btn.attr('disabled', 'true');

            setTimeout(function() {
              $btn.html($btn.data('originalText'));
              $btn.removeAttr('disabled');
            }, 3000);

            // grant that event wont be propagated
            return false;
        });

    }

    Copyable.prototype.copy = function () {
        if (!this.options.target) {
            return false;
        }

        const elementId = this.options.target.replace('#', '');
        const range = document.createRange();
        range.selectNode(document.getElementById(elementId));
        window.getSelection().addRange(range);
        document.execCommand("copy");
        window.getSelection().removeAllRanges();
    }

    function Plugin(option) {
        return this.each(function () {
            const self = $(this);
            const data = self.data('px.copyable');
            const opts = typeof option == 'object' && option;

            if (!data) {
                self.data('px.copyable', new Copyable(this, opts))
            }

            if (typeof option == 'string'){
                data[option]()
            }
        })
    }

    $.fn.copyable = Plugin
    $.fn.copyable.Constructor = Copyable

    // - Copyable
    //
    //## Copy a value to clipboard.

    $(window).on('load', function () {
        // init elements
        $('[data-copy]').each(function () {
            Plugin.call($(this), { target: $(this).data('copy') })
        })
    })

}(jQuery);
