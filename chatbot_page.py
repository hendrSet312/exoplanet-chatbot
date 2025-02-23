import streamlit as st
from langchain.schema import HumanMessage,BaseMessage,AIMessage
from backend.groq import *

st.set_page_config(layout="wide")

def update_conversation(role, content, input_context=None, output_context=None):
    st.session_state.messages.append({"role": role, "content": content})

def process_chat(user_input):
    with st.spinner("Berpikir..."):
        chat_history = [('human' if msg['role'] == "human" else 'ai', msg['content']) for msg in st.session_state.messages]

        retrieved_document = st.session_state.Retriever['history_aware'].invoke({
            "chat_history": chat_history,
            "input": "user_input"
        })

        answer = st.session_state.Chatbot.generate_answer(
            retriever_result = retrieved_document,
            tone = st.session_state.tone,
            question = user_input
        )

        with message_container.chat_message("user"):
            st.markdown(user_input)

        update_conversation("user", user_input)
        update_conversation("assistant", answer, user_input, answer)

        with message_container.chat_message("assistant"):
            st.markdown(answer)


with st.expander('🛠️ Pengaturan'):
    api_key = st.text_input('API Key (Groq) : ',help = 'API key untuk chatbot, dapatkan API key https://console.groq.com/keys')
    tone = st.pills('🗣️ Gaya bahasa',
                    ['Normal','Teknikal'], 
                    help = 'Normal : untuk umum atau belum teralu paham astronomi dan sains \n\n Teknikal : untuk orang ahli di astronomi, mahasiswa, peneliti atau astronot')

    if st.button("Simpan"):
        st.session_state.api_key = api_key
        st.session_state.tone = tone
        st.session_state.ShapInterpreter = ShapInterpreter(st.session_state['api_key'])
        st.session_state.Chatbot = chatbot(st.session_state['api_key'])



with st.container():
    if st.session_state.prediction != None : 
        cols1, cols2 = st.columns(2)
        with cols1 :
            st.subheader('📊 SHAP Graph Explanation')
            with st.spinner('Menghasilkan penjelasan...'):
                if st.session_state.ShapResult == None and st.session_state.ShapInterpreter: 
                    interpret_result = st.session_state.ShapInterpreter.generate_insight(st.session_state['prediction'],st.session_state['tone'])
                    st.session_state.ShapResult = interpret_result

                if st.session_state.ShapResult : 
                    with st.container(height = 400):
                        st.image(st.session_state.prediction['image'])
                        st.write(st.session_state.ShapResult)


        with cols2  : 
            st.subheader('🤖 Chatbot Assistant')
            with st.container():
                if len(st.session_state.api_key.strip()) < 1 and len(st.session_state.tone.strip()) < 1:
                    st.error('Tolong atur API key dan gaya bicara yang ada inginkan terlebih dahulu lewat pengaturan')
                else : 

                    st.session_state.Retriever['base']  = st.session_state.Chatbot.create_retrieval(
                            st.session_state.prediction,
                            st.session_state.ShapResult
                    )

                    st.session_state.Retriever['history_aware']  = st.session_state.Chatbot.generate_aware_history(
                        st.session_state.Retriever['base']
                    )
                    
                    message_container  = st.container(height = 400, border=True)

                    for message in st.session_state.messages:
                        with message_container.chat_message(message["role"]):
                            st.markdown(message["content"])

                    with st.container(border=True):
                        if prompt := st.chat_input("Tanyakan sesuatu..."):
                            process_chat(prompt)

    else : 
        st.error('Tolong buat prediksi terlebih dahulu')
                    