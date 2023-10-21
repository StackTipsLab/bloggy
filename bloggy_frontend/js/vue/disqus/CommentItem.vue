<template>
  <div id="comment-row" :style="commentStyle" :data-id="comment.id">
    <div class="d-flex flex-row">

      <div class="comment-author-tooltip">

        <!-- Show user profile image if registered, else show gravtar -->
        <template v-if="comment.user && comment.user.profile_photo">
          <img :src="comment.user.profile_photo" width="36" height="36" style="margin-right: 0.5rem" class="rounded-circle" />
        </template>
        <template v-else-if="comment.comment_author_email">
          <img :src="getGravatar(comment.comment_author_email, 80)" width="36" height="36" style="margin-right: 0.5rem" class="rounded-circle" />
        </template>
        <template v-else>
            <img src="/static/media/default_avatar.png" width="36" height="36" style="margin-right: 0.5rem" class="rounded-circle" />
        </template>

        <template v-if="comment.user">
          <span class="tooltip-content">
            <a :href="'/user/' + comment.user.username" class="text-decoration-none text-dark fw-semibold">{{
                comment.user.name
              }}</a>
            <p>
              <small class="text-muted">{{ comment.user.bio }}</small>
              <br>
              <small class="text-muted">{{ comment.user.location }}</small>
            </p>
          </span>
        </template>

      </div>

      <div class="d-block w-100">
        <div class="comment-message">


          <template v-if="comment.user">
            <template v-if="this.currentUser!= null && this.currentUser.username == comment.user.username  && comment.reply_set.length <= 0">
              <button class="delete-comment-action-button" type="submit" @click.prevent="onDeleteComment(comment.id, comment.parent)">DELET</button>
            </template>
          </template>

          <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex flex-row align-items-center">
              <template v-if="comment.user">
                <a :href="'/user/' + comment.user.username" class="text-decoration-none text-dark fw-semibold">{{ comment.user.name }}</a>
                <small class="text-muted">&nbsp;-&nbsp;{{ getFormattedDate(comment.comment_date) }}</small>
              </template>
              <template v-else>
                <a target="_blank" :href="comment.comment_author_url" class="text-decoration-none text-dark fw-semibold text-capitalize">
                  {{ comment.comment_author_name }}
                </a>
<!--                  <span class="mx-2 badge rounded-pill bg-info">Unregistered</span>-->
                  <small class="text-muted">&nbsp;-&nbsp;{{ getFormattedDate(comment.comment_date) }}</small>
              </template>

            </div>
          </div>

          <p class="user-comment-text text-justify">{{ comment.comment_content }}</p>

          <div class="comment-reply-button" v-show="!hideReply">
            <small class="fs-13" @click="showCommentsForm = !showCommentsForm" style="color:#6c757d;">
                <span style="height: 16px;width: 16px;fill: #6c757d;">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" role="img" aria-labelledby="akzyi6xyrwck0c1guyizkuu7pw2rza9e" class="crayons-icon reaction-icon not-reacted"><title id="akzyi6xyrwck0c1guyizkuu7pw2rza9e">Comment button</title><path d="M10.5 5h3a6 6 0 110 12v2.625c-3.75-1.5-9-3.75-9-8.625a6 6 0 016-6zM12 15.5h1.5a4.501 4.501 0 001.722-8.657A4.5 4.5 0 0013.5 6.5h-3A4.5 4.5 0 006 11c0 2.707 1.846 4.475 6 6.36V15.5z"></path></svg>
                </span>REPLY
            </small>
          </div>
        </div>

        <transition name="slide-fade">
          <comment-form v-show="showCommentsForm"
                        :post-id="postId"
                        :parent="comment.id"
                        :placeholder-text="comment.comment_author_name"
                        :add-comment-event="addCommentEvent"
                        v-on:hide-comment-form-event="hideCommentFormEvent"
                        comment-style="margin-top:0.5rem"></comment-form>
        </transition>
      </div>
    </div>

  </div>
</template>
<script>
import CommentForm from './CommentForm.vue';
import moment from 'moment'

