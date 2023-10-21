<template>
  <Transition name="bounce">
  <div class="cookie-consent-banner" v-if="show">
    <div class="cookies-banner__close-button" @click="dismiss">[X]</div>
    <div class="cookie-consent-banner__inner">
      <div class="cookie-consent-banner__copy">
        <div class="cookie-consent-banner__description">

          Cookies and IP addresses allow us to deliver and improve our web content and to provide you with a
          personalized experience. Our website uses cookies and collects your IP address for these purposes.
          <br>
          <br>
          By using our site, you acknowledge that you have read and understood our
          <a href="/cookie-policy/" target="_blank">cookie policy</a> and
          <a href="/privacy-policy/" target="_blank">privacy policy.</a>
        </div>
      </div>

      <div class="cookie-consent-banner__actions mt-3">
        <a @click="saveCookieChoice" class="btn btn-sm btn-primary">
          Yes, I agree
        </a>

        <a @click="dismiss" class="btn btn-sm btn-secondary">
          No, thanks
        </a>
      </div>
    </div>
  </div>
  </Transition>

</template>

<script>
export default {
  name: "CookieConsent",
  computed: {
    cookie() {
      return !this.getCookie(this.cookieName)
    }
  },
  beforeMount() {
    let delay = 2000;
    setTimeout(() => {
      this.show = this.cookie
    }, delay)
  },
  data: function () {
    return {
      cookieName: "stacktips_cookie__consent",
      cookieExpiryDays: 365,
      // cookieDomain: window.location.hostname,
      cookieDomain: "stacktips.com",
      cookiePath: '/',
      show: undefined
    }
  },

  methods: {
    dismiss() {
      this.show = false
    },
    saveCookieChoice() {
      this.show = false
      this.setCookie(this.cookieName, 1, this.cookieExpiryDays, this.cookieDomain, this.cookiePath)
    },
    getCookie(name) {
      const value = `;${document.cookie}`
      const parts = value.split(`; ${name}=`)
      return parts.length !== 2 ?
          undefined :
          parts.pop().split(';').shift()
    },
    setCookie(name, value, expiryDays, domain, path) {
      const exdate = new Date()
      exdate.setDate(exdate.getDate() + (expiryDays || 365))
      const cookie = [
        `${name}=${value}`,
        `expires=${exdate.toUTCString()}`,
        `path=${(path || '/')}`
      ]
      if (domain) {
        cookie.push('domain=${domain}')
      }
      document.cookie = cookie.join(';')
    }
  }
}
</script>