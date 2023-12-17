<template>
  <div class="container quizlet-form">

    <!-- Quiz Landing page -->
    <div class="row justify-content-center" v-show="this.quizState == undefined">
      <div class="hero col-md-8 jumbotron p-3 p-lg-5 text-centerd">
        <h1 class="display-2 fw-normal">{{ quiz.title }}</h1>
        <p class="lead text-muted">
          Interactive Quiz
          <span class="meta-seperator"></span>
          {{ quiz.questions_count }} Questions
          <span class="meta-seperator"></span>
          {{ quiz.duration }} Minutes
        </p>


        <p class="leadd">
          {{ quiz.description }} Good luck!
        </p>

        <div class="row">
          <div class="col-md-12">
            <h3>Instructions:</h3>
            <ul>
              <li>Total number of questions: {{ quiz.questions_count }}</li>
              <li>Time allotted: {{ quiz.duration }} minutes</li>
              <li>Each question carry 1 mark, no negative marks.</li>
            </ul>
          </div>
          <div class="col-md-12">
            <h3>Note:</h3>
            <ul>
              <li>Click the 'Submit Test' button given in the bottom of this page to Submit your answers.</li>
              <li>Test will be submitted automatically if the time expired</li>
              <li>Do not refresh the page while taking the test.</li>
            </ul>

          </div>
        </div>

        <div v-show="this.quizState == undefined">
          <button @click.prevent="startQuiz()" class="btn btn-lg btn-primary mt-3 px-5">Start Quiz</button>
        </div>
      </div>
    </div>

    <!-- Quiz Test page -->
    <div class="row justify-content-center --full-screen" v-show="this.quizState === 'inprogress'">
      <div class="col-lg-10 col-md-10 col-sm-12 quizlet-form--container">
        <div class="d-flex justify-content-between align-items-center quizlet-form--header">
          <div class="meta">
            <h1 class="h1 mb-1 mr-3">{{ quiz.title }}</h1>
            <p class="lead text-muted">
              {{ quiz.questions_count }} Questions
              <span class="meta-seperator"></span>
              {{ quiz.duration }} Minutes
            </p>
          </div>

          <p class="display-6 quiz-countdown-timer"
            v-bind:class="(timerCount <= 60000) ? ' text-danger ' : ' text-success'">
            {{ timeRemaining + 'm' }}
          </p>
        </div>


        <!-- Quiz questions container-->
        <div class="quizlet-form--card">
          <div class="mb-4">
            <h3 class="lead fw-bolder pb-2">{{ currentIndex+1 }}: {{ quiz.questions[currentIndex].title }}</h3>
            <input type="hidden" class="form-control" :value="quiz.questions[currentIndex].id">

            <template v-if="quiz.questions[currentIndex].description">
              <div class="description" v-html="quiz.questions[currentIndex].description">
              </div>
            </template>
          </div>

          <template v-for="(answerOption, answerIndex) in quiz.questions[currentIndex].answers">
            <template v-if="currentIndex + 1 <= quiz.questions.length">

              <!-- For single choice questions -->
              <template v-if="quiz.questions[currentIndex].type === 'binary'">
                <div class="form-check quizlet-form--label" :class="[{ '--disabled': questionState === 'answered' },
                { '--wrong-answer': questionState === 'answered' && radioButtonAnswer === answerOption.key && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) },
                { '--correct-answer': questionState === 'answered' && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) }
                ]">

                  <label class="form-check-label">
                    <input type="radio" class="form-check-input ml-0" v-model="radioButtonAnswer"
                      @change="answerClicked($event)" :disabled="questionState === 'answered'"
                      :value="answerOption.key">{{ answerOption.value }}
                  </label>


                  <div class="check-icon --danger"
                    v-if="questionState === 'answered' && radioButtonAnswer === answerOption.key && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                      fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none" />
                      <path
                        d="M15.73 3H8.27L3 8.27v7.46L8.27 21h7.46L21 15.73V8.27L15.73 3zM17 15.74L15.74 17 12 13.26 8.26 17 7 15.74 10.74 12 7 8.26 8.26 7 12 10.74 15.74 7 17 8.26 13.26 12 17 15.74z" />
                    </svg>
                  </div>

                  <div class="check-icon --success"
                    v-if="questionState === 'answered' && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                      fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none" />
                      <path
                        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                  </div>

                </div>
              </template>

              <!-- For multiple choice questions -->
              <template v-if="quiz.questions[currentIndex].type === 'multiple'">
                <div class="form-check quizlet-form--label" :class="[
                  { '--disabled': questionState === 'answered' },
                  { '--wrong-answer': questionState === 'answered' && checkboxAnswer.includes(answerOption.key) && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) },
                  { '--correct-answer': questionState === 'answered' && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key) }
                ]">

                  <label class="form-check-label ">
                    <input type="checkbox" :id="answerOption.key" :disabled="questionState === 'answered'"
                      @change="answerClicked($event)" :value="answerOption.key" v-model="checkboxAnswer"
                      class="form-check-input ml-0">{{
                    answerOption.value
                    }}
                  </label>

                  <div class="check-icon --danger"
                    v-if="questionState === 'answered' && checkboxAnswer.includes(answerOption.key) && !quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                      fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none" />
                      <path
                        d="M15.73 3H8.27L3 8.27v7.46L8.27 21h7.46L21 15.73V8.27L15.73 3zM17 15.74L15.74 17 12 13.26 8.26 17 7 15.74 10.74 12 7 8.26 8.26 7 12 10.74 15.74 7 17 8.26 13.26 12 17 15.74z" />
                    </svg>
                  </div>

                  <div class="check-icon --success"
                    v-if="questionState === 'answered' && quiz.questions[currentIndex].correctAnswer.includes(answerOption.key)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
                      fill="#000000">
                      <path d="M0 0h24v24H0z" fill="none" />
                      <path
                        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                  </div>

                </div>
              </template>


            </template>
          </template>


          <div class="explanation-banner"
            v-if="this.questionState === 'answered' && quiz.questions[currentIndex].explanation">
            <p class="mb-0"><span class="h5">Explanation:</span>
              {{ quiz.questions[currentIndex].explanation }}
            </p>
          </div>

          <!-- Bottom CTA container -->
          <div class="mt-4">
            <template v-if="this.questionState === 'unanswered'">
              <button @click.prevent="checkAnswer($event)" :disabled="this.nextButtonDisabled == true"
                class="btn btn-lg btn-primary" style="width: 30%;" :class="[{}]">Check Your
                Answer
                <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24">
                  <path d="M9.4 18 8 16.6l4.6-4.6L8 7.4 9.4 6l6 6Z" />
                </svg>
              </button>
            </template>

            <template v-else-if="this.questionState === 'answered'">
              <template v-if="this.currentIndex + 1 >= quiz.questions.length">
                <button @click.prevent="showResults()" class="btn btn-lg btn-primary" style="width: 30%;">Show Quiz
                  Summary
                  <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24">
                    <path
                      d="m6.7 18-5.65-5.65 1.425-1.4 4.25 4.25 1.4 1.4Zm5.65 0L6.7 12.35l1.4-1.425 4.25 4.25 9.2-9.2 1.4 1.425Zm0-5.65-1.425-1.4L15.875 6 17.3 7.4Z" />
                  </svg>
                </button>
              </template>
              <template v-else>
                <button @click.prevent="nextQuestion($event)" class="btn btn-lg btn-primary" style="width: 30%;">Next
                  Question
                  <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24">
                    <path d="M9.4 18 8 16.6l4.6-4.6L8 7.4 9.4 6l6 6Z" />
                  </svg>
                </button>
              </template>

            </template>

          </div>

        </div>
      </div>
    </div>

    <!-- Summary page -->
    <div class="row justify-content-center text-center" v-show="this.quizState === 'completed'">
      <div class="hero col-md-8 jumbotron pt-5 text-center">

        <div class="test-result" :class="[
          { '--danger': computeScore.percentage <= 70 },
          { '--success': computeScore.percentage > 70 },
        ]">{{ computeScore.correctAnswersCount }}/{{ computeScore.totalQuestions }}</div>

        <h1 class="display-1 mt-3">Result Summary</h1>
        <h3 class="h1 mb-0">You've scored
          <span :class="[
            { 'text-danger': computeScore.percentage <= 70 },
            { 'text-success': computeScore.percentage > 70 },
          ]">{{ computeScore.percentage + '%' }}</span>
        </h3>

        <p class="lead my-3"
          :class="[{ 'text-danger': computeScore.percentage <= 70 },{ 'text-success': computeScore.percentage > 70 }]"
          v-show="computeScore.percentage > 70">You've completed {{ quiz['title'] }} test with {{
          computeScore.correctAnswersCount }} correct {{
          computeScore.correctAnswersCount > 0 ? 'answers' : 'answer'
          }} out of
          {{ computeScore.totalQuestions }}
          questions.
        </p>

        <p class="lead text-dangers my-3" v-show="computeScore.percentage <= 70">Oh, we're sorry! We knew it wasn't easy
          to
          get
          all the answers right. You can
          Quiz again.</p>
        <div v-show="this.quizState == 'completed'">
          <button @click.prevent="reStartQuiz()" class="btn btn-lg btn-primary mt-3 px-5">Retake Quiz</button>
        </div>

      </div>

    </div>

  </div>

