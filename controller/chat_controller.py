import openai
import random
from sqlalchemy import or_

from sqlalchemy.orm import Session

from config import config
from config.error_handling import UnicornException
from database.models import FAQ, FineTune
from router.chat.gpt import GPT, Example


def post_chat(request, session: Session):
    openai.api_key = config.SECRET_KEY

    question = request.question
    fine_tuned_model = request.fine_tuned_model
    if question is not None:
        question = question.strip()

    if fine_tuned_model is not None:
        fine_tune = session.query(FineTune).filter(FineTune.fine_tuned_model.like(f'%{fine_tuned_model}%')).first()
        if fine_tune is None:
            return UnicornException(result_msg=config.ERROR_MODEL_NOT_EXIST[1],
                                    result_code=config.ERROR_MODEL_NOT_EXIST[0])
    else:
        fine_tune = session.query(FineTune).filter(FineTune.status == 'succeeded'
                                                   ).order_by(FineTune.id.desc()).first()

    response = openai.Completion.create(
        model=fine_tune.model,
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


def post_chat_db(request, session: Session):
    openai.api_key = config.SECRET_KEY

    question = request.question
    if question is not None:
        question = question.strip()

    gpt = GPT(temperature=config.temperature,
              max_tokens=config.max_tokens)

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
