<template>
  <div class="form-check bloggify-form--label" :class="[
                  { '--disabled': questionStatus === QuestionState.ANSWERED },
                  { '--wrong-answer': questionStatus === QuestionState.ANSWERED && checkboxAnswer.length && !correctAnswer.includes(answerOption.key) },
                  { '--correct-answer': questionStatus === QuestionState.ANSWERED && correctAnswer.includes(answerOption.key) }
                ]">

    <label class="form-check-label ">
      <input type="checkbox" :id="answerOption.key" :disabled="questionStatus === QuestionState.ANSWERED"
             @change="answerClicked" :value="answerOption.key" v-model="checkboxAnswer"
             class="form-check-input ml-0">{{
        answerOption.value
      }}
    </label>

    <div class="check-icon --danger"
         v-if="questionStatus === QuestionState.ANSWERED && checkboxAnswer.length && !correctAnswer.includes(answerOption.key)">
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
           fill="#000000">
        <path d="M0 0h24v24H0z" fill="none"/>
        <path
            d="M15.73 3H8.27L3 8.27v7.46L8.27 21h7.46L21 15.73V8.27L15.73 3zM17 15.74L15.74 17 12 13.26 8.26 17 7 15.74 10.74 12 7 8.26 8.26 7 12 10.74 15.74 7 17 8.26 13.26 12 17 15.74z"/>
      </svg>
    </div>

    <div class="check-icon --success"
         v-if="questionStatus === QuestionState.ANSWERED && correctAnswer.includes(answerOption.key)">
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px"
           fill="#000000">
        <path d="M0 0h24v24H0z" fill="none"/>
        <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
      </svg>
    </div>

  </div>
</template>
<script>
import QuestionState from "../enums/QuestionState";
import QuizState from "../enums/QuizState";

export default {
  name: 'question-kind-multiple',
  props: {
    answerOption: {},
    currentIndex: {},
    questionStatus: {},
    correctAnswer: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      checkboxAnswer: [], //Answer Binary
    };
  },
  computed: {
    QuestionState() {
      return QuestionState
    },
    QuizState() {
      return QuizState
    },
  },
  methods: {
    answerClicked() {

      //Note, the parent checkboxAnswer[] needs to hold all user selected options list
      // This list will be matched when validating the correct answers
      if (!(this.checkboxAnswer[0] in this.$parent.checkboxAnswer)) {
        this.$parent.checkboxAnswer.push(this.checkboxAnswer[0]);
      }
      this.$parent.answerClicked();
    }
  }
}
</script>