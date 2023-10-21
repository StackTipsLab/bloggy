<template>
  <form class="w-100 comment-area" :style="commentStyle" ref="commentForm">
    <div class="form-floating">
      <input type="hidden" id="postId" name="postId" v-model="postId">
      <input type="hidden" id="parent" name="parent" v-model="parent">
      <textarea class="form-control comment-text-box" placeholder="Leave a comment here" v-model="message"/>
      <template v-if="placeholderText">
        <label for="floatingTextarea2" class="text-muted text-sm">Reply to {{
            placeholderText
          }}</label>
      </template>
      <template v-else>
        <label for="floatingTextarea2" class="text-muted text-sm">Add to the discussion</label>
      </template>
    </div>
    <div class="d-flex justify-content-end">
      <button class="btn btn-primary btn-sm mt-3" type="submit" @click.prevent="submitComment()">Post comment</button>
    </div>
  </form>
</template>
<script>
export default {
  data() {
    return {
      message: '',
    }
  },
  props: ['comment', 'commentStyle', "postId", 'parent', 'placeholderText', 'addCommentEvent' ],
  methods: {
    submitComment: function () {
      console.log(`AddComment:: {"postId":"${this.postId}", "parent":"${this.parent}", "message":"${this.message}"}`);
      this.addCommentEvent(this.postId, this.parent, this.message)

      // if ((typeof (parent) !== "undefined") || (parent !== null)) {
      //   this.$emit('hideCommentFormEvent') //TODO emit not working now
      // }
      this.message = ''; //Clear message after submit
    }
  }
}
</script>