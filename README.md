# Vuka faq/chat api

http://openai.codecom.co.kr/api

### API 목록

- FAQ
  - FAQ 목록 : [GET] /faq
  - FAQ 등록 : [POST] /faq
  - FAQ 상세 : [GET] /faq/<faq_id>
  - FAQ 수정 : [PUT] /faq/<faq_id>
  - FAQ 삭제 : [DELETE] /faq/<faq_id>
  - FAQ csv : [GET] /faq/csv

- FineTune
  - 튜닝 목록 : [GET] /fine-tune
  - 튜닝 모델 목록 : [GET] /fine-tune/model
  - 튜닝 상세 : [GET] /fine-tune/<fine_tune_id>
  - 튜닝 상태 조회 : [GET] /fine-tune/<fine_tune_id>/status
  - 파일 변환(csv to jsonl) : [POST] /fine-tune/convert
  - 파일 튜닝 : [POST] /fine-tune/tuning

- Chatbot
  - 채팅 테스트 : [POST] /chat
  - 채팅 테스트(데이터베이스 기반) : [POST] /chat/db