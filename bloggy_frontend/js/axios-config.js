(function (root, $, undefined) {
    "use strict";

    jQuery(function () {
        initAxisConfigs();
    });

    function initAxisConfigs() {
        // axios.defaults.headers.common['X-CSRF-TOKEN'] = $('meta[name="csrf_token"]').attr('content');
        // axios.defaults.headers.common['X-CSRFToken'] = $('meta[name="csrf_token"]').attr('content');

        // console.log("csrf_token: " + $('meta[name="csrf_token"]').attr('content'));
        // axios.defaults.headers.common['X-CSRFToken'] = $('meta[name="csrf_token"]').attr('content');
        // axios.defaults.headers.common['X-CSRFToken'] = $('meta[name="csrf_token"]').attr('content');

        // axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        // axios.defaults.xsrfCookieName = "csrftoken";

        // axios.defaults.xsrfCookieName = 'csrftoken';
        // axios.defaults.xsrfHeaderName = 'dontpickme';
        // axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
}(this, jQuery));


