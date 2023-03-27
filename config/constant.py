GET_DEFAULT_PAGE_SIZE = 3

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_DELETE = -1
ERROR_DATA_NOT_EXIST = (201, "데이터가 존재 하지 않습니다")
ERROR_MODEL_NOT_EXIST = (202, "모델이 존재 하지 않습니다")
ERROR_FILE_NOT_EXIST = (203, "파일이 존재 하지 않습니다")

# openAI
model = 'davinci'
engine = 'text-davinci-003'
temperature = 0.6
max_tokens = 256
top_p = 1.0
best_of = 1
frequency_penalty = 0.0
presence_penalty = 0.0
stop = ["\n"]
PROMPT_END_WITH = "Vuka Supported -> :"
