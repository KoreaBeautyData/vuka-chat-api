import openai
import json
import csv

from sqlalchemy.orm import Session

from config import config
from database.schema import DefaultModel
from database.models import FineTune
from config.error_handling import UnicornException


def get_fine_tune_list(session: Session, page, page_length, refresh=False):
    response = DefaultModel()

    if page <= 0:
        page = 1
    else:
        page = page

    fine_tune_query = session.query(FineTune).order_by(FineTune.created_at.desc())

    if refresh == True:
        openai.api_key = config.OPENAI_SECRET_KEY
        for fine_tune in openai.FineTune.list().data:
            tune_data = fine_tune_query.filter(FineTune.ft_id == fine_tune.id).first()
            if tune_data is not None:
                tune_data.fine_tuned_model = fine_tune.fine_tuned_model
                tune_data.status = fine_tune.status
                tune_data.data = json.dumps(fine_tune)
                session.commit()

    fine_tune_list = fine_tune_query.offset(page_length * (page - 1)).limit(page_length).all()

    response.result_data = {
        'fine_tune_list': fine_tune_list,
        'fine_tune_count': fine_tune_query.count(),
        'page_length': page_length
    }
    return response


def get_fine_tune_model_list(session: Session):
    response = DefaultModel()

    fine_tune_model_list = session.query(FineTune
                        ).filter().order_by(FineTune.created_at.desc()).all()
    response.result_data = {
        'fine_tune_model_list': fine_tune_model_list,
    }
    return response


def get_fine_tune_detail(session: Session, fine_tune_id):
    response = DefaultModel()

    fine_tune = session.query(FineTune).filter(FineTune.id == fine_tune_id).first()

    response.result_data = {
        'fine_tune': fine_tune,
    }
    return response


def post_convert_csv_to_jsonl(session: Session, request):
    path = f'csv_file/'
    file = request.filename
    filename = file.split('.')[0]

    try:
        csvfile = open(f'{path}{file}', 'r')
        jsonfile = open(f'{path}{filename}_prepared.jsonl', 'w')

        fieldnames = ("prompt", "completion")
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            json.dump(row, jsonfile, ensure_ascii=False)
            jsonfile.write('\n')

        fine_tune = session.query(FineTune).filter(FineTune.filename == f'{filename}.csv').first()
        if fine_tune is not None:
            fine_tune.filename = f'{filename}_prepared.jsonl'
            session.commit()

        result = {
            'filename': request.filename
        }
        return result
    except FileNotFoundError:
        raise UnicornException(result_msg=config.ERROR_FILE_NOT_EXIST[1],
                               result_code=config.ERROR_FILE_NOT_EXIST[0])
    except IsADirectoryError:
        raise UnicornException(result_msg=config.ERROR_FILE_NOT_EXIST[1],
                               result_code=config.ERROR_FILE_NOT_EXIST[0])


def post_fine_tuning(session: Session, request):
    response = DefaultModel()

    filename = request.filename

    openai.api_key = config.OPENAI_SECRET_KEY

    try:
        # 파일 업로드
        tune_file = openai.File.create(
            file=open(f'csv_file/{filename}', 'rb'),
            purpose='fine-tune'
        )

        # 미세 조정 작업 생성
        fine_tune_model = openai.FineTune.create(training_file=tune_file.id, model=config.model)

        # 미세 조정 정보 db에 저장
        fine_tune = session.query(FineTune).filter(FineTune.filename == f'{filename}').first()
        if fine_tune is not None:
            fine_tune.status = fine_tune_model.status
            fine_tune.ft_id = fine_tune_model.id
            fine_tune.model = config.model
            fine_tune.fine_tune_model = fine_tune_model.fine_tuned_model
            fine_tune.data = json.dumps(fine_tune_model)
            session.commit()

        response.result_data = {
            'fine_tune': fine_tune_model,
            'filename': fine_tune.filename
        }
        return response
    except FileNotFoundError:
        raise UnicornException(result_msg=config.ERROR_FILE_NOT_EXIST[1],
                               result_code=config.ERROR_FILE_NOT_EXIST[0])

def get_fine_tuning_status(id, session: Session):
    openai.api_key = config.OPENAI_SECRET_KEY

    fine_tune = openai.FineTune.retrieve(id=id)

    fine_tune_obj = session.query(FineTune).filter(FineTune.ft_id == id).first()
    if fine_tune_obj is not None:
        fine_tune_obj.status = fine_tune.status
        fine_tune_obj.fine_tuned_model = fine_tune.fine_tuned_model
        session.commit()

    result = {
        'status': fine_tune.status,
        'fine_tuned_model': fine_tune.fine_tuned_model,
    }
    return result
