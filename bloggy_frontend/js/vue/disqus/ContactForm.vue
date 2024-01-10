<template>
  <div class="">
    <form @submit.prevent="submit" @reset="onReset" method="post" role="form" class="update-profile-form contact-form">
      <div class="col-md-7">

        <template v-if="this.submitMessage">
          <div :class="['alert mb-2', 'alert-' + this.submitStatus]">{{ this.submitMessage }}</div>
        </template>

        <div class="form-group ">
          <label for="userName">Your name<sup class="text-danger">*</sup></label>
          <input type="text" name="userName" v-model="userName" class="form-control" id="userName" required>
        </div>
        <div class="form-group">
          <label for="name">Your email<sup class="text-danger">*</sup></label>
          <div :class="['input-group', isEmailValid()]">
            <input type="email" class="form-control" v-model="email" name="email" id="email" required>
          </div>
        </div>
        <div class="form-group mt-3">
          <label for="website">Your website</label>
          <input type="text" class="form-control" v-model="website" name="website" id="website" required>
        </div>
      </div>
      <div class="form-group mt-3">
        <label for="message">Your message<sup class="text-danger">*</sup></label>
        <textarea class="form-control" v-model="message" id="message" name="message" rows="5" required></textarea>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-secondary" @click.prevent="onReset">Reset form</button>
        <button type="submit" class="btn btn-primary" @click.prevent="onSubmit">Send message</button>
      </div>
      <small>This site is protected by reCAPTCHA and the Google
        <a href="https://policies.google.com/privacy">Privacy Policy</a> and
        <a href="https://policies.google.com/terms">Terms of Service</a> apply.</small>
    </form>

  </div>
</template>
<script>
import Api from '../Api.js'

export default {
  name: "ContactForm",
  data() {
    return {
      userName: "",
      email: "",
      message: "",
      website: "",
      submitMessage: undefined,
      submitStatus: '',
      reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/,
    };
  },
  mounted() {
    let recaptchaScript = document.createElement('script')
    recaptchaScript.setAttribute('src', 'https://www.google.com/recaptcha/api.js?render=6Lf70xIcAAAAAE8G94jdsyl67tFPckUMHCMf3ExE')
    document.head.appendChild(recaptchaScript)
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


    onReset() {
      this.userName = "";
      this.email = "";
      this.message = "";
      this.submitMessage = "";
      this.website = "";
    },
    onSubmit(e) {
      if (this.email === "") {
        this.submitStatus = "danger"
        this.submitMessage = "Please enter a valid email"
        return;
      }


      grecaptcha.ready(function () {
        grecaptcha.execute('6Lf70xIcAAAAAE8G94jdsyl67tFPckUMHCMf3ExE', {action: 'submit'})
            .then((token) => {
              // if (!a.formValid) {
              //   return;
              // }
              const postBody = {
                name: userName._value,
                email: email._value,
                message: message._value,
                website: website._value,
                reCaptchaResponse: token
              };

              axios.post(`${window.location.origin}/${Api.contact}`, postBody)
                  .then((response) => {
                    this.submitStatus = "success";
                    this.submitMessage = "Your message has been sent. Thank you!";
                  })
                  .catch((error) => {
                    this.submitStatus = "danger";
                    this.submitMessage = "Something went wrong. Please try again later.";
                  });
            });
      });

    },
  },
};
</script>