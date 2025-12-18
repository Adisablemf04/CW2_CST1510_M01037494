# pages/5_AI_Assistant.py
import streamlit as st
from app.services.gemini_service import get_response, stream_response
from app.data.users import get_user_by_username

# ---------- AUTH GUARD ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first to access the AI Assistant.")
    st.stop()

# Get user role from DB
user_record = get_user_by_username(st.session_state.username)
user_role = user_record[3] if user_record else "user"  # role column

st.set_page_config(page_title="Gemini AI Assistant", page_icon="🤖", layout="wide")
st.title(f"Gemini AI Assistant — Welcome {st.session_state.username}")
st.caption("Powered by Gemini API")

# ---------- Domain prompts ----------
domain_prompts = {
    "General": "You are a helpful assistant.",
    "Cybersecurity": "You are a cybersecurity expert. Provide technical analysis and actionable recommendations.",
    "Datasets": "You are a data analyst. Help interpret datasets and suggest insights.",
    "Tickets": "You are an IT assistant. Help manage and troubleshoot support tickets."
}

intro_messages = {
    "General": f"👋 Hi {st.session_state.username}, I’m your assistant for general tasks ({user_role}).",
    "Cybersecurity": f"🔐 Hi {st.session_state.username}, I’m your assistant for cybersecurity incidents and analysis ({user_role}).",
    "Datasets": f"📊 Hi {st.session_state.username}, I’m your assistant for dataset exploration and insights ({user_role}).",
    "Tickets": f"🎫 Hi {st.session_state.username}, I’m your assistant for ticket management and troubleshooting ({user_role})."
}

# ---------- Sidebar controls ----------
with st.sidebar:
    st.subheader("Chat Controls")

    # Domain selector
    domain = st.selectbox(
        "Choose assistant domain",
        ["General", "Cybersecurity", "Datasets", "Tickets"],
        index=0
    )

    # Clear button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- Initialize or refresh chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# If domain changed, reset with new intro
if not st.session_state.messages or st.session_state.get("current_domain") != domain:
    system_prompt = domain_prompts.get(domain, "You are a helpful assistant.")
    intro_message = intro_messages.get(domain, f"👋 Hi {st.session_state.username}, I’m your assistant.")
    st.session_state.messages = [
        {"role": "user", "content": system_prompt},
        {"role": "assistant", "content": intro_message}
    ]
    st.session_state.current_domain = domain

# ---------- Display history (skip system prompt) ----------
for m in st.session_state.messages:
    if m["content"] in domain_prompts.values():
        continue
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------- Chat input ----------
prompt = st.chat_input("Ask me something...")
if prompt:
    # Show user bubble
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Streaming Gemini response with domain + role
    with st.chat_message("assistant"):
        container = st.empty()
        full_text = ""
        for chunk in stream_response(st.session_state.messages, domain=domain, user_role=user_role):
            full_text += chunk
            container.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})