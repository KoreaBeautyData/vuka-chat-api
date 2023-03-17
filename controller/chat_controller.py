import openai

from typing import Optional
from fastapi import APIRouter
from sqlalchemy import or_
from sqlalchemy.orm import Session

from config import config
from database.models import FAQ
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
    if question is not None:
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

def fine_tuning(session: Session):
    openai.api_key = config.SECRET_KEY
    # openai.File.create(
    #     file=open("csv_file/faq2_prepared.jsonl", "rb"),
    #     purpose='fine-tune'
    # )

    fine_tune_list = openai.FineTune.list()
    # fine_tune_event_list = openai.FineTune.list_events(id="ft-ZH4wTwGqbYNIxjRPaCD7uQ6A")
    # file_list = openai.File.list()
    # engine = openai.Engine.list()
    # file_retrieve = openai.File.retrieve("file-te85pltb1FpkGWZI6xdQ4TCQ")
    # content = openai.File.download("file-te85pltb1FpkGWZI6xdQ4TCQ")

    # response = openai.Completion.create(
    #     model=config.engine_tuning,
    #     prompt=f"뷰카프로는 어떤 서비스인가요{config.PROMPT_END_WITH}",
    #     max_tokens=config.max_tokens,
    #     temperature=config.temperature,
    #     top_p=config.top_p,
    #     best_of=config.best_of,
    #     frequency_penalty=config.frequency_penalty,
    #     presence_penalty=config.presence_penalty,
    #     stop=config.stop
    # )


    import random

    faq_query = session.query(FAQ)
    random_faq_id = random.randrange(1, faq_query.count())
    faq = faq_query.filter(FAQ.id == random_faq_id).first()

    response = openai.Completion.create(
        model=config.engine_tuning,
        prompt=f"{faq.question}{config.PROMPT_END_WITH}",
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        top_p=config.top_p,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=config.stop
    )
    result = {
        'question': faq.question,
        'answer': faq.answer,
        'ai_Q': f"{faq.question}{config.PROMPT_END_WITH}",
        'ai_A': response.choices[0].text.strip()
    }
    return result