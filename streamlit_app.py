import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3

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

# 送信ボタンを追加
if st.button("送信"):
    if user_msg:  # メッセージが空でない場合のみ送信
        c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", ('ユーザー', user_msg))
        conn.commit()
        st.success("メッセージが送信されました！")

# メッセージの読み込み
c.execute("SELECT user, message, timestamp FROM messages ORDER BY timestamp DESC")
messages = c.fetchall()

# メッセージ表示
for user, message, timestamp in messages:
    st.write(f"{user} ({timestamp}): {message}")

# データベース接続を閉じる
conn.close()
