## rag-streamlit-bot
A Retrieval-Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and OpenAI. Upload documents, index them into a vector store, and chat contextually with your data.

### Features
- Document upload & indexing – process local files into searchable chunks

- Semantic retrieval – embed and query content via LangChain + OpenAI embeddings

- Chat UI – interactive conversation using Streamlit’s chat components

- Session memory – maintains chat history within each session

### Quickstart
1. Clone the repo
```
git clone https://github.com/abeeha-baig/RAG-ODS.git
cd RAG-ODS

```
2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

```
3. Install dependencies
```
pip install -r requirements.txt

```
4. Configure Secrets
Add your OpenAI API key to ```.streamlit/secrets.toml```:
```
OPENAI_API_KEY = "sk-your-openai-key-here"

```
5. Run the app
```
python -m streamlit run main.py

```
### Project Structure
```

├── Documents
│   ├── advanced-security-guide.pdf
│   ├── database-security-guide.pdf
│   └── enterprise-user-security-administrators-guide.pdf
├── README.md
├── chat_history.json
├── db
│   └── chroma.sqlite3
├── main.py
├── requirements.txt
├── templates
│   ├── bot.jpg
│   ├── human.jpg
│   └── pdf_icon.png
├── utils
│   ├── chunking.py
│   ├── conversation.py
│   ├── embeddings.py
│   ├── helpers.py
│   ├── history.py
│   ├── pdf_processing.py
│   └── retrieval.py
└── web_template.py

```

### How It Works

1. Upload documents via Streamlit.

2. LangChain splits and embeds content, storing it in a vector store.

3. User messages trigger semantic document search.

4. Context + prompt sent to OpenAI for generating chat responses.


### Enhancements

- Swap vector store: e.g., FAISS, Chroma, Pinecone.

- Add support for PDFs, DOCX, Web URLs.

- Improve performance: caching, chunking strategies, embedding batch requests.