import json
import os

CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """
    Load chat history from a JSON file.
    """
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            history = json.load(file)
        if isinstance(history, list):
            return history
        else:
            return []
    else:
        return []

def save_chat_history(chat_history):
    """
    Save the chat history to a JSON file.
    """
    if isinstance(chat_history, list):
        with open(CHAT_HISTORY_FILE, "w") as file:
            json.dump(chat_history, file)