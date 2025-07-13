


🧠 Knowledge Bot - RAG-powered Document Chatbot

A powerful document-based chatbot that lets you upload PDFs and images and ask natural language questions, powered by LangChain, Ollama, ChromaDB, and served using FastAPI + Streamlit.

📂 Features

✅ Upload multiple PDF and image files


✅ Extract and split content using LangChain


✅ Embed with Ollama Embeddings (nomic-embed-text)


✅ Store and retrieve chunks using ChromaDB


✅ Answer queries using ChatOllama (gemma:2b or any model)


✅ Frontend in Streamlit

✅ Backend in FastAPI

🛠️ Project Structure

knowledge-bot/

├── backend/
|
│   ├── main.py # FastAPI backend entrypoint
│   
|    ├── rag_pipeline.py       # RAG pipeline logic
│   
|    ├── config.py             # CORS setup
│   
    └── uploaded_files/       # Directory where files are stored

├── frontend/
|      
│  └── app.py                # Streamlit UI
|
└── README.md

🧑‍💻 How It Works

1. You upload PDF or image files.
2. The backend:
   - Extracts and splits content.
   - Embeds chunks using Ollama embeddings.
   - Stores them in ChromaDB vector store.
3. When you ask a question:
   - It retrieves relevant chunks.
   - Generates an answer using ChatOllama.
   - Returns the answer to the frontend.

💻 How to Run This in PyCharm (Step-by-Step)

1. Clone or create the project in PyCharm and organize files as shown above.

2. Create and activate virtual environment:
   python -m venv .venv
   source .venv/bin/activate   (Windows: .venv\Scripts\activate)

3. Install dependencies:
   pip install fastapi uvicorn streamlit langchain langchain-community langchain-core langchain-ollama langchain-chroma unstructured python-multipart pillow

4. Make sure Ollama and models are ready:
   ollama run gemma:2b
   ollama run nomic-embed-text

5. Run the backend:
   cd backend
   uvicorn main:app --reload

6. Run the frontend:
   cd frontend
   streamlit run app.py

7. Upload files and ask questions through the browser UI.

🔍 Example Files to Test
Upload any of your own PDFs or images. For example:
- contract.pdf
- invoice.jpg
🧠 Model & RAG Details

Model: gemma:2b via Ollama
Embedding Model: nomic-embed-text
Retriever: Chroma vector store
Prompt: System + user input template

🚧 TODO (Future Enhancements)

- Conversational memory (chat history)
- File deduplication
- Multilingual support
- Authentication
- Upload status bar

🧾 License
This project is for educational and research purposes.
🙋 Need Help?
Feel free to raise issues or reach out with errors or feature requests.
