from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import streamlit as st

GREETINGS = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
HATE_SPEECH_LIST = ["bitch", "bastard", "fuck"]

def check_greetings(query_text):
    """
    Check if the query is a common greeting.
    """
    return any(greeting in query_text.lower() for greeting in GREETINGS)

def contains_hate_speech(query_text):
    """
    Check if the query contains hate speech.
    """
    return any(hate_speech in query_text.lower() for hate_speech in HATE_SPEECH_LIST)

def process_query(query_text):
    """
    Process a user query using the RAG model and update chat history.

    Args:
        query_text (str): The query text.

    Returns:
        response (dict): The response to the query.
        source_metadata (str): Metadata for the source.
    """
    if "conversation" not in st.session_state or st.session_state.conversation is None:
        st.error("RAG model is not initialized. Please upload and process the PDF first.")
        return

    if check_greetings(query_text):
        response = {"answer": "Hello! Please ask a relevant question related to database security."}
        return response, None

    if contains_hate_speech(query_text):
        response = {"answer": "Please use appropriate language."}
        return response, None

    response = st.session_state.conversation({"question": query_text})

    if "i don't know" in response["answer"].lower() or "irrelevant" in response["answer"].lower():
        response["answer"] = "This query is not related to the database security domain. Please ask a relevant question."
        return response, None

    source_metadata = "Source not available"
    if "source_documents" in response and response["source_documents"]:
        source_urls = []
        for doc in response["source_documents"]:
            source_url = doc.metadata.get("source", "Source not available")
            source_urls.append(f"Source: {source_url}")
        source_metadata = "\n".join(set(source_urls)) if source_urls else source_metadata

    return response, source_metadata