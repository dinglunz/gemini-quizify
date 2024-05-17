import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('D:\_DEV\Github Repos\RadicalX\gemini-quizify'))
from doc_ingestion import DocumentProcessor
from embedding_client import EmbeddingClient


# Import Task libraries
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class SimpleDocument:
    def __init__(self, text, metadata={}):
        self.page_content = text
        self.metadata = metadata


class ChromaCollectionCreator:
    def __init__(self, processor, embed_model):
        self.processor = processor      # This will hold the DocumentProcessor from Task 3
        self.embed_model = embed_model  # This will hold the EmbeddingClient from Task 4
        self.db = None                  # This will hold the Chroma collection
    
    def create_chroma_collection(self):
        
        # Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        # Split documents into text chunks
        text_splitter = CharacterTextSplitter(separator=" ", chunk_size=500, chunk_overlap=100)
        document_objects = []
        for document in self.processor.pages:
            page_text = document.text if hasattr(document, 'text') else str(document)
            chunks = text_splitter.split_text(page_text)
            for chunk in chunks:
                document_objects.append(SimpleDocument(chunk))

        if document_objects:
            st.success(f"Successfully split pages into {len(document_objects)} documents.", icon="✅")

        # Initialize an empty Chroma collection
        try:
            self.db = Chroma(
                collection_name="DocumentCollection",
                embedding_function=self.embed_model
            )
        except Exception as e:
            st.error(f"Failed to initialize Chroma Collection: {str(e)}", icon="🚨")
            return

        try:
            self.db.add_documents(document_objects)
            st.success("Successfully created Chroma Collection!", icon="✅")
        except Exception as e:
            st.error(f"Failed to create Chroma Collection: {str(e)}", icon="🚨")

    def query_chroma_collection(self, query) -> Document:
        if self.db:
            docs = self.db.similarity_search_with_relevance_scores(query)
            if docs:
                return docs[0]
            else:
                st.error("No matching documents found!", icon="🚨")
        else:
            st.error("Chroma Collection has not been created!", icon="🚨")

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents()
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "gemini-quizify-422618",
        "location": "us-west1"
    }
    
    embed_client = EmbeddingClient(**embed_config)
    print(type(embed_client))
    
    chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
    with st.form("Load Data to Chroma"):
        st.write("Select PDFs for Ingestion, then click Submit")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            chroma_creator.create_chroma_collection()
