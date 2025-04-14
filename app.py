import streamlit as st
import uuid
from db import save_message, load_messages
from chatbot import generate_response as generate_response_gemini
from local_model import LocalLLM  # local_model.py에서 LocalLLM 클래스 import
import os

st.set_page_config(page_title="Woosong Chatbot", page_icon="🎓", layout="wide")

# --- 모델 초기화 ---
@st.cache_resource  # 이 데코레이터는 모델을 한 번만 로드하고 캐시합니다
def load_local_model():
    return LocalLLM()

# --- 사이드바에 모델 선택 옵션 추가 ---
with st.sidebar:
    st.title("Model Settings")
    model_option = st.selectbox(
        "Select AI Model",
        ["Gemini-1.5-Flash", "Local-Qwen-0.5B"],
        help="Select the AI model to use for generating responses"
    )
    
    if model_option == "Local-Qwen-0.5B":
        try:
            if 'local_model' not in st.session_state:
                with st.spinner("Loading local model..."):
                    st.session_state.local_model = load_local_model()
            st.success("Local model loaded successfully!")
        except Exception as e:
            st.error(f"Model loading failed: {str(e)}")
            st.warning("Switching back to Gemini model.")
            model_option = "Gemini-1.5-Flash"

st.title("🎓 Woosong University Student Chatbot")
st.caption("Hello! I'm an AI chatbot for Woosong University students. Ask me anything!")

# --- 세션 상태 초기화 ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    # 세션 시작 시 DB에서 이전 대화 기록 로드
    st.session_state.messages = load_messages(st.session_state.session_id)
    # DB에 기록이 없으면 초기 메시지 추가 (화면 표시용)
    if not st.session_state.messages:
        st.session_state.messages = [{'role': 'assistant', 'content': "Hello! How can I help you today?"}]

# --- 대화 내용 표시 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 사용자 입력 처리 ---
prompt = st.chat_input("Enter your message here...")

if prompt:
    # 1. 사용자 메시지를 화면에 표시하고 DB에 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    save_message(st.session_state.session_id, "user", prompt)

    # 2. 선택된 모델에 따라 응답 생성
    with st.spinner("Generating response..."):
        if model_option == "Gemini-1.5-Flash":
            current_history = load_messages(st.session_state.session_id)
            full_response = generate_response_gemini(current_history)
        else:  # Local-Qwen-0.5B
            # 로컬 모델은 현재 메시지만 처리
            full_response = st.session_state.local_model.generate_response(prompt)

    if full_response:
        # 3. 응답을 화면에 표시하고 DB에 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        with st.chat_message("assistant"):
            st.markdown(full_response)
        save_message(st.session_state.session_id, "assistant", full_response)
    else:
        # 응답 생성 실패 또는 불필요 시
        st.warning("Sorry, I couldn't generate a response.")

# --- 모델 상태 표시 ---
with st.sidebar:
    st.divider()
    st.write("Currently using model:", model_option)
    if model_option == "Local-Qwen-0.5B":
        st.write("Model Status: Loaded")
        st.write("Device:", st.session_state.local_model.device if 'local_model' in st.session_state else "Not loaded")