</template>

<script>
import Api from './Api.js'

export default {
  name: "quizlet",
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
      quizState: undefined, // underfined, inprogress, completed
      questionState: "unanswered", // unanswered, answered
      timerCount: undefined,
      timeRemaining: undefined,
      timer: undefined,
      nextButtonDisabled : true
    };
  },

  computed: {
    computeScore() {
      if (this.quizState == 'completed') {
        let correctAnswersCount = 0;
        let inCorrectAnswersCount = 0;
        const totalQuestions = this.quiz.questions.length;

        for (var i = 0; i < totalQuestions; i++) {
          var question = this.quiz.questions[i];
          var userAnswer = this.userAnswers[question.id];

          if (this.arraysEqual(userAnswer, question.correctAnswer)) {
            correctAnswersCount++
          } else {
            inCorrectAnswersCount++
          }
          console.log("Question", question);
          console.log("User answer", userAnswer);
        }

        console.log("Correct answers count", correctAnswersCount);
        console.log("Incorrect answers count", inCorrectAnswersCount);

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
    millisToMinutesAndSeconds(millis) {
      const date = new Date(Date.UTC(0, 0, 0, 0, 0, 0, millis)),
        parts = [
          // date.getUTCHours(),
          date.getUTCMinutes(),
          date.getUTCSeconds()
        ]
      return parts.map(s => String(s).padStart(2, '0')).join(':');
    },

    reStartQuiz() {
      this.quizState = undefined
      this.userAnswers = {}
      this.currentQuestionId = 0
      this.currentIndex = 0
      this.questionState = "unanswered"
      this.nextButtonDisabled = true
      this.radioButtonAnswer = ''
      this.checkboxAnswer = []
    },
    startQuiz() {
      this.quizState = "inprogress";

      if (!this.timer) {
        this.timerCount = this.quiz.duration * 1000 * 60;
        this.timeRemaining = this.millisToMinutesAndSeconds(this.timerCount);
      }

      this.timer = setInterval(() => {
        if (this.timerCount > 0) {
          this.timerCount -= 1000;
          this.timeRemaining = this.millisToMinutesAndSeconds(this.timerCount);

        } else {
          clearInterval(this.timer);
          this.showResults();
        }
      }, 1000);

    },

    showResults() {
      this.saveAnswer();
      this.quizState = "completed";

      this.saveUserResults()
    },

    saveUserResults(){
      const postBody = { quiz_id: this.quiz.id, score: this.computeScore.percentage };
      let url = `${window.location.origin}/${Api.saveQuizScore}`;
      axios.post(url, postBody)
        .then(response => {
          console.log("Response:" + response);
        })
        .catch(error => {
          console.log("Error:" + error);
          alert('Join Stacktips to start earning reputation and unlocking new privileges like voting and bookmarking.')
        });
    

    },

    saveAnswer() {
      const currentQuestion = this.quiz.questions[this.currentIndex];
      const keyname = currentQuestion.id.toString();

      if (currentQuestion.type === 'binary') {
        this.userAnswers[keyname] = [this.radioButtonAnswer];
      } else if (currentQuestion.type === 'multiple') {
        this.userAnswers[keyname] = this.checkboxAnswer;
      }
    },

    isCorrectAnswer(answerKey) {
      if (this.questionState == 'answered' &&
        this.quiz.questions[this.currentIndex].correctAnswer.find(answerKey)) {
        console.log("Answer is correct!")
        return true
      }
      return false;
    },

    nextQuestion(e) {
      this.saveAnswer();
      this.currentIndex++;
      this.questionState = "unanswered"
      this.nextButtonDisabled = true
      this.radioButtonAnswer = ''
      this.checkboxAnswer = []

    },

    checkAnswer(e) {
      this.saveAnswer();
      this.questionState = "answered"
    },

    answerClicked(e) {
      this.nextButtonDisabled = false
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