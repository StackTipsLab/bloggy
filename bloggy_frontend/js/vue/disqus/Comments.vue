<template>
  <div id="threaded-comments">
    <h3 class="h3 mb-2">
      <template v-if="commentsList.length> 0">{{ commentsList.length }} Comments</template>
      <template v-else>Discussions</template>
    </h3>

    <div class=" mt-3">
      <div class="d-flex flex-row comment-box-main">
        <template v-if="this.currentUser === 'AnonymousUser'">
          <div class="comments-login-notice">
            <p>Login with your existing account or create an account to join the discussion. We welcome relevant,
              respectful comments.</p>
            <a :href="'/login?next=' + this.currentUrl" class="btn btn-primary">Login or Create an account</a>
          </div>
        </template>

        <template v-else>
          <div class="comment-author-tooltip">
            <template v-if="null!= this.user && this.user.profile_photo">
              <img :src="this.user.profile_photo" width="32" height="32" style="margin-right: 0.5rem"
                   class="rounded-circle">
            </template>
            <template v-else>
              <img src="https://media.stacktips.com/static/media/default_avatar.png" width="32" height="32" style="margin-right: 0.5rem"
                   class="rounded-circle">
            </template>
          </div>
          <comment-form :add-comment-event="addComment" :post-id="postId"></comment-form>
        </template>
      </div>

      <div class="comment-thread">
        <div :data-cid="comment.id" v-for="(comment, index) in commentsList" class="mt-3">
          <template v-if="comment.parent == null">
            <comment-item :comment="comment" :index="index"
                          :post-id="postId"
                          :add-comment-event="addComment"
                          :delete-comment-event="deleteComment"
                          :current-user="user"
                          v-bind:key="comment.id"></comment-item>
          </template>

          <template v-if="comment.reply_set">
            <comment-item :comment="reply"
                          v-for="reply in comment.reply_set"
                          :parent-comment-user="comment.user_name"
                          :key="reply.id"
                          :post-id="postId"
                          :hide-reply="true"
                          :current-user="user"
                          :add-comment-event="addComment"
                          :delete-comment-event="deleteComment"
                          comment-style="padding-left:45px;margin-top:8px"></comment-item>

          </template>
        </div>
      </div>

    </div>
  </div>
</template>
<script>
import Api from '../Api.js'

import CommentItem from './CommentItem.vue';
import CommentForm from './CommentForm.vue';

export default {
  components: {
    'comment-item': CommentItem,
    'comment-form': CommentForm,
  },
  props: {
    currentUser: {
      type: String,
      required: false,
    },
    postId: {
      type: String,
      required: true,
    },
    postType: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      currentUrl: "",
      commentsList: [],
      user: null,
    };
  },

  created() {

    this.currentUrl = window.location.pathname;
    this.loadComments();
    this.loadCurrentUserDetails();


  },
  methods: {
    addComment: function (postId, parent, text) {

      const postBody = {postId: postId, parent: parent, comment: text};
      console.log("Comments:: posting comment to server: " + JSON.stringify(postBody));
      let url = `${window.location.origin}/${Api.comments}`;

      axios.post(url, postBody)
          .then(response => {
            console.log("Response:" + response);

            if ((typeof (parent) === "undefined")) {
              this.commentsList.unshift(response.data);
            } else {
              const replySet = this.commentsList.find(f => f.id === parent).reply_set;
              replySet.unshift(response.data);
            }
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },

    deleteComment: function (commentId, parentId) {
      let url = `${window.location.origin}/${Api.comments}/${commentId}`;
      axios.delete(url)
          .then(response => {
            console.log("Response:" + response);

            if (parentId == null) {
              const indexOfObject = this.commentsList.findIndex(object => {
                return object.id === commentId;
              });

              this.commentsList.splice(indexOfObject, 1);
            } else {
              const replySet = this.commentsList.find(f => f.id === parentId).reply_set;
              const indexOfObject = replySet.findIndex(object => {
                return object.id === commentId;
              });
              replySet.splice(indexOfObject, 1);
            }
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },


    loadComments: function () {
      let url = `${window.location.origin}/${Api.comments}/${this.postId}`;
      axios.get(url).then(response => {
        console.log("Response:" + response);
        this.commentsList = response.data;
      });
    },

    loadCurrentUserDetails: function () {
      if (null != this.currentUser && this.currentUser != 'AnonymousUser') {
        let url = `${window.location.origin}/${Api.users}/${this.currentUser}`;
        axios.get(url).then(response => {
          console.log("Response:" + response);
          this.user = response.data[0];
        });
      }
    }

  },

}
</script>