import streamlit as st
from langchain.memory import ConversationBufferMemory

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": 'Halo! berdasarkan penjelasan analisa kami, apakah ada yang ingin ditanyakan ?'}]

if "api_key" not in st.session_state:
    st.session_state.api_key = ''

if "tone" not in st.session_state:
    st.session_state.tone = None

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = []

if 'ShapInterpreter' not in st.session_state:
    st.session_state.ShapInterpreter = None

if 'ShapResult' not in st.session_state:
    st.session_state.ShapResult = None

if 'Chatbot' not in st.session_state:
    st.session_state.Chatbot = None 

if 'Retriever' not in st.session_state : 
    st.session_state.Retriever = {'base':None, 'history_aware':None} 

def homepage():
    st.title('Halo 👋, selamat datang di ExoExplorer')
    
    st.text(""" ExoExplorer adalah website berbasis AI yang dapat memprediksi peluang planet luar tata surya yang dapat ditinggali menggunakan machine learning.Selain itu, website ini bisa menjelaskan hasil prediksi yang dibuat dengan bantuan SHAP dan generative AI. 
            """)

page = st.navigation([st.Page(homepage, title = '🏠 Homepage'),st.Page('pred_page.py',title = '📊 prediction'), st.Page('chatbot_page.py',title = '🤖 Chatbot')])
page.run()


