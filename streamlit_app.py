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
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (user, message))
            conn.commit()
    except Exception as e:
        st.error(f"メッセージの保存中にエラーが発生しました: {e}")

# メッセージをデータベースから読み込み
def load_messages():
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC")
            return c.fetchall()
    except Exception as e:
        st.error(f"メッセージの読み込み中にエラーが発生しました: {e}")
        return []

# チャットログをセッションにロード
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = load_messages()  # 初回メッセージをデータベースから取得

st.title("オープンチャットアプリ")

# ユーザーのメッセージ入力
user_msg = st.chat_input("メッセージを入力してください")

if user_msg:
    # メッセージをデータベースに保存
    save_message('ユーザー', user_msg)

    # チャットログを更新
    st.session_state.chat_log.insert(0, {
        'user': 'ユーザー',
        'message': user_msg,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # セッション内で直接リフレッシュするのではなく、データを反映
    st.experimental_rerun()  # ← 問題の可能性があるためここを使用せずに他の方法を試す

# チャットログの表示
for chat in st.session_state.chat_log:
    st.write(f"{chat['user']} ({chat['timestamp']})")
    st.write(chat['message'])

# 自動更新 (定期的にページをリロードする方法)
st_autorefresh(interval=3000)  # 3秒ごとにページを自動的にリフレッシュ
