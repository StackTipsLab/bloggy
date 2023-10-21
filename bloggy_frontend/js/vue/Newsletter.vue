<template>
  <section :class="widgetStyle">
    <div class="sidebar-widget newsletter-subscribe" id="newsletterSection">
      <div class="intro mb-2">
        <h3 class="sidebar-widget-title">
          <span class="c-link c-link--branded text-primary">Subscribe</span> our newsletter
        </h3>
        <p class="mb-1">{{ widgetMessage }}</p>
        <div class="mb-2"><small class="text-muted">We promise no spam.</small></div>
        <template v-if="message">
          <div :class="['alert mb-2', 'alert-' + this.status]">{{ message }}</div>
        </template>

        <form class="d-flex-row" method="post">
          <div class="input-group">
            <input class="form-control mb-2" type="name" required name="name" placeholder="Your name" v-model="name">
          </div>

          <div :class="['input-group', isEmailValid()]">
            <input class="form-control mb-2" type="email" name="email" placeholder="Your email" v-model="email"/>
          </div>

          <button type="submit" @click.prevent="subscribeNewsletter()"
                  class="btn btn-primary justify-center w-100 mt-2 mb-0">{{ widgetButtonLabel }}
          </button>
        </form>
      </div>

    </div>
  </section>
</template>
<script>
import Api from "./Api";

export default {
  props: {
    widgetStyle: {
      type: String,
      required: false,
      default: "bg-gray"
    },
    widgetMessage: String,
    widgetButtonLabel: {
      type: String,
      default: "SUBSCRIBE"
    },
  },
  data: function () {
    return {
      status: '',
      message: undefined,
      email: '',
      reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/,
      name: null,
    };
  },
  methods: {
    isEmailValid: function () {
      if (this.email === "") {
        return "";
      } else if (this.reg.test(this.email)) {
        return 'has-success';

      } else {
        return 'was-validated form-control:invalid'
      }
    },
    subscribeNewsletter: function () {
      if (this.email === "" || !this.reg.test(this.email)) {
        this.status = "danger"
        this.message = "Please enter a valid email"
        return;
      }


      this.message = undefined;
      console.log("SubscribeNewsletter:: posting comment to server: " +
          JSON.stringify({email: this.email, name: this.name}));

      let url = `${window.location.origin}/${Api.newsletter}`;
      axios.post(url, {email: this.email, name: this.name})
          .then(response => {
            console.log("Response:" + response);
            this.status = "success"
            this.message = "Thank you for subscribing"

          })
          .catch(error => {
            console.error('There was an error!', error);

            this.status = "error"
            this.message = "Oops! Something went wrong!"
          });
    }
  }
}
</script>