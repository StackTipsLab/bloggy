<template>
    <section class="section bg-grey" v-if="Object.keys(JsonData.testimonials).length > 0">
        <div class="container">
            <header class="section__header">
                <h2 class="section__header--title">{{JsonData.title}}</h2>
                <p class="lead">{{JsonData.lead}}</p>
            </header>
            <div class="card-deck mt-5">
                <template v-for="(Testimony, index) in JsonData.testimonials">
                    <!-- wrap every 2 on lg-->
                    <div v-if="index>0 && index % 3 === 0" class="w-100 d-none d-lg-block my-lg-3"></div>
                    <!-- wrap every 3 on md-->
                    <div v-if="index>0 && index % 2 === 0" class="w-100 d-none d-md-block d-lg-none my-md-2"></div>
                    <div class="card testimonial">
                        <div class="card-body">
                            <p class="testimonial__quoted--text">{{Testimony.quote}}</p>
                            <div class="media align-items-center pt-2">
                                <a :href="Testimony.url" target="_blank">
                                    <img class="testimonial__user--avatar" :src="Testimony.avatar" :alt="Testimony.name">
                                </a>
                                <div class="media-body lh-1">
                                    <h6 class="mb-0">{{Testimony.name}}</h6>
                                    <small>{{Testimony.strapline}}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </section>
</template>
<script>
    import TestimonialsJson from "../json/twitter-testimonials.json"
    export default {
        name: "Testimonials",
        data() {
            return {
                JsonData: TestimonialsJson,
            }
        },
    }
</script>