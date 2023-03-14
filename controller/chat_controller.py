import openai

from typing import Optional, List
from fastapi import APIRouter
from sqlalchemy import or_, and_, BinaryExpression
from sqlalchemy.orm import Session

import config
from models import FAQ
from router.chat.gpt import GPT, Example


router = APIRouter(
    prefix="/api/chat",
)


def get_chat(session: Session,
               question: Optional[str] = None):
    openai.api_key = config.SECRET_KEY
    # prompt_initial = f'Human:%s\nAI:' % (question)
    #
    # last_history_object = session.query(History).order_by(History.id.desc()).first()
    # if last_history_object is None:
    #     last_history = ''
    # else:
    #     last_history = last_history_object.content
    # # prompt = f'{last_history}\n{prompt_initial}'
    # prompt = last_history + '\n' + prompt_initial
    #
    # response = openai.Completion.create(
    #     model='davinci',
    #     # model=config.engine3,
    #     prompt=f"{question}",
    #     temperature=config.temperature,
    #     max_tokens=config.max_tokens,
    #     top_p=config.top_p,
    #     frequency_penalty=config.frequency_penalty,
    #     presence_penalty=config.presence_penalty,
    #     stop=config.stop
    # )
    # print(response.choices[0].text.strip())
    # result = response.choices[0].text.strip()
    # content = prompt + result
    #
    # history = History()
    # history.question = question
    # history.answer = result
    # history.content = content
    # session.add(history)
    # session.commit()

    gpt = GPT(temperature=config.temperature, max_tokens=config.max_tokens)

    query_filter = []
    for q in question.split(' '):
        query_filter.append(or_(FAQ.question.like(f'%{q}%'),
                                FAQ.answer.like(f'%{q}%')))

    faqs = session.query(FAQ).filter(*query_filter).all()

    for faq in faqs:
        gpt.add_example(Example(
            f'{faq.question}',
            f'{faq.answer}'
        ))

    if len(faqs) > 0:
        question = faqs[0].question

    result = gpt.submit_request(question)
    answer = result.choices[0].text.strip()
    return answer