// MD5 (Message-Digest Algorithm) by WebToolkit
const MD5=function(s){function L(k,d){return(k<<d)|(k>>>(32-d))}function K(G,k){var I,d,F,H,x;F=(G&2147483648);H=(k&2147483648);I=(G&1073741824);d=(k&1073741824);x=(G&1073741823)+(k&1073741823);if(I&d){return(x^2147483648^F^H)}if(I|d){if(x&1073741824){return(x^3221225472^F^H)}else{return(x^1073741824^F^H)}}else{return(x^F^H)}}function r(d,F,k){return(d&F)|((~d)&k)}function q(d,F,k){return(d&k)|(F&(~k))}function p(d,F,k){return(d^F^k)}function n(d,F,k){return(F^(d|(~k)))}function u(G,F,aa,Z,k,H,I){G=K(G,K(K(r(F,aa,Z),k),I));return K(L(G,H),F)}function f(G,F,aa,Z,k,H,I){G=K(G,K(K(q(F,aa,Z),k),I));return K(L(G,H),F)}function D(G,F,aa,Z,k,H,I){G=K(G,K(K(p(F,aa,Z),k),I));return K(L(G,H),F)}function t(G,F,aa,Z,k,H,I){G=K(G,K(K(n(F,aa,Z),k),I));return K(L(G,H),F)}function e(G){var Z;var F=G.length;var x=F+8;var k=(x-(x%64))/64;var I=(k+1)*16;var aa=Array(I-1);var d=0;var H=0;while(H<F){Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=(aa[Z]|(G.charCodeAt(H)<<d));H++}Z=(H-(H%4))/4;d=(H%4)*8;aa[Z]=aa[Z]|(128<<d);aa[I-2]=F<<3;aa[I-1]=F>>>29;return aa}function B(x){var k="",F="",G,d;for(d=0;d<=3;d++){G=(x>>>(d*8))&255;F="0"+G.toString(16);k=k+F.substr(F.length-2,2)}return k}function J(k){k=k.replace(/rn/g,"n");var d="";for(var F=0;F<k.length;F++){var x=k.charCodeAt(F);if(x<128){d+=String.fromCharCode(x)}else{if((x>127)&&(x<2048)){d+=String.fromCharCode((x>>6)|192);d+=String.fromCharCode((x&63)|128)}else{d+=String.fromCharCode((x>>12)|224);d+=String.fromCharCode(((x>>6)&63)|128);d+=String.fromCharCode((x&63)|128)}}}return d}var C=Array();var P,h,E,v,g,Y,X,W,V;var S=7,Q=12,N=17,M=22;var A=5,z=9,y=14,w=20;var o=4,m=11,l=16,j=23;var U=6,T=10,R=15,O=21;s=J(s);C=e(s);Y=1732584193;X=4023233417;W=2562383102;V=271733878;for(P=0;P<C.length;P+=16){h=Y;E=X;v=W;g=V;Y=u(Y,X,W,V,C[P+0],S,3614090360);V=u(V,Y,X,W,C[P+1],Q,3905402710);W=u(W,V,Y,X,C[P+2],N,606105819);X=u(X,W,V,Y,C[P+3],M,3250441966);Y=u(Y,X,W,V,C[P+4],S,4118548399);V=u(V,Y,X,W,C[P+5],Q,1200080426);W=u(W,V,Y,X,C[P+6],N,2821735955);X=u(X,W,V,Y,C[P+7],M,4249261313);Y=u(Y,X,W,V,C[P+8],S,1770035416);V=u(V,Y,X,W,C[P+9],Q,2336552879);W=u(W,V,Y,X,C[P+10],N,4294925233);X=u(X,W,V,Y,C[P+11],M,2304563134);Y=u(Y,X,W,V,C[P+12],S,1804603682);V=u(V,Y,X,W,C[P+13],Q,4254626195);W=u(W,V,Y,X,C[P+14],N,2792965006);X=u(X,W,V,Y,C[P+15],M,1236535329);Y=f(Y,X,W,V,C[P+1],A,4129170786);V=f(V,Y,X,W,C[P+6],z,3225465664);W=f(W,V,Y,X,C[P+11],y,643717713);X=f(X,W,V,Y,C[P+0],w,3921069994);Y=f(Y,X,W,V,C[P+5],A,3593408605);V=f(V,Y,X,W,C[P+10],z,38016083);W=f(W,V,Y,X,C[P+15],y,3634488961);X=f(X,W,V,Y,C[P+4],w,3889429448);Y=f(Y,X,W,V,C[P+9],A,568446438);V=f(V,Y,X,W,C[P+14],z,3275163606);W=f(W,V,Y,X,C[P+3],y,4107603335);X=f(X,W,V,Y,C[P+8],w,1163531501);Y=f(Y,X,W,V,C[P+13],A,2850285829);V=f(V,Y,X,W,C[P+2],z,4243563512);W=f(W,V,Y,X,C[P+7],y,1735328473);X=f(X,W,V,Y,C[P+12],w,2368359562);Y=D(Y,X,W,V,C[P+5],o,4294588738);V=D(V,Y,X,W,C[P+8],m,2272392833);W=D(W,V,Y,X,C[P+11],l,1839030562);X=D(X,W,V,Y,C[P+14],j,4259657740);Y=D(Y,X,W,V,C[P+1],o,2763975236);V=D(V,Y,X,W,C[P+4],m,1272893353);W=D(W,V,Y,X,C[P+7],l,4139469664);X=D(X,W,V,Y,C[P+10],j,3200236656);Y=D(Y,X,W,V,C[P+13],o,681279174);V=D(V,Y,X,W,C[P+0],m,3936430074);W=D(W,V,Y,X,C[P+3],l,3572445317);X=D(X,W,V,Y,C[P+6],j,76029189);Y=D(Y,X,W,V,C[P+9],o,3654602809);V=D(V,Y,X,W,C[P+12],m,3873151461);W=D(W,V,Y,X,C[P+15],l,530742520);X=D(X,W,V,Y,C[P+2],j,3299628645);Y=t(Y,X,W,V,C[P+0],U,4096336452);V=t(V,Y,X,W,C[P+7],T,1126891415);W=t(W,V,Y,X,C[P+14],R,2878612391);X=t(X,W,V,Y,C[P+5],O,4237533241);Y=t(Y,X,W,V,C[P+12],U,1700485571);V=t(V,Y,X,W,C[P+3],T,2399980690);W=t(W,V,Y,X,C[P+10],R,4293915773);X=t(X,W,V,Y,C[P+1],O,2240044497);Y=t(Y,X,W,V,C[P+8],U,1873313359);V=t(V,Y,X,W,C[P+15],T,4264355552);W=t(W,V,Y,X,C[P+6],R,2734768916);X=t(X,W,V,Y,C[P+13],O,1309151649);Y=t(Y,X,W,V,C[P+4],U,4149444226);V=t(V,Y,X,W,C[P+11],T,3174756917);W=t(W,V,Y,X,C[P+2],R,718787259);X=t(X,W,V,Y,C[P+9],O,3951481745);Y=K(Y,h);X=K(X,E);W=K(W,v);V=K(V,g)}var i=B(Y)+B(X)+B(W)+B(V);return i.toLowerCase()};
const default_image = "https://stacktips.sgp1.digitaloceanspaces.com/media/uploads/default_avatar.png"

