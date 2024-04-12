import openai
import json

response = openai.Completion.create(          # ChatCompletion 대신 Completion을 사용  // 이는 Complete 모델 API 호출방식
    engine = "gpt-3.5-turbo-instruct",        # model 대신 engine을 지정하고 gpt-3.5-turbo-instruct를 지정 // Complete 모델 API 호출방식
    prompt = "오늘 날씨가 매우 좋고 기분이",                                            # 'Chat'의    
    stop= ".",                                # 문자가 나오면 종료
    max_tokens = 100,                         # 최대 토큰 수 
    n = 2,                                    # 인덱스 수
    temperature = 0.5                         # 다양성 매개변수
)

print(json.dumps(response, indent=2, ensure_ascii= False))

