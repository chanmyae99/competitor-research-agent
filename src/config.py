import os
from dotenv import load_dotenv

try:
    import streamlit as st
except ImportError:
    st = None

load_dotenv()


def get_secret(key: str):
    """
    Get configuration value from:
    1. Streamlit secrets (deployment)
    2. Environment variables (.env)
    """

    if st is not None:
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass

    return os.getenv(key)


OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
SERPER_API_KEY = get_secret("SERPER_API_KEY")