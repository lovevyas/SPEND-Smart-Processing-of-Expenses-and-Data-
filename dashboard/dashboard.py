# -------------------------------
# Path setup
# -------------------------------
import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

import sqlite3
import tempfile
import pandas as pd
import streamlit as st
from main import process_image 




DB_PATH = os.path.join(PROJECT_ROOT, "spend.db")

# -------------------------------
# DB helpers
# -------------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)

def load_transactions():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY created_at DESC",
        conn
    )
    conn.close()
    return df

# -------------------------------
# Streamlit config
# -------------------------------
st.set_page_config(
    page_title="SPEND – Expense Dashboard",
    layout="wide"
)

st.title("💸 SPEND – Expense Dashboard")
st.caption("AI-powered expense tracking from receipts & payments")

# -------------------------------
# Upload data
# -------------------------------
st.subheader("📤 Add New Expenses")

uploaded_files = st.file_uploader(
    "Upload bill or payment screenshots",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)
if uploaded_files:
    with st.spinner("Processing uploaded bills..."):
        for file in uploaded_files:
            st.write(f"Processing: {file.name}")
            
if uploaded_files:
    with st.spinner("Processing uploaded bills..."):
        for idx, file in enumerate(uploaded_files, start=1):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(file.read())
                temp_path = tmp.name

            txn = process_image(temp_path)
            st.success(f"Added expense: {txn['merchant']} – {txn['amount']}")

    st.rerun()



# -------------------------------
# Load data
# -------------------------------
df = load_transactions()

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.header("🔍 Filters")

selected_date = st.sidebar.selectbox(
    "Filter by date",
    ["All"] + sorted(df["date"].dropna().unique().tolist())
)

if selected_date != "All":
    df = df[df["date"] == selected_date]

# -------------------------------
# Overview metrics
# -------------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Transactions", len(df))

with col2:
    st.metric("Total Spend", f"{df['amount'].sum():.2f}")

with col3:
    st.metric("Avg Confidence", f"{df['confidence'].mean():.2f}")

# -------------------------------
# Transactions table
# -------------------------------
st.subheader("📄 All Transactions")
st.dataframe(df, width="stretch")


# -------------------------------
# Spend by Merchant
# -------------------------------
st.subheader("🏪 Spend by Merchant")

merchant_df = (
    df.groupby("merchant", as_index=False)["amount"]
    .sum()
    .sort_values("amount", ascending=False)
)

if not merchant_df.empty:
    st.bar_chart(merchant_df.set_index("merchant"))
else:
    st.info("No merchant data available.")

# -------------------------------
# Spend by Wallet
# -------------------------------
st.subheader("💳 Spend by Wallet")

wallet_df = (
    df[df["wallet_id"].notnull()]
    .groupby("wallet_id", as_index=False)["amount"]
    .sum()
)

if not wallet_df.empty:
    st.bar_chart(wallet_df.set_index("wallet_id"))
else:
    st.info("No wallet-based transactions yet.")
    
# -------------------------------
# Monthly Spend
# -------------------------------
st.subheader("📆 Monthly Spending")

df["month"] = df["date"].str[:7]

monthly = df.groupby("month", as_index=False)["amount"].sum()
st.line_chart(monthly.set_index("month"))

# -------------------------------
# Unusual Spend
# -------------------------------

st.subheader("⚠️ Unusual Expenses")

threshold = df["amount"].mean() + 2 * df["amount"].std()
outliers = df[df["amount"] > threshold]

if not outliers.empty:
    st.dataframe(outliers)
else:
    st.write("No unusually high expenses detected.")
