from langchain_community.embeddings import OpenAIEmbeddings
import numpy as np
import os
import uuid
import chromadb
from chromadb import Client
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
import streamlit as st

# openai_api_key = st.secrets["OPENAI_API_KEY"]

def compute_similarity_score(query_embedding, chunk_embedding):
    """
    Compute the cosine similarity score between the query embedding and a chunk embedding.
    """
    return np.dot(query_embedding, chunk_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding))

def get_embeddings(chunk_metadata_pairs, openai_api_key):
    """
    Generate and return embeddings for the text chunks, storing metadata for each chunk.

    Args:
        chunk_metadata_pairs (list): List of tuples containing text chunks and metadata.
        openai_api_key (str): The API key for OpenAI.
        
    Returns:
        vectordb: A vector database with embeddings.
        sources (list): List of metadata associated with each text chunk.
    """
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    texts = [chunk for chunk, _ in chunk_metadata_pairs]
    sources = [{"source": source} for _, source in chunk_metadata_pairs]  # Include source in metadata

    filtered_sources = [{key: value for key, value in metadata.items() if isinstance(value, (str, int, float))} for metadata in sources]

    persist_directory = 'db'

    if os.path.exists(persist_directory):
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    else:
        vectordb = Chroma.from_texts(texts=texts, embedding=embedding, persist_directory=persist_directory, metadatas=filtered_sources)
        vectordb.persist()
    
    return vectordb, filtered_sources
@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=60))
def embed_with_retry(embedding, texts):
    """
    Embed the texts with a retry mechanism to handle rate limits.

    Args:
        embedding (OpenAIEmbeddings): The embedding module.
        texts (list): The list of texts to embed.

    Returns:
        list: List of embeddings for the texts.
    """
    return embedding.embed_documents(texts)