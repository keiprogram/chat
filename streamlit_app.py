import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import hashlib
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_cookies_manager import EncryptedCookieManager  # 追加

# パスワードをハッシュ化する関数
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ハッシュ化されたパスワードをチェックする関数
def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# 新しいユーザーを追加する関数
def add_user(conn, username, password):
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
    conn.commit()

# ユーザーをログインさせる関数
def login_user(conn, username, password):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    return c.fetchall()

# ユーザー名の存在を確認する関数
def check_user_exists(conn, username):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    return c.fetchone() is not None

def main():
    st.title("モチベーション向上")

    # クッキーマネージャーの初期化
    cookies = EncryptedCookieManager(prefix="user_", key="some_secret_key")
    if not cookies.ready():
        st.stop()

    # データベースに接続
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()

    # ユーザーがログイン済みかどうかクッキーで確認
    if "logged_in" in cookies and cookies["logged_in"]:
        st.session_state['username'] = cookies['username']

    menu = ["ホーム", "ログイン", "サインアップ", "使い方"]
    choice = st.sidebar.selectbox("メニュー", menu)

    if choice == "ホーム":
        if 'username' in st.session_state:
            st.write(f"ようこそ、{st.session_state['username']}さん！")
        else:
            st.warning("まずログインしてください。")

    elif choice == "ログイン":
        st.subheader("ログイン画面です")
        username = st.sidebar.text_input("ユーザー名を入力してください")
        password = st.sidebar.text_input("パスワードを入力してください", type='password')

        if st.sidebar.button("ログイン"):
            result = login_user(conn, username, make_hashes(password))

            if result:
                # セッションステートに保存
                st.session_state['username'] = username
                st.success(f"{username} さんでログインしました")

                # クッキーに保存
                cookies["logged_in"] = True
                cookies["username"] = username
                cookies.save()

                st.success('ホーム画面に移動して下さい')

            else:
                st.warning("ユーザー名かパスワードが間違っています")

    elif choice == "サインアップ":
        st.subheader("新しいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください", type='password')

        if st.button("サインアップ"):
            if check_user_exists(conn, new_user):
                st.error("このユーザー名は既に使用されています。別のユーザー名を選んでください。")
            else:
                add_user(conn, new_user, make_hashes(new_password))
                st.success("アカウントの作成に成功しました")
                st.info("ログイン画面からログインしてください")

    elif choice == "使い方":
        st.text("チームスに付属の使い方動画を見てください")

    conn.close()

if __name__ == '__main__':
    main()
