import openai
import shutil
import json
import csv

from sqlalchemy.orm import Session

from config import config
from database.schema import DefaultModel
from database.models import FineTune


def get_fine_tune_list():
    openai.api_key = config.SECRET_KEY

    fine_tune_list = openai.FineTune.list()
    return fine_tune_list

def post_convert_csv_to_jsonl(file):
    path = f'csv_file/'
    filename = file.filename.split('.')[0]
    with open(f'{path}{file.filename}', 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)

    csvfile = open(f'{path}{file.filename}', 'r')
    jsonfile = open(f'{path}{filename}_prepared.jsonl', 'w')

    fieldnames = ("prompt", "completion")
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile, ensure_ascii=False)
        jsonfile.write('\n')
    return jsonfile.name

def post_fine_tuning(file, session: Session):
    response = DefaultModel()

    openai.api_key = config.SECRET_KEY

    # 파일 업로드
    tune_file = openai.File.create(
        file=open(f'csv_file/{file.filename}', 'rb'),
        purpose='fine-tune'
    )

    # 미세 조정 작업 생성
    fine_tune_model = openai.FineTune.create(training_file=tune_file.id, model=config.model)

    # 미세 조정 정보 db에 저장
    fine_tune = FineTune()
    fine_tune.status = fine_tune_model.status
    fine_tune.ft_id = fine_tune_model.id
    fine_tune.model = config.model
    fine_tune.fine_tune_model = fine_tune_model.fine_tuned_model
    fine_tune.data = json.dumps(fine_tune_model)
    session.add(fine_tune)
    session.commit()

    response.result_data = {
        'fine_tune': fine_tune_model
    }
    return response

def get_fine_tuning_status(id, session: Session):
    openai.api_key = config.SECRET_KEY

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
