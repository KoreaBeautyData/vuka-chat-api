import openai
import shutil

from typing import Optional
from fastapi import APIRouter
from sqlalchemy import or_
from sqlalchemy.orm import Session

from config import config
from database.models import FAQ, FineTune
from router.chat.gpt import GPT, Example


def post_chat(request, session: Session):
    openai.api_key = config.SECRET_KEY

    question = request.question
    if question is not None:
        question = question.strip()

    last_fine_tune_model = session.query(FineTune).filter(FineTune.status == 'succeeded'
                                                ).order_by(FineTune.id.desc()).first()
    if last_fine_tune_model is not None:
        model = last_fine_tune_model.fine_tuned_model
    else:
        model = config.model

    response = openai.Completion.create(
        model=model,
        prompt=f"{question}{config.PROMPT_END_WITH3}",
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        top_p=config.top_p,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=config.stop
    )

    answer = f'{response.choices[0].text.strip()}'
    # result = f'Q: {question}\nA: {answer}'
    result = {
        'question': question,
        'answer': answer
    }

    # ----------------------------------

    # gpt = GPT(temperature=config.temperature, max_tokens=config.max_tokens)
    #
    # query_filter = []
    # if question is not None:
    #     for q in question.split(' '):
    #         query_filter.append(or_(FAQ.question.like(f'%{q}%'),
    #                                 FAQ.answer.like(f'%{q}%')))
    #
    # faqs = session.query(FAQ).filter(*query_filter).all()
    #
    # for faq in faqs:
    #     gpt.add_example(Example(
    #         f'{faq.question}',
    #         f'{faq.answer}'
    #     ))
    #
    # if len(faqs) > 0:
    #     question = faqs[0].question
    #
    # result = gpt.submit_request(question)
    # answer = result.choices[0].text.strip()
    return result
