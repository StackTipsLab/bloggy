<template>
  <div class="container quizlet-form">
    <!-- Quiz Landing page -->
    <quiz-landing-component
        v-if="this.quizStatus === QuizState.UNDEFINED"
        :quiz="quiz"
        :quiz-state="this.quizStatus"/>

    <!-- Quiz Test page -->
    <div class="row --full-screen" v-if="this.quizStatus === QuizState.IN_PROGRESS">
      <div class="quizlet-form--container">
        <div class="quizlet-form--header">
          <div class="meta">
            <h1 class="display-2 text-capitalize fw-600 mb-4">{{ quiz.title }}</h1>
            <p class="text-muted">
              {{ quiz.questions_count }} Questions
              <span class="meta-seperator"></span>
              {{ quiz.duration }} Minutes
            </p>
          </div>

          <div class="d-flex justify-content-between align-items-center ">
            <p class="display-6 quiz-countdown-timer"
               v-bind:class="(timerCount <= 60000) ? ' text-danger ' : ' text-success'">
              {{ timeRemaining + 'm' }}
            </p>
            <p class="h3">
              Question: {{ currentIndex + 1 }} of {{ quiz.questions_count }}
            </p>
          </div>
        </div>
        <!-- Quiz questions container-->
        <div class="quizlet-form--card">
          <div class="mb-4">
            <h3 class="lead pb-2">{{ quiz.questions[currentIndex].title }}</h3>
            <input type="hidden" class="form-control" :value="quiz.questions[currentIndex].id">
            <template v-if="quiz.questions[currentIndex].description">
              <div class="description" v-html="quiz.questions[currentIndex].description">
              </div>
            </template>
          </div>

          <template v-for="(answerOption, answerIndex) in quiz.questions[currentIndex].answers">
            <template v-if="currentIndex + 1 <= quiz.questions.length">

              <!-- For single choice questions -->
              <!--              <question-kind-binary v-if="quiz.questions[currentIndex].type === QuestionType.BINARY "
                                                  :answer-option="answerOption"
                                                  :current-index="currentIndex"
                                                  :question-status="questionStatus"
                                                  :correctAnswer="quiz.questions[currentIndex].correctAnswer"/>-->
              <template v-if="quiz.questions[currentIndex].type === QuestionType.BINARY">
                <div class="form-check quizlet-form--label"
                     :class="[{ '--disabled': questionStatus === QuestionState.ANSWERED},
                { '--wrong-answer': questionStatus === QuestionState.ANSWERED && radioButtonAnswer === answerOption.key && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) },
                { '--correct-answer': questionStatus === QuestionState.ANSWERED && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) }
                ]">

                  <label class="form-check-label">
                    <input type="radio" class="form-check-input ml-0"
                           v-model="radioButtonAnswer"
                           @change="answerClicked()"
                           :disabled="questionStatus === QuestionState.ANSWERED"
                           :value="answerOption.key"/>
                    {{ answerOption.value }}
                  </label>

                  <div class="check-icon --danger"
                       v-if="questionStatus === QuestionState.ANSWERED && radioButtonAnswer === answerOption.key && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                         fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none"/>
                      <path
                          d="M15.73 3H8.27L3 8.27v7.46L8.27 21h7.46L21 15.73V8.27L15.73 3zM17 15.74L15.74 17 12 13.26 8.26 17 7 15.74 10.74 12 7 8.26 8.26 7 12 10.74 15.74 7 17 8.26 13.26 12 17 15.74z"/>
                    </svg>
                  </div>

                  <div class="check-icon --success"
                       v-if="questionStatus === QuestionState.ANSWERED && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                         fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none"/>
                      <path
                          d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                  </div>
                </div>
              </template>

              <!-- For multiple choice questions -->
              <!--              <question-kind-multiple v-if="quiz.questions[currentIndex].type === QuestionType.MULTIPLE"-->
              <!--                                      :answer-option="answerOption"-->
              <!--                                      :current-index="currentIndex"-->
              <!--                                      :question-status="questionStatus"-->
              <!--                                      :correctAnswer="quiz.questions[currentIndex].correctAnswer"/>-->
              <template v-if="quiz.questions[currentIndex].type === QuestionType.MULTIPLE">
                <div class="form-check quizlet-form--label" :class="[
                  { '--disabled': questionStatus === QuestionState.ANSWERED },
                  { '--wrong-answer': questionStatus === QuestionState.ANSWERED && checkboxAnswer.length && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) },
                  { '--correct-answer': questionStatus === QuestionState.ANSWERED && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) }
                ]">

                  <label class="form-check-label ">
                    <input type="checkbox" :id="answerOption.key" :disabled="questionStatus === QuestionState.ANSWERED"
                           @change="answerClicked" :value="answerOption.key" v-model="checkboxAnswer"
                           class="form-check-input ml-0">{{
                      answerOption.value
                    }}
                  </label>

                  <div class="check-icon --danger"
                       v-if="questionStatus === QuestionState.ANSWERED && checkboxAnswer.length && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                         fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none"/>
                      <path
                          d="M15.73 3H8.27L3 8.27v7.46L8.27 21h7.46L21 15.73V8.27L15.73 3zM17 15.74L15.74 17 12 13.26 8.26 17 7 15.74 10.74 12 7 8.26 8.26 7 12 10.74 15.74 7 17 8.26 13.26 12 17 15.74z"/>
                    </svg>
                  </div>

                  <div class="check-icon --success"
                       v-if="questionStatus === QuestionState.ANSWERED && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                         fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none"/>
                      <path
                          d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                  </div>

                </div>
              </template>


            </template>
          </template>
          <div class="explanation-banner"
               v-if="this.questionStatus === QuestionState.ANSWERED && quiz.questions[currentIndex].explanation">
            <div class="alert alert-info p-4">
              <h3 class="h4">Explanation</h3>
              <p class="mb-0">
                {{ quiz.questions[currentIndex].explanation }}
              </p>
            </div>
          </div>

          <!-- Bottom CTA container -->
          <div class="mt-4">
            <template v-if="this.questionStatus === QuestionState.UNANSWERED">
              <button @click.prevent="checkAnswer($event)" :disabled="this.nextButtonDisabled === true"
                      class="btn btn-lg btn-primary" :class="[{}]">Check your answer
              </button>
            </template>

            <template v-else-if="this.questionStatus === QuestionState.ANSWERED">
              <template v-if="this.currentIndex + 1 >= quiz.questions.length">
                <button @click.prevent="showResults()" class="btn btn-lg btn-primary"
                        id="quiz_show_results">Quiz Summary
                </button>
              </template>
              <template v-else>
                <button @click.prevent="nextQuestion($event)" class="btn btn-lg btn-primary">Next
                  question
                </button>
              </template>
            </template>

          </div>

        </div>
      </div>
    </div>

    <!-- Summary page -->
    <quiz-summary-page v-if="this.quizStatus === QuizState.COMPLETED"
                       :quiz="quiz"
                       :quiz-status="this.quizStatus"
                       :user-answers="this.userAnswers"/>
  </div>
