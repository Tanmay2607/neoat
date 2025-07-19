# 📊 Tanmay's Excel Sheet Analyzer

A Streamlit-powered conversational assistant that lets you query Excel files using natural language and get instant analysis or visualizations.

---

## 🚀 Features

- **Upload Excel files** (`.xlsx`)  
- **Natural language queries**, like “count countries with total > 100”  
- **Dynamic Python code generation**  OpenRouter / Mistral LLM  
- **Visual slides**: bar charts, histograms, etc., can display in Streamlit  
- **Smart normalization**: case-insensitive and punctuation-agnostic matching  
- **Safe execution**: handles DataFrame, Series, scalar outputs 

---

## 🛠️ Installation

 1. Clone the repo:
   ```bash
   git clone https://github.com/Tanmay2607/neoat.git
   cd neoat
   ```
 2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## ⚙️ Setup
1. Sign up at OpenRouter.ai and obtain your API key.
2. Add the key to Streamlit secrets:
   In ~/.streamlit/secrets.toml (locally) or via the Streamlit Cloud UI:
   ```
   openai_api_key = "YOUR_OPENROUTER_API_KEY"
   
## ▶️ Run the App
```bash
streamlit run app.py
```
##🚧 Limitations
1. Requires a valid OpenRouter (Mistral) API key
2. Best suited for Excel files with numeric and text-based columns
3. Complex queries may need clear formulation
4. LLM response time may vary depending on model/load

