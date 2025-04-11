import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# Gemini API 키 설정
api_key_raw = os.getenv("GEMINI_API_KEY")
if not api_key_raw:
    raise ValueError("GEMINI_API_KEY 환경 변수를 설정해주세요.")

# '#' 문자가 있다면 그 앞부분만 사용 (주석 처리 문제 방지)
api_key = api_key_raw.split('#')[0].strip().strip('"')

genai.configure(api_key=api_key)
print(f"Loaded API Key: {api_key[:5]}...{api_key[-5:]}") # 디버깅용: 로드된 키 일부 출력 (이제 제거됨)

# Gemini 모델 초기화
model = genai.GenerativeModel('gemini-1.5-flash') # 또는 다른 원하는 모델

# 시스템 프롬프트 (챗봇의 역할 및 페르소나 설정)
SYSTEM_PROMPT = """
You are a friendly and helpful AI chatbot designed to assist international students at Woosong University.
Answer student questions and provide help on various topics such as campus life, academic information, campus facilities, etc.
Always use polite and clear language.
"""

def generate_response(history):
    """대화 기록을 바탕으로 Gemini API를 호출하여 응답을 생성합니다."""
    try:
        # 시스템 프롬프트를 대화 시작 부분에 추가
        conversation_history = [{'role': 'user', 'parts': [SYSTEM_PROMPT]},
                                {'role': 'model', 'parts': ["Hello! I am the Woosong University chatbot. How can I help you today?"]}]
        
        # DB에서 로드된 메시지를 Gemini API 형식에 맞게 변환
        for message in history:
            role = 'user' if message['role'] == 'user' else 'model'
            conversation_history.append({'role': role, 'parts': [message['content']]})

        # 마지막 메시지가 user의 메시지일 경우에만 응답 생성
        if conversation_history[-1]['role'] == 'user':
            response = model.generate_content(conversation_history)
            return response.text
        else:
            # 마지막 메시지가 model의 메시지이면 추가 응답 생성 불필요
            return None 
    except Exception as e:
        print(f"Gemini API 호출 오류: {e}")
        return "죄송합니다. 응답을 생성하는 중에 오류가 발생했습니다."
