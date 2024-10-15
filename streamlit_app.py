import sqlite3

# データベースに接続
conn = sqlite3.connect('chat.db')
c = conn.cursor()

# テーブルの作成
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()
conn.close()
import streamlit as st
import sqlite3
import pandas as pd

st.title("オープンチャットアプリ")

# チャットログを保存するセッションステート
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

# ユーザーのメッセージ入力
user_msg = st.chat_input("メッセージを入力してください")

if user_msg:
    # メッセージをデータベースに保存
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", ('ユーザー', user_msg))
    conn.commit()
    conn.close()

    # チャットログに追加
    st.session_state.chat_log.append({'user': 'ユーザー', 'message': user_msg})

# チャットログの表示
for chat in st.session_state.chat_log:
    st.chat_message(chat['user'], chat['message'])

# メッセージの読み込み
conn = sqlite3.connect('chat.db')
c = conn.cursor()
c.execute("SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC")
messages = c.fetchall()
conn.close()

# メッセージの表示
for user, message, timestamp in messages:
    st.chat_message(user, message, timestamp)
