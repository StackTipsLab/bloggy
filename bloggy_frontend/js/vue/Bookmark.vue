<template>
  <button name="bookmark-button" @click.prevent="onBookmarkClick(postId, postType)"
          v-bind:class="(verticalAlignment)?'pulse-button':'pulse-button horizontal-layout'">
    <template v-if="userBookmarkCount > 0">
      <span class="reaction__icon--active">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" role="img" aria-hidden="true"
             class="crayons-icon">
          <path
              d="M5 2h14a1 1 0 011 1v19.143a.5.5 0 01-.766.424L12 18.03l-7.234 4.536A.5.5 0 014 22.143V3a1 1 0 011-1z"></path>
        </svg>
      </span>
    </template>
    <template v-else>
      <span class="reaction__icon--inactive">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" role="img" aria-hidden="true"
             class="crayons-icon">
          <path
              d="M5 2h14a1 1 0 011 1v19.143a.5.5 0 01-.766.424L12 18.03l-7.234 4.536A.5.5 0 014 22.143V3a1 1 0 011-1zm13 2H6v15.432l6-3.761 6 3.761V4z"></path>
          </svg>
      </span>
    </template>
    <div class="vote-count" id="vote-count">
      {{ this.count }}
    </div>
  </button>
</template>
<script>
import Api from './Api.js'

export default {
  props: {
    postId: {type: String, required: true},
    postType: {type: String, required: true},
    count: {type: Number, required: false},
    userBookmarkCount: {type: Number, required: false},
    verticalAlignment: {type: Boolean, required: false}
  },
  data() {
    return {}
  },
  methods: {
    onBookmarkClick: function (postId, postType) {
      const postBody = {post_id: postId, post_type: postType};
      let url = `${window.location.origin}/${Api.bookmark}`;
      axios.post(url, postBody)
          .then(response => {
            console.log("Response:" + response);
            this.count = response.data.count;
            this.userBookmarkCount = response.data.userBookmarkCount;
          })
          .catch(error => {
            console.log("Error:" + error);
            alert('Join Stacktips to start earning reputation and unlocking new privileges like voting and bookmarking.')
          });
    }
  }
}

</script>