"""
Senior Daily Companion — Vercel & Python Compatibility Entrypoint
For Streamlit local run: use `streamlit run streamlit_app.py`
"""

def handler(request=None, *args, **kwargs):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "Senior Daily Companion is active."
    }

app = handler
application = handler
