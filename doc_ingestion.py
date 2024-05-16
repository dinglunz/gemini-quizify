import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import os
import tempfile
import uuid

class DocumentProcessor:
    def __init__(self):
        self.pages = []  # List to keep track of pages from all documents

    def ingest_documents(self):
        # Step 1: Render a file uploader widget
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )

        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                # Generate a unique identifier to append to the file's original name
                unique_id = uuid.uuid4().hex
                original_name, file_extension = os.path.splitext(uploaded_file.name)
                temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)

                # Write the uploaded PDF to a temporary file
                with open(temp_file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())

                # Step 2: Process the temporary file using PyPDFLoader
                pdf_loader = PyPDFLoader(temp_file_path)
                pages = pdf_loader.load()  # Load the document and get the pages

                # Add the extracted pages to the 'pages' list
                self.pages.extend(pages)

                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)

            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents()
