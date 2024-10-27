from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st

openai_api_key = st.secrets["OPENAI_API_KEY"]

prompt_template = """
You are an Oracle Database expert AI assistant. Please answer the following question in a detailed, step-by-step manner. If applicable, provide a numbered list of steps. Make sure your response is complete, and if you start listing steps, include all necessary steps until the end. If you cannot complete the response, indicate that clearly.

Question: {question}

Answer:
"""

prompt = PromptTemplate.from_template(prompt_template)

def start_conversation(vector_embeddings):
    """
    Initialize and return a conversational retrieval chain using vector embeddings for document retrieval.
    
    This function sets up a conversation with memory using a language model (LLM) and a retriever based on 
    the vector embeddings. The conversation is powered by an LLM (OpenAI) that answers user queries in a 
    conversational style. The vector store retriever, built from the provided vector embeddings, enables the 
    model to retrieve relevant information based on the user's input. The conversation memory is used to 
    maintain context across multiple interactions, providing more coherent and context-aware responses.

    Args:
        vector_embeddings (Chroma): The vector store containing document embeddings for retrieval.

    Returns:
        conversation (ConversationalRetrievalChain): An initialized conversation chain with memory for interactive Q&A.
    """
    llm = OpenAI(api_key=openai_api_key)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_embeddings.as_retriever(),
        memory=memory,
        prompt=prompt  # Use the custom prompt template
    )
    return conversation
