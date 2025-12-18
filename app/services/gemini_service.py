import streamlit as st
import google.generativeai as genai
from app.services.data_loader import get_domain_context

# Configure Gemini with your API key from secrets.toml
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Choose a model (flash = faster, pro = deeper)
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

def _convert_role(role: str) -> str:
    """Convert Streamlit roles to Gemini roles."""
    return "model" if role == "assistant" else "user"

def get_response(messages):
    """
    Non-streaming Gemini response.
    messages: list of {"role": "user"|"assistant", "content": "..."}
    """
    history = [{"role": _convert_role(m["role"]), "parts": [m["content"]]} for m in messages]
    chat = model.start_chat(history=history)
    latest_user = messages[-1]["content"]
    resp = chat.send_message(latest_user)
    return resp.text

def stream_response(messages, domain="General", user_role="user"):
    """
    Streaming Gemini response generator with domain + role context injection.
    """
    # Convert existing messages into Gemini history
    history = [{"role": _convert_role(m["role"]), "parts": [m["content"]]} for m in messages]

    # Inject domain context if not General
    if domain != "General":
        context = get_domain_context(domain)
        history.append({
            "role": "user",
            "parts": [f"User role: {user_role}\nHere is domain context from the database:\n{context}"]
        })

    chat = model.start_chat(history=history)
    latest_user = messages[-1]["content"]

    for chunk in chat.send_message(latest_user, stream=True):
        if hasattr(chunk, "text") and chunk.text:
            yield chunk.text