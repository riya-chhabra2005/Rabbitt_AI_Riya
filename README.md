# 1. Clone repository
git clone https://github.com/riya-chhabra2005/Rabbitt_AI_Riya.git
cd Rabbitt_AI_Riya

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create Streamlit secrets folder
mkdir .streamlit

# 6. Create secrets file
echo GROQ_API_KEY="YOUR_GROQ_API_KEY" > .streamlit/secrets.toml

# 7. Run the application
streamlit run app.py
