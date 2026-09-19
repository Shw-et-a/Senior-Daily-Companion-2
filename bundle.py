import re

with open('translations.py', 'r', encoding='utf-8') as f:
    t_lines = f.read()

with open('modules/tasks.py', 'r', encoding='utf-8') as f:
    tk_lines = f.read()

with open('modules/voice.py', 'r', encoding='utf-8') as f:
    v_lines = f.read()

with open('modules/ai_engine.py', 'r', encoding='utf-8') as f:
    ai_lines = f.read()

with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    app_lines = f.read()

header = '''"""
Senior Daily Companion — Main Application
A Gen AI-powered, senior-first daily companion website.
"""

import os
import json
import re
from datetime import datetime
import pytz
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

load_dotenv()
'''

# Clean translations docstring
t_clean = re.sub(r'^"""[\s\S]*?"""', '', t_lines).strip()

# Clean tasks docstring
tk_clean = re.sub(r'^"""[\s\S]*?"""', '', tk_lines).strip()

# Clean voice imports and docstring
v_clean = re.sub(r'^"""[\s\S]*?"""', '', v_lines)
v_clean = re.sub(r'import streamlit\.components\.v1 as components', '', v_clean).strip()

# Clean ai_engine imports and docstring
ai_clean = re.sub(r'^"""[\s\S]*?"""', '', ai_lines)
ai_clean = re.sub(r'import os\b', '', ai_clean)
ai_clean = re.sub(r'import json\b', '', ai_clean)
ai_clean = re.sub(r'import re\b', '', ai_clean)
ai_clean = re.sub(r'from dotenv import load_dotenv\b', '', ai_clean)
ai_clean = re.sub(r'from google import genai\b', '', ai_clean)
ai_clean = re.sub(r'from google\.genai import types\b', '', ai_clean)
ai_clean = re.sub(r'load_dotenv\(\)', '', ai_clean)

# Upgrade _get_client to check st.secrets too
old_get_client = """def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GOOGLE_API_KEY not found. Please create a .env file with your key. "
                "See .env.example for instructions."
            )
        _client = genai.Client(api_key=api_key)
    return _client"""

new_get_client = """def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            try:
                if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
                    api_key = st.secrets["GOOGLE_API_KEY"]
            except Exception:
                pass
        if not api_key:
            raise EnvironmentError(
                "GOOGLE_API_KEY not found. Please add GOOGLE_API_KEY to your .env file or Streamlit Cloud Secrets."
            )
        _client = genai.Client(api_key=api_key)
    return _client"""

if old_get_client in ai_clean:
    ai_clean = ai_clean.replace(old_get_client, new_get_client)
else:
    print("Warning: old_get_client not found directly in ai_clean")

ai_clean = ai_clean.strip()

# Clean app lines
app_clean = re.sub(r'^"""[\s\S]*?"""', '', app_lines).strip()
app_clean = re.sub(r'from modules\.ai_engine[^\n]+', '', app_clean)
app_clean = re.sub(r'from modules\.tasks[^\n]+', '', app_clean)
app_clean = re.sub(r'from modules\.voice[^\n]+', '', app_clean)
app_clean = re.sub(r'from translations[^\n]+', '', app_clean)
app_clean = re.sub(r'import streamlit as st', '', app_clean)
app_clean = re.sub(r'import streamlit\.components\.v1 as components', '', app_clean)
app_clean = re.sub(r'from datetime import datetime', '', app_clean)
app_clean = re.sub(r'import pytz', '', app_clean)
app_clean = app_clean.strip()

final_bundle = f"{header}\n\n# {'='*60}\n# TRANSLATIONS\n# {'='*60}\n{t_clean}\n\n# {'='*60}\n# TASKS\n# {'='*60}\n{tk_clean}\n\n# {'='*60}\n# VOICE HELPERS\n# {'='*60}\n{v_clean}\n\n# {'='*60}\n# AI ENGINE\n# {'='*60}\n{ai_clean}\n\n# {'='*60}\n# MAIN STREAMLIT APP\n# {'='*60}\n{app_clean}\n"

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(final_bundle)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(final_bundle)

print("SUCCESS: app.py and streamlit_app.py created as complete standalone single-file apps!")