export default {
  components: {
    'comment-form': CommentForm,
  },
  props: ['comment', 'postId', 'hideReply', 'commentStyle', 'parentCommentUser', 'deleteCommentEvent', 'addCommentEvent', 'currentUser'],
  data: function () {
    return {
      showCommentsForm: false
    }
  },

  methods: {
    getGravatar: function (email, size) {
      email = typeof email !== 'undefined' ? email : 'john.doe@example.com';
      var allowed_rating = typeof allowed_rating !== 'undefined' ? allowed_rating : 'g';
      var force_default = 'n';

      return ("https://secure.gravatar.com/avatar/" + MD5(email.toLowerCase().trim()) + "?size=" + size + "&default=" + encodeURIComponent(default_image) + "&rating=" + allowed_rating + (force_default === 'y' ? "&forcedefault=" + force_default : ''));
    },

    hideCommentFormEvent: function () {
      console.log("hideCommentFormEvent");
      this.showCommentsForm = true;
    },

    onDeleteComment: function (commentId, parentId) {
      console.log("DeleteComment:" + commentId + " Parent:" + parentId);
      this.deleteCommentEvent(commentId, parentId);
    },
    onReplyClick: function (cid) {
      console.log("Reply clicked", cid);
      // this.$refs.childs[0].hidden = false;
    },

    getFormattedDate(date) {
      const formattedDate = moment('19 Oct 2017').format('DD MMM, YYYY')
      return formattedDate;
    }
  }
}
</script>