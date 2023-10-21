<template>
  <button name="like-button" @click.prevent="onVoteClick(postId, postType)"
          v-bind:class="(verticalAlignment)?'pulse-button':'pulse-button horizontal-layout'">

    <template v-if="userVoteCount > 0">
      <span class="reaction__icon--active">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" role="img"
             aria-labelledby="a70h7v8cbcf18yl2a7nyjv0jkqz6lsba"
             class="crayons-icon crayons-icon reaction-icon--like reaction-icon reacted">
          <title id="a70h7v8cbcf18yl2a7nyjv0jkqz6lsba">Like comment:</title>
          <path
              d="M5.116 12.595a4.875 4.875 0 015.56-7.68h-.002L7.493 8.098l1.06 1.061 3.181-3.182a4.875 4.875 0 016.895 6.894L12 19.5l-6.894-6.894.01-.01z"></path>
        </svg>
      </span>
    </template>
    <template v-else>
      <span class="reaction__icon--inactive">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" role="img"
             aria-labelledby="affb755br23xvyj00q73jc257v3pgoa0" class="crayons-icon reaction-icon not-reacted">
            <title id="affb755br23xvyj00q73jc257v3pgoa0">Like comment:</title>
            <path
                d="M18.884 12.595l.01.011L12 19.5l-6.894-6.894.01-.01A4.875 4.875 0 0112 5.73a4.875 4.875 0 016.884 6.865zM6.431 7.037a3.375 3.375 0 000 4.773L12 17.38l5.569-5.569a3.375 3.375 0 10-4.773-4.773L9.613 10.22l-1.06-1.062 2.371-2.372a3.375 3.375 0 00-4.492.25v.001z"></path>
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
    userVoteCount: {type: Number, required: false},
    verticalAlignment: {type: Boolean, required: false}
  },
  methods: {

    onVoteClick: function (postId, postType) {
      const postBody = {post_id: postId, post_type: postType};
      let url = `${window.location.origin}/${Api.vote}`;
      axios.post(url, postBody)
          .then(response => {
            console.log("Response:" + response);
            this.count = response.data.count;
            this.userVoteCount = response.data.userVoteCount;
          })
          .catch(error => {
            console.log("Error:" + error);
            alert('Join Stacktips to start earning reputation and unlocking new privileges like voting and bookmarking.')
          });
    },
  }
}
</script>