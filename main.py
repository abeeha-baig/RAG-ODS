import streamlit as st
from utils.pdf_processing import load_and_process_pdfs
from utils.embeddings import get_embeddings, compute_similarity_score
from utils.retrieval import process_query
from utils.conversation import start_conversation
from utils.history import load_chat_history, save_chat_history
from web_template import get_templates, get_css
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from utils.helpers import load_web_templates, initialize_session_state
from langchain_community.llms import OpenAI

bot_template, user_template = get_templates()
css = get_css()

PDF_PATHS = [
    'Documents/database-security-guide.pdf',
    'Documents/advanced-security-guide.pdf',
    'Documents/enterprise-user-security-administrators-guide.pdf'
]

PDF_SOURCES = {
    'database-security-guide.pdf': 'https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/database-security-guide.pdf',
    'advanced-security-guide.pdf': 'https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/advanced-security-guide.pdf',
    'enterprise-user-security-administrators-guide.pdf': 'https://docs.oracle.com/en/database/oracle/oracle-database/21/dbimi/enterprise-user-security-administrators-guide.pdf'
}

def display_chat_history(bot_template, user_template):
    """
    Display the chat history in the sidebar.
    """
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if "role" not in message or "content" not in message:
                st.sidebar.error(f"Malformed message: {message}")
                continue
            if message["role"] == "user":
                st.sidebar.markdown(user_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
            elif message["role"] == "bot":
                st.sidebar.markdown(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)

def main():
    """
Main function to set up and run the Streamlit app for Oracle Database Security Q/A.

This function initializes the web interface using Streamlit, loads the necessary templates and session state, 
processes PDF documents to create vector embeddings, sets up a conversational retrieval chain, and handles user input.
It uses the OpenAI API for generating responses based on user queries and maintains the chat history.

Steps:
1. Sets up the Streamlit page configuration, including title and layout.
2. Retrieves the OpenAI API key from Streamlit secrets for secure access.
3. Loads web templates for displaying the chat interface and styles.
4. Initializes session state variables to manage conversation state and chat history.
5. Checks if the retriever and conversation state are set; if not, processes the PDF documents to create vector embeddings.
6. Initializes the conversational retrieval chain using the vector embeddings and memory buffer.
7. Stores the sources and chat history in the session state.
8. Displays the chat history in the sidebar.
9. Provides an input field for user queries and a button to submit the query.
10. Handles the query processing and response generation using the OpenAI API.
11. Displays the response along with the source metadata (if available) and updates the chat history.
12. Saves the updated chat history to maintain state between interactions.

Note: This function requires the OpenAI API key to be set up in Streamlit secrets.

Returns:
    None
"""
     
    st.set_page_config(page_title="Oracle Database Security Q/A", page_icon=":books:", layout="wide")

    openai_api_key = st.secrets["OPENAI_API_KEY"]

    bot_template, user_template, css = load_web_templates()
    st.write(css, unsafe_allow_html=True)
    st.sidebar.header("Chat History")

    initialize_session_state()

    if "retriever" not in st.session_state or st.session_state.conversation is None:
        chunk_source_pairs = load_and_process_pdfs(PDF_PATHS, PDF_SOURCES)
        if chunk_source_pairs:
            vector_embeddings, sources = get_embeddings(chunk_source_pairs, openai_api_key=openai_api_key)
            
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            
            llm = OpenAI(api_key=openai_api_key)
            
            retriever = vector_embeddings.as_retriever()
            
            st.session_state.retriever = retriever
            
            st.session_state.conversation = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                memory=memory
            )

            st.session_state.sources = sources
            st.session_state.chat_history = load_chat_history()
            st.success("Model initialized successfully!")
        else:
            st.error("No chunks found. Ensure PDFs are processed correctly.")

    display_chat_history(bot_template, user_template)

    query_text = st.text_input("Enter your query:")

    if st.button("Submit"):
        if query_text:
            embedding_module = OpenAIEmbeddings(openai_api_key=openai_api_key)

            response, source_metadata = process_query(query_text)

            st.session_state.chat_history.append({"role": "user", "content": query_text})
            st.session_state.chat_history.append({"role": "bot", "content": response["answer"]})

            if source_metadata:
                st.markdown(bot_template.replace("{{MSG}}", f"{response['answer']}"), unsafe_allow_html=True)
            else:
                st.markdown(bot_template.replace("{{MSG}}", response["answer"]), unsafe_allow_html=True)

            save_chat_history(st.session_state.chat_history)
        else:
            st.error("Please enter a query.")

if __name__ == "__main__":
    main()
