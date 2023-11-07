<template>
  <div class="row bg-light p-4">
    <div class="hero">
      <div v-show="computeScore.percentage >= 70" class="text-green">
        <h2 class="display-4 fw-normal">Great job!🎉🎉🎉. You're making excellent progress!</h2>
        <p class="my-3 lead">You've just completed the <strong>{{ quiz['title'] }}</strong>, and you've achieved an
          impressive
          score of {{ computeScore.percentage + '%' }}!</p>
        <p class="my-3 lead">✅ You answered {{ computeScore.correctAnswersCount }} out of {{
            computeScore.totalQuestions
          }} questions
          correctly. </p>
        <p class="lead">Way to go! You're clearly mastering the concepts and skills required in
          {{ quiz.category.title }}. Keep up
          the fantastic work, and continue your learning journey!</p>
        <p class="lead">Remember, practice makes perfect. Feel free to explore more quizzes and resources to further
          enhance your
          knowledge. You're on the right path to achieving your goals!</p>
      </div>

      <div v-show="computeScore.percentage < 70 && computeScore.percentage >= 50" class="text-amber">
        <h2 class="display-4 fw-normal">Congratulations!! on completing the {{ quiz.title }}!</h2>
        <p class="my-3 lead">✅ You answered {{ computeScore.correctAnswersCount }} out of {{
            computeScore.totalQuestions
          }} questions correctly. Your score is {{ computeScore.percentage + '%' }}</p>
        <p class="my-3 lead">We knew it wasn't easy to get all the answers right. But, you're making progress, and every
          correct answer
          brings you closer to your goal.</p>
        <p class="my-3 lead">Remember, learning is a continuous process, and it's okay to face challenges along the
          way.</p>
      </div>
      <div v-show="computeScore.percentage < 50">
        <h2 class="display-4 fw-normal">Keep going, and don't be discouraged!</h2>
        <p class="my-3 lead">Completing the <strong>{{ quiz.title }}</strong> is a commendable effort, regardless of the
          score. You can retake this quiz again. </p>
        <p class="my-3 lead">❌ You answered {{ computeScore.correctAnswersCount }} out of
          {{ computeScore.totalQuestions }} questions correctly. Your score is {{ computeScore.percentage + '%' }}</p>
        <p class="my-3 lead">You've got this! Keep learning, keep practicing, and you'll undoubtedly see improvement.
          Best of luck!
        </p>
      </div>
      <button @click.prevent="reStartQuiz()" class="btn btn-lg btn-primary mt-3 px-5">Retake Quiz</button>

<!--      <div class="my-5">
        <p class="text-capitalize text-muted">Share your Quiz Success with Friends!</p>
        <div class="d-grid gap-2 d-md-block my-4 d-print-none">
          <div class="social-share-button facebook-this">
            <a href="#" target="_blank">Facebook</a>
          </div>
          <div class="social-share-button tweet-this">
            <a href="#" class="meta-act-link meta-tweet" target="_blank">Tweet</a>
          </div>
          <div class="social-share-button copy-this">
            <button data-copy-btn="buttonCopy" data-copy-url="#" class="#">Copy</button>
          </div>
        </div>
      </div>-->
    </div>
  </div>
</template>
<script>
import QuizState from "./QuizState";

export default {
  name: 'quiz-summary-page',
  props: {
    quizStatus: {
      type: String
    },
    quiz: {
      type: Object,
      required: false
    },
    userAnswers: {
      type: Object,
      required: false
    },
  },

  computed: {
    quizState() {
      return QuizState
    },
    computeScore() {
      if (this.quizStatus === QuizState.COMPLETED) {
        let correctAnswersCount = 0;
        let inCorrectAnswersCount = 0;
        const totalQuestions = this.quiz.questions.length;

        for (let i = 0; i < totalQuestions; i++) {
          const question = this.quiz.questions[i];
          const userAnswer = this.userAnswers[question.id];

          if (this.arraysEqual(userAnswer, question.correctAnswer)) {
            correctAnswersCount++
          } else {
            inCorrectAnswersCount++
          }
        }

        return {
          "correctAnswersCount": correctAnswersCount,
          "inCorrectAnswersCount": inCorrectAnswersCount,
          "percentage": Math.ceil((correctAnswersCount / totalQuestions) * 100),
          "totalQuestions": totalQuestions
        }
      }
      return {}
    }
  },

  methods: {
    reStartQuiz() {
      this.$parent.reStartQuiz();
    },

    arraysEqual(a, b) {
      if (a === b) return true;
      if (a == null || b == null) return false;
      if (a.length !== b.length) return false;
      a.sort();
      b.sort();
      // If you don't care about the order of the elements inside
      // the array, you should sort both arrays here.
      // Please note that calling sort on an array will modify that array.
      // you might want to clone your array first.

      for (let i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
      }
      return true;
    }
  }
}
</script>