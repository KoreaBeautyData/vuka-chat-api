# postgresql database
db = {
    'user': 'root',
    'pw': 'dusrufgofk1234',
    'host': 'fastapi-db.cdljnsmnne9o.ap-northeast-2.rds.amazonaws.com',
    'port': 5432,
    'database': 'fastapi_test'
}

# openAI
SECRET_KEY = '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'
temperature = 0.6
max_tokens = 256
top_p = 1.0
best_of = 1
frequency_penalty = 0.0
presence_penalty = 0.0
model = 'davinci'
engine = 'text-davinci-003'
engine_tuning = 'davinci:ft-koreabeautydata-2023-03-17-04-28-47'
engine_tuning2 = 'ada:ft-koreabeautydata-2023-03-17-07-19-34'
stop = ["\n##\n"]
COMPLETION_END_WITH = "\n##\n"
PROMPT_END_WITH = "\n##\n"
PROMPT_END_WITH2 = "\nSupported:"
PROMPT_END_WITH3 = "\n뷰카프로 ->\n"

GET_DEFAULT_PAGE_SIZE = 3

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_DELETE = -1
ERROR_DATA_NOT_EXIST = (204, "데이터가 존재 하지 않습니다")
ERROR_FILE_NOT_EXIST = (203, "파일이 존재 하지 않습니다")
ERROR_MODEL_NOT_EXIST = (202, "모델을 확인해주세요")