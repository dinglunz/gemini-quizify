# Quizify

Quizify is an interactive quiz builder application built using Streamlit and LangChain. It allows users to upload PDF documents, extract content, generate quiz questions based on a specified topic, and navigate through the generated quiz interactively.

## Features

- **PDF Document Ingestion**: Upload multiple PDF files and extract their content.
- **Quiz Generation**: Generate quiz questions based on a specified topic and extracted content.
- **Interactive Quiz**: Navigate through the quiz questions, submit answers, and receive feedback.

## Project Structure

- `doc_ingestion.py`: Handles PDF document ingestion and content extraction.
- `embedding_client.py`: Embedding client configuration for Google Cloud's VertexAI.
- `data_pipeline.py`: Creates a Chroma collection from the extracted content.
- `quiz_generator_algorithm.py`: Generates quiz questions using the specified topic and content.
- `generate_quiz_ui.py`: Manages the quiz questions and navigation.
- `quizify.py`: Main application script to run the Streamlit interface.

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/dinglunz/gemini-quizify.git
    cd gemini-quizify
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit application**:

    ```sh
    streamlit run quizify.py
    ```

2. **Upload PDF files**: Use the file uploader in the interface to upload PDF documents for ingestion.

3. **Specify Quiz Topic and Number of Questions**: Enter the topic for the quiz and select the number of questions to generate.

4. **Generate Quiz**: Click the "Submit" button to generate quiz questions based on the uploaded content and specified topic.

5. **Navigate through the Quiz**: Use the "Next Question" and "Previous Question" buttons to navigate through the generated quiz questions. Submit your answers and receive feedback.

## Dependencies

The project dependencies are listed in the `requirements.txt` file. Some of the key dependencies include:

- `streamlit`: For building the interactive web application.
- `langchain`: For handling document processing, embedding, and quiz generation.
- `google-cloud`: For integrating with Google Cloud's VertexAI.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [LangChain](https://langchain.com/)
- [Google Cloud VertexAI](https://cloud.google.com/vertex-ai)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

Happy Quizzing!
