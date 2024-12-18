import streamlit as st
from utils import process_user_question
import os
from dotenv import load_dotenv

# Streamlit app title
st.title("Database Q&A Chat")

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and processing
if user_question := st.chat_input("Ask a question about the database:"):
    # Append user's question to session state
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate response using process_user_question
    with st.chat_message("assistant"):
        st.write("Thinking...")
        response = process_user_question(
            db_uri= os.getenv("MYSQL_URI"),
            question=user_question
        )
        st.markdown(response)

    # Append assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})