/**
 * Vue is a modern JavaScript library for building interactive web interfaces
 * using reactive data binding and reusable components. Vue's API is clean
 * and simple, leaving you to focus on building your next great project.
 */

import Vue from 'vue/dist/vue.js';

Vue.component("comments", () => import("./vue/disqus/Comments.vue"));
Vue.component('contact-form', () => import('./vue/disqus/ContactForm.vue'));
Vue.component('cookie-consent', () => import('./vue/CookieConsent.vue'));
window.addEventListener('load', function () {
    window.axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const app = new Vue({
        el: '#vueRoot',
    });
}, false);

Vue.config.devtools = true;