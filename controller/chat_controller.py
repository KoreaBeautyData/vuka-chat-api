import openai
import random

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from config import config, constant
from database.models import FAQ, FineTune
from router.chat.gpt import GPT, Example


def post_chat(request, session: Session):
    openai.api_key = config.OPENAI_SECRET_KEY

    question = request.question
    fine_tuned_model = request.fine_tuned_model
    if question is not None:
        question = question.strip()

    if fine_tuned_model is not None:
        fine_tune = session.query(FineTune).filter(FineTune.fine_tuned_model.like(f'%{fine_tuned_model}%')).first()
        if fine_tune is None:
            return HTTPException(detail=constant.ERROR_MODEL_NOT_EXIST[1],
                                 status_code=constant.ERROR_MODEL_NOT_EXIST[0])
    else:
        fine_tune = session.query(FineTune).filter(FineTune.status == 'succeeded'
                                                   ).order_by(FineTune.id.desc()).first()

    response = openai.Completion.create(
        model=fine_tune.model,
        prompt=f"{question}{constant.PROMPT_END_WITH}",
        temperature=constant.temperature,
        max_tokens=constant.max_tokens,
        top_p=constant.top_p,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=constant.stop
    )

    answer = f'{response.choices[0].text.strip()}'
    result = {
        'question': question,
        'answer': answer
    }
    return result


def post_chat_db(request, session: Session):
    openai.api_key = config.OPENAI_SECRET_KEY

    question = request.question
    if question is not None:
        question = question.strip()

    gpt = GPT(temperature=constant.temperature,
              max_tokens=constant.max_tokens)

    query_filter = []
    if question is not None:
        for q in question.split(' '):
            query_filter.append(or_(FAQ.question.like(f'%{q}%'),
                                    FAQ.answer.like(f'%{q}%')))

    faqs = session.query(FAQ).filter(*query_filter).all()

    if len(faqs) > 0:
        for faq in faqs:
            gpt.add_example(Example(
                f'{faq.question}',
                f'{faq.answer}'
            ))

        idx = random.randrange(0, len(faqs))
        question = faqs[idx].question

    data = gpt.submit_request(question)
    answer = data.choices[0].text.strip()
    result = {
        'question': f'Q: {question}',
        'answer': answer
    }
    return result
