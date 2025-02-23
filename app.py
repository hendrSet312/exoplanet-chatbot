import streamlit as st
import pandas as pd

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": 'Halo! berdasarkan penjelasan analisa kami, apakah ada yang ingin ditanyakan ?'}]

if "api_key" not in st.session_state:
    st.session_state.api_key = ''

if "tone" not in st.session_state:
    st.session_state.tone = None

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

if 'ShapInterpreter' not in st.session_state:
    st.session_state.ShapInterpreter = None

if 'ShapResult' not in st.session_state:
    st.session_state.ShapResult = None

if 'Chatbot' not in st.session_state:
    st.session_state.Chatbot = None 

if 'Retriever' not in st.session_state : 
    st.session_state.Retriever = {'base':None, 'history_aware':None} 

def homepage():
    st.image('media/image/logo/logo.jpeg')
    st.title('🚀✨ Selamat Datang di ExoExplorer ✨🚀')
    
    st.markdown("""
    ### 🌌 **Jelajahi Misteri Alam Semesta** 🌌
    
    **ExoExplorer** adalah platform berbasis kecerdasan buatan (AI) yang membawa Anda dalam perjalanan eksplorasi planet-planet di luar tata surya. Temukan dunia baru dan ketahui peluang planet-planet tersebut untuk dapat dihuni dengan bantuan **machine learning**.

    🔍 **Apa yang Membuat Kami Spesial?**
    - **Prediksi Kehidupan di Luar Bumi**: Model AI canggih kami menganalisis data untuk memperkirakan kemungkinan planet yang layak huni.
    - 💡 **Penjelasan Hasil yang Transparan**: Dapatkan wawasan mendalam dari prediksi melalui analisis **SHAP**, yang mengungkap faktor-faktor utama yang mempengaruhi kelayakhunian.
    - 🤖 **Chatbot Cerdas**: Diskusikan hasil prediksi dan topik terkait astronomi dengan AI generatif kami, kapan saja!

    🛠️ **Ayo Mulai Eksplorasi dan Temukan Dunia Baru Bersama ExoExplorer!**
    """)

    if st.button('🚀 Mulai prediksi'):
        st.switch_page('pred_page_opt.py')


page = st.navigation([
    st.Page(homepage, title='🏠 Beranda'),
    st.Page('pred_page_opt.py', title='📊 Prediksi Kelayakhunian'),
    st.Page('chatbot_page.py', title='🤖 Chatbot Interaktif')
])

page.run()


