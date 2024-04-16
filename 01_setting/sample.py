import json
import openai  # openai 

response = openai.ChatCompletion.create(  # api 호출
    model = "gpt-3.5-turbo",   # 모델명
    messages = [
        {
            "role" : "user",
            "content" : "iPhone8의 출시일 알려줘"  # 프롬포트
        },
    ],
    max_tokens=100,  # 생성할 문장의 최대 토큰 수
    temperature=1,  # 생성할 문장의 다양성을 나타내는 변수
    n=2,            # 문장의 개수 ( 0 ~ 2 )
)

print(json.dumps(response, indent=2, ensure_ascii=False))
# 결과를 response 변수에 저장 후 json.dumps로 내용을 변환.

# {
#   "id": "chatcmpl-9D2lecw0SKlCYHJ7jTdQ3tUlKt61T",
#   "object": "chat.completion",
#   "created": 1712895930,
#   "model": "gpt-3.5-turbo-0125",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "\"콘소메\"는 \"Consomme\"라는 프랑스어 단어로, 통틀어서 깊고 풍부한
# 맛을 가진 정제된 육수를 가리킵니다. 일반적으로 육수를 끓여 구운 후 여러 과정을 거쳐 정화
# 된 육수를 말하며,"
#       },
#       "logprobs": null,
#       "finish_reason": "length"
#     },
#     {
#       "index": 1,
#       "message": {
#         "role": "assistant",
#         "content": "콘소메란 \"콘텐츠 소비자 메타버스\"의 줄임말로, 현재의 인터넷 콘텐츠
#  소비 형태에 가상현실(VR), 증강현실(AR), 혼합현실(MR) 등의 기술을 접목"
#       },
#       "logprobs": null,
#       "finish_reason": "length"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 23,
#     "completion_tokens": 200,
#     "total_tokens": 223
#   },
#   "system_fingerprint": "fp_b28b39ffa8"
# }