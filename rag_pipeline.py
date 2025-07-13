from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader

from typing import List
import os

class RAGPipeline:
    def __init__(self, directory_path: str = "uploaded_files", model_name: str = "gemma:2b"):
        self.directory_path = directory_path
        self.model_name = model_name
        self.chain = None
        self._setup_pipeline()

    @staticmethod
    def load_documents_from_directory(directory_path: str) -> List[Document]:
        all_documents = []
        for filename in os.listdir(directory_path):
            path = os.path.join(directory_path, filename)
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(path)
                all_documents.extend(loader.load())
            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                loader = UnstructuredImageLoader(path)
                all_documents.extend(loader.load())
        return all_documents

    def _setup_pipeline(self):
        docs = self.load_documents_from_directory(self.directory_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(chunks, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer based only on the context below.\n\n{context}"),
            ("human", "{input}")
        ])

        llm = ChatOllama(model=self.model_name, temperature=0)
        qa_chain = create_stuff_documents_chain(llm, prompt)
        self.chain = create_retrieval_chain(retriever, qa_chain)

    def ask(self, query: str) -> str:
        if self.chain is None:
            return "❌ RAGPipeline not initialized."
        result = self.chain.invoke({"input": query})
        answer = result.get("answer", "")
        if not answer or "i don't know" in answer.lower():
            return "❌ I couldn’t find that information in the provided documents."
        return answer
