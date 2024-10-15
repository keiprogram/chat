import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import time

# データベースに接続
conn = sqlite3.connect('chat.db')
c = conn.cursor()

# メッセージテーブルの作成
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# タイトル
st.title("オープンチャットアプリ")

# ページのリフレッシュを3秒ごとに設定
st_autorefresh(interval=3000)  # 3秒ごとにリフレッシュ

# ユーザーのメッセージ入力
user_msg = st.text_input("メッセージを入力してください")

# メッセージ送信時の処理
if user_msg:
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", ('ユーザー', user_msg))
    conn.commit()
    user_msg = ""  # メッセージ送信後に入力フィールドをリセット

# メッセージの読み込み
c.execute("SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC")
messages = c.fetchall()

# メッセージ表示
for user, message, timestamp in messages:
    st.write(f"{user} ({timestamp}): {message}")

conn.close()
