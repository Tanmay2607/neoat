# --- 2. Import libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import io
from google.colab import files
import getpass
from openai import OpenAI

# --- 3. Set up OpenRouter API Key ---
openrouter_api_key = getpass.getpass("Enter your OpenRouter API Key: ")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key)

# --- 4. Helper: Clean LLM code output ---
def extract_python_code(response_text):
    import re

    # Extract the first ```python ... ``` block (or ``` ... ```)
    match = re.search(r"```(?:python)?(.*?)```", response_text, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        # Fallback: remove common non-code explanations
        lines = response_text.splitlines()
        code_lines = []
        for line in lines:
            if line.strip().startswith("#") or "import " in line or "df[" in line or "result =" in line or "plt." in line:
                code_lines.append(line)
        code = "\n".join(code_lines)

    return code.strip()

# --- 5. LLM Call via OpenRouter ---
def call_llm_with_openrouter(prompt):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful data analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- 6. DataFrame Helpers ---
def normalize_column_names(df):
    normalized_columns = {}
    for col in df.columns:
        new_col = col.strip().lower().replace(' ', '_')
        new_col = ''.join(e for e in new_col if e.isalnum() or e == '_')
        normalized_columns[col] = new_col
    df = df.rename(columns=normalized_columns)
    return df

def get_data_schema(df):
    schema = [f"{col} ({df[col].dtype})" for col in df.columns]
    return ", ".join(schema)

def generate_llm_prompt(query, schema):
    prompt = f"""
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
"""
    return prompt.strip()

def execute_generated_code(code, df):
    local_scope = {'df': df, 'pd': pd, 'plt': plt}
    try:
        exec(code, {}, local_scope)
        result = local_scope.get('result', None)
        if result is not None:
            return result
        else:
            return "✅ Code executed successfully (e.g., chart displayed)."
    except Exception as e:
        return f"❌ Error executing code: {e}"


# --- 7. Main Execution ---
print("\n📁 Please upload your Excel file:")
uploaded = files.upload()

if not uploaded:
    print("\n⚠️ No file uploaded. Please run the cell again.")
else:
    filename = next(iter(uploaded))
    print(f"\n📄 Processing '{filename}'...")

    try:
        df = pd.read_excel(io.BytesIO(uploaded[filename]), engine='openpyxl')
        df = normalize_column_names(df)
        print("\n✅ Data loaded successfully. Here's a preview:")
        display(df.head())

        query = input("\n❓ Please ask a question about your data: ")

        if query:
            schema = get_data_schema(df)
            prompt = generate_llm_prompt(query, schema)

            print("\n🤖 Thinking...")
            raw_response = call_llm_with_openrouter(prompt)
            generated_code = extract_python_code(raw_response)

            print("\n🧾 Generated Python code:\n")
            print(generated_code)

            print("\n💡 Here's the answer:")
            result = execute_generated_code(generated_code, df)

            if isinstance(result, (pd.DataFrame, pd.Series)):
                display(result)
            else:
                print(result)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
