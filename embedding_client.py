# embedding_client.py

from langchain_google_vertexai import VertexAIEmbeddings

class EmbeddingClient:

    def __init__(self, model_name, project, location):
        # Initialize the VertexAIEmbeddings client with the given parameters
        self.client = VertexAIEmbeddings(
            model=model_name,
            project=project,
            location=location
        )
        
    def embed_query(self, query):
        vectors = self.client.embed_query(query)
        return vectors
    
    def embed_documents(self, documents):
        try:
            return self.client.embed_documents(documents)
        except AttributeError:
            print("Method embed_documents not defined for the client.")
            return None

if __name__ == "__main__":
    model_name = "textembedding-gecko@003"
    project = "gemini-quizify-422618"
    location = "us-west1"

    embedding_client = EmbeddingClient(model_name, project, location)
    vectors = embedding_client.embed_query("Hello World!")
    if vectors:
        print(vectors)
        print("Successfully used the embedding client!")
