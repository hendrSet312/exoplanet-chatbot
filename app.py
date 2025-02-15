import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_choice" not in st.session_state:
    st.session_state.selected_choice = None

if "api_key" not in st.session_state:
    st.session_state.api_key = ''

if "response_mode" not in st.session_state:
    st.session_state.response_mode = None

if "tone" not in st.session_state:
    st.session_state.tone = None

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = [1]

def homepage():
    st.title('Halo 👋, selamat datang di ExoExplorer')
    
    st.text(""" ExoExplorer adalah website berbasis AI yang dapat memprediksi peluang planet luar tata surya yang dapat ditinggali menggunakan machine learning.Selain itu, website ini bisa menjelaskan hasil prediksi yang dibuat dengan bantuan SHAP dan generative AI. 
            """)

page = st.navigation([st.Page(homepage, title = '🏠 Homepage'),st.Page('pred_page.py',title = '📊 prediction'), st.Page('chatbot_page.py',title = '🤖 Chatbot')])
page.run()