</template>

<script>
import Api from '../Api.js'
import QuizLandingComponent from "./QuizLandingComponent.vue";
import QuizSummaryPage from "./QuizSummaryPage.vue";
import QuizState from "./QuizState";
import QuestionType from "./QuestionType";
import QuestionState from "./QuestionState";
import QuestionKindBinary from "./QuestionKindBinary.vue";
import QuestionKindMultiple from "./QuestionKindMultiple.vue";

export default {
  name: "quizlet",
  computed: {
    QuestionType() {
      return QuestionType
    },
    QuestionState() {
      return QuestionState
    },
    QuizState() {
      return QuizState
    }
  },
  components: {QuestionKindMultiple, QuestionKindBinary, QuizSummaryPage, QuizLandingComponent},
  props: {
    user: {
      type: Object,
      required: false,
    },
    quiz: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      radioButtonAnswer: '', //Answer Binary
      checkboxAnswer: [], //Answer Binary
      currentQuestionId: undefined,
      userAnswers: {},
      currentIndex: 0,
      quizStatus: QuizState.UNDEFINED,
      questionStatus: QuestionState.UNANSWERED,
      timerCount: undefined,
      timeRemaining: undefined,
      timer: undefined,
      nextButtonDisabled: true
    };
  },

  methods: {
    millisToMinutesAndSeconds: function (millis) {
      const date = new Date(Date.UTC(0, 0, 0, 0, 0, 0, millis)),
          parts = [
            // date.getUTCHours(),
            date.getUTCMinutes(),
            date.getUTCSeconds()
          ]
      return parts.map(s => String(s).padStart(2, '0')).join(':');
    },

    reStartQuiz() {
      this.trackGA4Event({
        'event': 'quiz_retake_event',
        'title': this.quiz.title,
        "slug": this.quiz.slug,
        "category": this.quiz.category.slug,
      })

      this.quizStatus = QuizState.UNDEFINED
      this.questionStatus = QuestionState.UNANSWERED
      this.currentQuestionId = 0
      this.nextButtonDisabled = true
      this.radioButtonAnswer = ''
      this.checkboxAnswer = []
      this.userAnswers = {}
      this.currentIndex = 0
      this.timerCount = undefined
      this.timer = undefined
      this.timeRemaining = undefined
    },

    startQuiz() {
      this.quizStatus = QuizState.IN_PROGRESS;
      if (!this.timer) {

        // Set default timer count and time remaining
        this.timerCount = this.quiz.duration * 1000 * 60;
        this.timeRemaining = this.millisToMinutesAndSeconds(this.timerCount);

        this.timer = setInterval(() => {
          if (this.timer) {
            if (this.timerCount > 0) {
              this.timerCount -= 1000;
              this.timeRemaining = this.millisToMinutesAndSeconds(this.timerCount);
            } else {
              clearInterval(this.timer);
              this.showResults();
            }
          }
        }, 1000);
      }

      this.trackGA4Event({
        'event': 'quiz_start_event',
        'title': this.quiz.title,
        "slug": this.quiz.slug,
        "category": this.quiz.category.slug,
      });
    },

    trackGA4Event(event) {
      if (typeof dataLayer !== "undefined") {
        dataLayer.push(event);
      }
    },

    showResults() {
      this.quizStatus = QuizState.COMPLETED;
      this.trackGA4Event({
        'event': 'quiz_completed_event',
        'title': this.quiz.title,
        "slug": this.quiz.slug,
        "status": this.quizStatus,
        "category": this.quiz.category.slug,
      })
      this.saveAnswer();
      // this.saveUserResults()

      // this.timer.stop()
      // this.timer = null;
      // this.timerCount = null;
    },

    saveUserResults() {
      const postBody = {quiz_id: this.quiz.id, score: this.computeScore.percentage};
      let url = `${window.location.origin}/${Api.saveQuizScore}`;
      axios.post(url, postBody)
          .then(response => {
            // console.log("Response:" + response);
          })
          .catch(error => {
            console.log("Error:" + error);
            alert('Sign in to start earning reputation and unlocking new privileges like voting and bookmarking.')
          });
    },

    saveAnswer() {
      const currentQuestion = this.quiz.questions[this.currentIndex];
      const keyname = currentQuestion.id.toString();
      if (currentQuestion.type === QuestionType.BINARY) {
        this.userAnswers[keyname] = [this.radioButtonAnswer];
      } else if (currentQuestion.type === QuestionType.MULTIPLE) {
        this.userAnswers[keyname] = this.checkboxAnswer;
      }
    },

    isCorrectAnswer(answerKey) {
      if (this.questionStatus === QuestionState.ANSWERED && this.quiz.questions[this.currentIndex].correctAnswer.find(answerKey)) {
        console.log("Answer is correct!")
        return true
      }
      return false;
    },

    nextQuestion(e) {
      this.saveAnswer();
      this.radioButtonAnswer = ''
      this.checkboxAnswer = []
      this.currentIndex++;
      this.questionStatus = QuestionState.UNANSWERED
      this.nextButtonDisabled = true
    },

    checkAnswer(e) {
      this.saveAnswer();
      // this.radioButtonAnswer = ''
      // this.checkboxAnswer = []
      this.questionStatus = QuestionState.ANSWERED
    },

    answerClicked(e) {
      this.nextButtonDisabled = false
    },
  }
}
</script>