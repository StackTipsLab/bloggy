<template>
  <div class="row justify-content-center">
    <div class="hero">
      <h1 class="display-2 text-capitalize fw-600 mb-4">{{ quiz.title }}</h1>
      <p class="text-muted">Interactive Quiz<span class="meta-seperator"></span>{{ quiz.questions_count }}
        Questions<span class="meta-seperator"></span>{{ quiz.duration }} Minutes</p>
      <article class="quiz-description" v-html="quiz.content"></article>
      <button @click.prevent="startQuiz" class="btn btn-lg btn-primary mt-3 px-4" id="quiz_start_cta_click">Start Quiz
      </button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'quiz-landing-component',
  props: {
    quizState: {
      type: String
    },
    quiz: {
      type: Object,
      required: true,
    },
  },
  methods: {
    startQuiz() {
      this.$parent.startQuiz()
    }
  }
}
</script>