import sqlite3
from datetime import datetime

DB_NAME = "chatbot_history.db"

def connect_db():
    """데이터베이스에 연결하고 커서를 반환합니다."""
    conn = sqlite3.connect(DB_NAME)
    # ROW 팩토리를 사용하여 딕셔너리 형태로 결과를 받을 수 있도록 설정
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """'messages' 테이블이 없으면 생성합니다."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_message(session_id, role, content):
    """메시지를 데이터베이스에 저장합니다."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    """, (session_id, role, content, datetime.now()))
    conn.commit()
    conn.close()

def load_messages(session_id, limit=50):
    """특정 세션의 최근 메시지를 불러옵니다."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content FROM messages
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (session_id, limit))
    # DB는 최신순으로 가져오지만, 실제 대화 순서는 오래된 것이 먼저이므로 역순으로 반환
    messages = [{"role": row["role"], "content": row["content"]} for row in cursor.fetchall()][::-1]
    conn.close()
    return messages

# 앱 시작 시 테이블 자동 생성
create_table()
