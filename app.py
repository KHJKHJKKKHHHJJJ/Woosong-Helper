import streamlit as st
import uuid
from db import save_message, load_messages
from chatbot import generate_response

st.set_page_config(page_title="Woosong Chatbot", page_icon="🎓", layout="wide")

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

    # 2. Gemini 응답 생성 및 처리
    with st.spinner("Generating response..."):
        # DB에서 현재까지의 대화 기록 로드 (generate_response 함수에 전달하기 위함)
        # 시스템 프롬프트는 generate_response 내부에서 처리됨
        current_history = load_messages(st.session_state.session_id)
        full_response = generate_response(current_history)

    if full_response:
        # 3. Gemini 응답을 화면에 표시하고 DB에 저장
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        with st.chat_message("assistant"):
            st.markdown(full_response)
        save_message(st.session_state.session_id, "assistant", full_response)
    else:
        # 응답 생성 실패 또는 불필요 시
        st.warning("Sorry, I couldn't generate a response.")
