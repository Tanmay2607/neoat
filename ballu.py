# --- 1. Imports ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
import re
import os
# --- 2. Helper: Extract code from LLM ---
def extract_python_code(response_text):
    match = re.search(r"```(?:python)?(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text

# --- 3. OpenRouter LLM call ---
# --- 3. OpenRouter LLM call ---
def call_llm_with_openrouter(prompt, api_key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://ko4t3cifhed5jwykr8efcb.streamlit.app",
            "X-Title": "NeoAT Excel Assistant"
        }
    )
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful data analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# --- 4. Schema + Normalization ---
def normalize_column_names(df):
    return df.rename(columns=lambda col: ''.join(e for e in col.strip().lower().replace(' ', '_') if e.isalnum() or e == '_'))

def get_data_schema(df):
    return ", ".join([f"{col} ({df[col].dtype})" for col in df.columns])

def generate_llm_prompt(query, schema):
    return f"""
You are an expert data analyst. You are given a user query and the schema of a pandas DataFrame named 'df'.
Your task is to generate a Python script to answer the query.

**Data Schema:**
{schema}

**User Query:**
"{query}"

**Instructions:**
1. Generate only executable Python code that uses the 'df' DataFrame.
2. Do NOT include explanations or text outside the code block.
3. The code must calculate the answer and store it in a variable named 'result'.
4. If the query requires a visualization (e.g., "bar chart", "histogram"), generate valid code to create the plot using matplotlib.
5. Assume 'df' is already loaded.
""".strip()

def execute_generated_code(code, df):
    local_scope = {'df': df, 'pd': pd, 'plt': plt}
    try:
        exec(code, {}, local_scope)
        result = local_scope.get("result", None)

        # If result is a Series of countries, return count and names
        if isinstance(result, pd.Series) and result.dtype == object:
            return f"Count: {len(result)}\nCountries:\n" + "\n".join(result.astype(str))

        return result if result is not None else "✅ Code executed (e.g., chart displayed)."

    except Exception as e:
        return f"❌ Error executing code: {e}"


# --- 5. Streamlit App ---
st.set_page_config(page_title="NeoAT Excel Assistant", layout="centered")
st.title("Tanmay's Excel Sheet Analyzer")
st.markdown("Ask questions like:\n- *‘Count countries with lower rank than Syria’*\n- *‘Plot bar chart of top 5 by score’*")

api_key = st.secrets["openai_api_key"]
uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])
query = st.text_input("❓ Ask a question about your data")

if uploaded_file and api_key and query:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        df = normalize_column_names(df)
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        schema = get_data_schema(df)
        prompt = generate_llm_prompt(query, schema)
        with st.spinner("🤖 Thinking..."):
            response = call_llm_with_openrouter(prompt, api_key)
            code = extract_python_code(response)

        st.subheader("🧾 Generated Python Code")
        st.code(code, language="python")

        st.subheader("💡 Answer / Chart")
        result = execute_generated_code(code, df)
        if isinstance(result, (pd.Series, pd.DataFrame)):
            st.write(result)
        elif result is not None:
            st.write(result)

    except Exception as e:
        st.error(f"❌ Failed to process: {e}")
