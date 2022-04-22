/* ==========================================================================
 * select.js
 * ========================================================================== */
'use strict';
{
    const $ = django.jQuery;

    const init = function($element, options) {
        const settings = $.extend({}, options);
        $element.select2(settings);
    };

    $.fn.djangoAdminSelect = function(options) {
        const settings = $.extend({}, options);

        $.each(this, function(i, element) {
            const $element = $(element);
            init($element, settings);
        });

        return this;
    };

    $(function() {
        // Initialize all autocomplete widgets except the one in the template
        // form used when a new formset is added.
        $('.admin-select').not('[name*=__prefix__]').djangoAdminSelect();
    });

    $(document).on('formset:added', (function() {
        return function(event, $newFormset) {
            return $newFormset.find('.admin-select').djangoAdminSelect();
        };
    })(this));
}