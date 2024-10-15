import sqlite3
import streamlit as st
from datetime import datetime
import time

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row  # データを辞書形式で取得
    return conn

# メッセージをデータベースに保存
def save_message(user, message):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (user, message))
        conn.commit()

# メッセージをデータベースから読み込み
def load_messages():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC")
        return c.fetchall()

# チャットログをセッションにロード
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = load_messages()  # 初回メッセージをデータベースから取得

st.title("オープンチャットアプリ")

# ユーザーのメッセージ入力
user_msg = st.chat_input("メッセージを入力してください")

if user_msg:
    # メッセージをデータベースに保存
    save_message('ユーザー', user_msg)

    # 新しいメッセージをチャットログに追加
    st.session_state.chat_log.insert(0, {
        'user': 'ユーザー',
        'message': user_msg,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # ページをリロードして新しいメッセージを反映
    st.experimental_rerun()

# チャットログの表示
for chat in st.session_state.chat_log:
    st.write(f"{chat['user']} ({chat['timestamp']})")
    st.write(chat['message'])

# 自動更新用のボタン
if st.button('メッセージを更新'):
    # データベースから新しいメッセージを再取得
    new_messages = load_messages()
    
    # 新しいメッセージをセッションステートに追加
    st.session_state.chat_log = []
    for message in new_messages:
        st.session_state.chat_log.append({
            'user': message['user'],
            'message': message['message'],
            'timestamp': message['timestamp']
        })

    # ページをリロードして更新
    st.experimental_rerun()
