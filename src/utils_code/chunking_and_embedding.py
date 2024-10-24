
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os

def chunking_and_loading_vectorDB(content , EmbedModel, vectordb_name):
    """using recursive char splitter"""

    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.create_documents([content])
    chunck_list = text_splitter.split_documents(texts)

    if os.path.exists(f"./chroma_db/{vectordb_name}"):
        vector_store = Chroma(persist_directory=f"./chroma_db/{vectordb_name}", embedding_function=EmbedModel)

    else:
        vector_store = Chroma.from_documents(chunck_list, EmbedModel, persist_directory=f"./chroma_db/{vectordb_name}")

    return vector_store

