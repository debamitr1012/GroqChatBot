import streamlit as st
import os
from groq import Groq
import random
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
def main():
    groq_api_key = os.environ['GROQ_API_KEY']
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')
    st.title("Chat with Groq!")
    st.write("Hello! I'm your friendly Groq chatbot. I can help answer your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!")
    st.sidebar.title('Customization')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )
    conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)
    memory=ConversationBufferWindowMemory(k=conversational_memory_length)
    user_question = st.text_input("Ask a question:")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )
    conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
    )
    if user_question:
        response = conversation(user_question)
        message = {'human':user_question,'AI':response['response']}
        st.session_state.chat_history.append(message)
        st.write("Chatbot:", response['response'])
if __name__ == "__main__":
    main()
