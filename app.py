# -*- coding: utf-8 -*-
# 消費紀錄系統 Streamlit 雲端版 v1.1（使用環境變數設定密碼）

import streamlit as st
import pandas as pd
import os
from io import StringIO

# =======================
# 基本設定
# =======================
st.set_page_config(page_title="消費紀錄系統", page_icon="💰", layout="centered")

# 從環境變數讀取密碼（如未設定則預設為 1234）
PASSWORD = os.getenv("APP_PASSWORD", "1234")

# =======================
# 登入機制
# =======================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 登入系統")
    pwd = st.text_input("請輸入密碼", type="password")
    if st.button("登入"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.success("登入成功！")
            st.rerun()
        else:
            st.error("密碼錯誤，請重試。")
    st.stop()

# =======================
# 主介面
# =======================
st.title("💰 消費紀錄系統（雲端版）")

if "records" not in st.session_state:
    st.session_state.records = []

# -----------------------
# 新增紀錄
# -----------------------
st.subheader("📝 新增紀錄")

col1, col2 = st.columns(2)
with col1:
    date = st.date_input("日期")
    item = st.text_input("項目")
with col2:
    price = st.number_input("單價", min_value=0, step=1)
    qty = st.number_input("數量", min_value=1, value=1)

note = st.text_input("備註")

if st.button("新增"):
    if item:
        st.session_state.records.append({
            "日期": date, "項目": item, "單價": price, "數量": qty,
            "總價": price * qty, "備註": note
        })
        st.success(f"✅ 已新增 {item}")
    else:
        st.warning("請輸入項目名稱。")

# -----------------------
# 顯示與管理紀錄
# -----------------------
if st.session_state.records:
    st.subheader("📋 紀錄清單")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

    # 刪除紀錄
    delete_index = st.number_input("輸入要刪除的列號（從 0 開始）", min_value=0, step=1)
    if st.button("刪除紀錄"):
        if delete_index < len(st.session_state.records):
            deleted_item = st.session_state.records.pop(delete_index)
            st.success(f"🗑️ 已刪除 {deleted_item['項目']}")
        else:
            st.warning("列號不存在。")

    # 匯出資料
    csv = pd.DataFrame(st.session_state.records).to_csv(index=False).encode('utf-8-sig')
    st.download_button("📤 匯出CSV", csv, "消費紀錄.csv", "text/csv")

    # 匯入資料
    uploaded_file = st.file_uploader("📥 匯入CSV", type="csv")
    if uploaded_file is not None:
        df_new = pd.read_csv(uploaded_file)
        st.session_state.records.extend(df_new.to_dict('records'))
        st.success("✅ 匯入完成，已新增資料。")

# -----------------------
# 登出按鈕
# -----------------------
st.divider()
if st.button("🚪 登出"):
    st.session_state.authenticated = False
    st.rerun()
