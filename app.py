from sklearn.linear_model import LinearRegression
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    question TEXT,
    answer TEXT
)
""")
conn.commit()


st.set_page_config(page_title="AI Data Chatbot", layout="wide")

st.markdown("<h1 style='text-align:center;'>🤖 AI Data Analyst Chatbot</h1>", unsafe_allow_html=True)

# Sample button
if st.button("Use Sample Data"):
    df = pd.read_csv("sample_data.csv")
    st.session_state["df"] = df

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    st.session_state["df"] = df

if "df" not in st.session_state:
    st.warning("⚠ Upload a dataset or use sample data")
else:
    df = st.session_state["df"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

    with col2:
        st.subheader("📈 KPI Metrics")
        st.metric("Total Quantity", df["quantity"].sum())
        st.metric("Average Price", round(df["price"].mean(), 2))
        st.metric("Max Price", df["price"].max())

    st.markdown("---")

    # Chat history
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    query = st.text_input("💬 Ask your data question")

    if query:
        response = ""

        q = query.lower()

        if "total sales" in q:
            response = f"Total Sales: {df['price'].sum()}"
        elif "average price" in q:
            response = f"Average Price: {round(df['price'].mean(),2)}"
        elif "highest product" in q:
            top = df.loc[df["price"].idxmax()]
            response = f"Top Product: {top['product']} ({top['price']})"
        else:
            response = "Try: total sales, average price, highest product"

        st.session_state["chat"].append((query, response))
        cursor.execute("INSERT INTO queries VALUES (?, ?)", (query, response))
        conn.commit()

    # Display chat
    st.subheader("💬 Chat History")
    for q, r in st.session_state["chat"]:
     st.markdown(f"🧑‍💻 **You:** {q}")
     st.markdown(f"🤖 **Bot:** {r}")
     st.markdown("---") 


    # Insights
    st.subheader("📊 Insights")
    top_product = df.loc[df["price"].idxmax()]
    st.success(f"Best Product: {top_product['product']} (₹{top_product['price']})")

    # Graph
    st.subheader("📊 Visualization")

    chart_type = st.selectbox("Choose Chart", ["Bar", "Line", "Pie"])

    fig, ax = plt.subplots(figsize=(4,2.5))

    if chart_type == "Bar":
       ax.bar(df["product"], df["price"])
    elif chart_type == "Line":
       ax.plot(df["product"], df["price"])
    elif chart_type == "Pie":
       ax.pie(df["price"], labels=df["product"], autopct="%1.1f%%")

    st.pyplot(fig)
    st.subheader("📈 Simple Prediction")

    X = np.array(range(len(df))).reshape(-1,1)
    y = df["price"].values

    model = LinearRegression()
    model.fit(X, y)

    future = np.array([[len(df)+1]])
    prediction = model.predict(future)

    st.write(f"Next predicted value: {round(prediction[0],2)}")

    st.markdown("---")
    st.markdown("👨‍💻 Developed by Vardhini | AI Chatbot Project")