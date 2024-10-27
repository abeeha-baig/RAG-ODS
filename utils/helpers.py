import streamlit as st
from web_template import get_templates, get_css

def load_web_templates():
    bot_template, user_template = get_templates()
    css = get_css()
    return bot_template, user_template, css

def initialize_session_state():
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_chat_id" not in st.session_state:
        st.session_state.selected_chat_id = None

def display_chat_history(bot_template, user_template):
    """
    Display the chat history in the sidebar.
    """
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if "role" not in message or "content" not in message:
                continue  # Skip malformed messages
            if message["role"] == "user":
                st.sidebar.write(user_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
            elif message["role"] == "bot":
                st.sidebar.write(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)

