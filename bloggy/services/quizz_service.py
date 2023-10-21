import logging

logger = logging.getLogger(__name__)


def get_questions_json(post):
    questions = []
    for question in post.get_questions():

        answers = []
        correct_answer = []
        question_answers = question.get_answers()
        for index, answer in enumerate(question_answers):
            key_char = chr(index + 97)

            answers.append({
                "value": answer.content,
                "key": key_char
            })
            if answer.correct:
                correct_answer.append(key_char)

        questions.append({
            "id": question.id,
            "title": question.title,
            "description": question.description if question.description else "",
            "type": question.type,
            "explanation": question.explanation if question.explanation else "",
            "answers": answers,
            "correctAnswer": correct_answer
        })

    category = post.category.first()
    category_json = None
    if category:
        category_json = {
            "title": category.title,
            "slug": category.slug,
            "id": category.id
        }

    return {
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content if post.content else "",
        'questions_count': len(questions),
        'duration': post.duration,
        'logo': post.thumbnail.url if post.thumbnail else "",
        'questions': questions,
        'time': post.duration,
        'category': category_json
    }

