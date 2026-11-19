from dataclasses import dataclass
import os

from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None

def get_settings() -> Settings:
    """Load the API key from Streamlit Cloud secrets or a local .env file."""
    load_dotenv()
    secret_key = None
    try:
        import streamlit as st
        secret_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        # No secrets.toml is expected during local development.
        pass
    return Settings(openai_api_key=secret_key or os.getenv("OPENAI_API_KEY"))
