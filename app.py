import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Talking Rabbitt AI", page_icon="🐰", layout="wide")

st.title("🐰 Talking Rabbitt AI")
st.subheader("Talk to your business data")

st.write(
    "Upload a CSV dataset and ask questions about your business performance."
)

# -----------------------------
# OpenAI Client
# -----------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

df = None

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.write("### Dataset Preview")
    st.dataframe(df)

    st.write("### Dataset Columns")
    st.write(list(df.columns))


# -----------------------------
# Question Input
# -----------------------------
question = st.text_input("Ask a question about your data")

# -----------------------------
# AI Answer
# -----------------------------
if question and df is not None:

    schema = df.dtypes.to_string()

    prompt = f"""
You are a business data analyst.

Dataset schema:
{schema}

User Question:
{question}

Provide a clear business answer in 2-3 sentences.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        st.write("## 📊 AI Insight")
        st.success(answer)

    except Exception as e:
        st.error(f"AI response failed: {e}")


# -----------------------------
# Automatic Visualization
# -----------------------------
if df is not None:

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    if len(numeric_cols) > 0 and len(categorical_cols) > 0:

        st.write("## 📈 Automatic Data Visualization")

        x_col = categorical_cols[0]
        y_col = numeric_cols[0]

        chart_data = df.groupby(x_col)[y_col].sum().reset_index()

        fig = px.bar(
            chart_data,
            x=x_col,
            y=y_col,
            title=f"{y_col} by {x_col}",
            color=x_col
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("Upload a dataset with categorical and numeric columns to generate charts.")