import * as bootstrap from 'bootstrap'

// import 'bootstrap';
// const jQuery = require("jquery")
// require("bootstrap")
// require("@popperjs/core")


global.$ = global.jQuery = require('jquery');
import "../sass/style.scss";

window.axios = require('axios');
// require('./app/cookie');
require('./app/toast');
require('./app/heading');
require('./app/toc');
require('./app/bookmark');
require('./app/copyCode');
require('./app/newsletter');

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

$(document).ready(function () {
    console.log("Jquery loaded")
    // Animated Counter for home page
    const counters = document.getElementsByClassName("value-counter");
    for (const element of counters) {
        let duration = element.getAttribute("duration")
        if (duration === 'underfined') {
            duration = 1000;
        }
        animateValue(element, 1, element.getAttribute("max-value"), duration);
    }

    $(window).scroll(function () {
        var y = $(window).scrollTop();
        if (y > 0) {
            $("#main-navbar").addClass('--not-top');
        } else {
            $("#main-navbar").removeClass('--not-top');
        }
    });

})