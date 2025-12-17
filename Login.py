import streamlit as st
import time
from app.services.user_service import register_user, login_user

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# ---------- Initialise session state ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("Get Started")

# If already logged in
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard", type="secondary", use_container_width=True):  # Optional: add stretch here too
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary", use_container_width=True):  # Optional: add stretch here too
        if not login_username or not login_password:
            st.warning("Please enter both username and password.")
        else:
            success, message = login_user(login_username, login_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(message)
                st.balloons()
                time.sleep(2)  # pause so balloons are visible
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error(message)

# ----- REGISTER TAB -----
with tab_register:
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account", use_container_width=True):  # Optional: add stretch here too
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = register_user(new_username, new_password)
            if success:
                st.success(message)
                st.info("Tip: go to the Login tab and sign in with your new account.")
                st.toast("Account created successfully!")  # subtle popup
            else:
                st.error(message)