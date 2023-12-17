import 'flowbite';
import {createApp} from 'vue'

const app = createApp({})

import testimonials from './vue/Testimonials.vue'
import quizlet from './vue/quizlet.vue'

import './style.css'

app.component('testimonials', testimonials)
app.component('quizzes', quizlet)
app.mount('#vueRoot')
