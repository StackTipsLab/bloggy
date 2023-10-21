window.Cookies = require('../../vendor/js.cookie');

(function (root, $, undefined) {
    "use strict";
    jQuery(function () {
        // DOM ready, take it away
        var cache = {
            $cookieCompliance: $('.header__cookies'),
            $cookieConfirmation: $('.button--cookie')
        };

        /**
         * Init function for icocookies module.
         * @override
         */
        function init() {
            if (!Cookies.get('__stacktips_web_cookies')) {
                showCookieCompliance();
                addEventListeners();
            } else {
                removeCookieCompliance();
            }
        }

        function showCookieCompliance() {
            cache.$cookieCompliance.slideDown();
        }

        function removeCookieCompliance() {
            cache.$cookieCompliance.slideUp(400, function () {
                cache.$cookieCompliance.remove();
            });
        }

        function addEventListeners() {
            cache.$cookieConfirmation.on('click', acceptCookies);
        }

        function acceptCookies(e) {
            e.preventDefault();
            Cookies.set("__stacktips_web_cookiess", "true", {
                expires: 365,
                path: "/"
            });
            removeCookieCompliance();
        }

        init();

        // Public API
        return {};
    });

}(this, jQuery));
