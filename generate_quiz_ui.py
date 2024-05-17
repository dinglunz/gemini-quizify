import streamlit as st
import os
import sys
import json
sys.path.append(os.path.abspath('D:\_DEV\Github Repos\RadicalX\gemini-quizify'))
from doc_ingestion import DocumentProcessor
from embedding_client import EmbeddingClient
from data_pipeline import ChromaCollectionCreator
from quiz_generator_algorithm import QuizGenerator

class QuizManager:

    def __init__(self, questions: list):
        self.questions = questions
        self.total_questions = len(questions)

    def get_question_at_index(self, index: int):
        # Ensure index is always within bounds using modulo arithmetic
        valid_index = index % self.total_questions
        return self.questions[valid_index]

    def next_question_index(self, direction=1):
        if "question_index" not in st.session_state:
            st.session_state["question_index"] = 0
        
        current_index = st.session_state["question_index"]
        new_index = (current_index + direction) % self.total_questions
        st.session_state["question_index"] = new_index

# Test Generating the Quiz
if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "gemini-quizify-422618",
        "location": "us-west1"
    }
    
    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        processor.ingest_documents()
    
        embed_client = EmbeddingClient(**embed_config) 
    
        chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
        question = None
        question_bank = None
    
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                chroma_creator.create_chroma_collection()
                
                st.write(topic_input)
                
                # Test the Quiz Generator
                generator = QuizGenerator(topic_input, questions, chroma_creator.db)
                question_bank = generator.generate_quiz()

    if question_bank:
        screen.empty()
        with screen.container():
            st.header("Generated Quiz Questions: ")
            
            quiz_manager = QuizManager(question_bank)
            
            # Ensure session state is initialized
            if "question_index" not in st.session_state:
                st.session_state["question_index"] = 0

            # Display the question and choices
            with st.form("Multiple Choice Question"):
                index_question = quiz_manager.get_question_at_index(st.session_state["question_index"])
                
                # Unpack choices for radio
                choices = [f"{choice['key']}) {choice['value']}" for choice in index_question['choices']]
                
                st.write(index_question['question'])
                
                answer = st.radio(
                    'Choose the correct answer',
                    choices
                )
                
                if st.form_submit_button("Submit"):
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key):
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")
                