import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import os
from PIL import Image
from io import BytesIO

# データベースに接続
conn = sqlite3.connect('chat.db')
c = conn.cursor()

# メッセージテーブルの作成（ファイルと画像を保存するカラムを追加）
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, message TEXT, image BLOB, file BLOB, filename TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# タイトル
st.title("オープンチャットアプリ")

# ページのリフレッシュを3秒ごとに設定
st_autorefresh(interval=3000)  # 3秒ごとにリフレッシュ

# ユーザーのメッセージ入力
user_msg = st.text_input("メッセージを入力してください")

# 画像やファイルのアップロード
uploaded_image = st.file_uploader("画像を送信", type=["png", "jpg", "jpeg"])
uploaded_file = st.file_uploader("ファイルを送信", type=["pdf", "txt", "docx", "xlsx"])

# 送信ボタンを追加
if st.button("送信"):
    image_data = None
    file_data = None
    filename = None

    if user_msg or uploaded_image or uploaded_file:  # 何かが入力されている場合のみ送信
        # 画像をバイナリデータに変換
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format=uploaded_image.type.split('/')[1])
            image_data = img_byte_arr.getvalue()

        # ファイルをバイナリデータに変換
        if uploaded_file is not None:
            file_data = uploaded_file.read()
            filename = uploaded_file.name

        # メッセージとファイルをデータベースに保存
        c.execute("INSERT INTO messages (user, message, image, file, filename) VALUES (?, ?, ?, ?, ?)", 
                  ('ユーザー', user_msg, image_data, file_data, filename))
        conn.commit()
        st.success("メッセージが送信されました！")

# メッセージの読み込み
c.execute("SELECT user, message, image, file, filename, timestamp FROM messages ORDER BY timestamp DESC")
messages = c.fetchall()

# メッセージ表示
for user, message, image_data, file_data, filename, timestamp in messages:
    st.write(f"{user} ({timestamp}): {message}")
    
    # 画像表示
    if image_data is not None:
        st.image(Image.open(BytesIO(image_data)), caption=f"{user}が送信した画像", use_column_width=True)
    
    # ファイル表示とダウンロードリンク
    if file_data is not None:
        st.download_button(label=f"{filename} をダウンロード", data=file_data, file_name=filename)

# データベース接続を閉じる
conn.close()
