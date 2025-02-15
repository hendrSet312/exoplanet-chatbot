import streamlit as st

def generate_choices():
    # Define your choices
    choices = [
        "Apa arti hasil prediksi ini?",
        "Bagaimana kondisi lingkungan planet ini?",
    ]
    
    # Create columns for the choices
    st.text('Pertanyaan cepat :')
    cols = st.columns(2,vertical_alignment='center')
    selected_choice = None
    
    # Display choices in grid layout
    for i, choice in enumerate(choices):
        col_idx = i % 2
        with cols[col_idx]:
            if st.button(choice, key=f"choice_{i}", use_container_width=True):
                selected_choice = choice
                st.session_state[f"choice_{i}_selected"] = False
    
    return selected_choice

def process_chat(user_input):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with message_container.chat_message("user"):
        st.markdown(user_input)

    response = user_input
    st.session_state.messages.append({"role": "assistant", "content": response})
    with message_container.chat_message("assistant"):
        st.markdown(response)

    if 'selected_choice' in st.session_state:
        del st.session_state['selected_choice']
    
    st.rerun()

with st.container():
    if len(st.session_state.prediction) > 0 : 
        with st.popover('🛠️ Pengaturan'):

            api_key = st.text_input('API Key (Groq) : ',help = 'API key untuk chatbot, dapatkan API key https://console.groq.com/keys')
            tone = st.pills('🗣️ Gaya bahasa',
                            ['Normal','Teknikal'], 
                            help = 'Normal : untuk umum atau belum teralu paham astronomi dan sains \n\n Teknikal : untuk orang ahli di astronomi, mahasiswa, peneliti atau astronot')
            
            response_mode = st.pills(
                "🔊 Pilih mode respon",
                ["Teks saja", "Suara & Teks"],
                help="Teks saja: Chatbot merespons dengan teks.\n\n Suara & Teks: Chatbot berbicara sambil menampilkan teks."
            )

            if st.button("Simpan"):
                st.session_state.api_key = api_key
                st.session_state.response_mode = response_mode
                st.session_state.tone = tone
        
        if len(st.session_state.api_key.strip()) < 1:
            st.error('Tolong atur API key terlebih dahulu lewat pengaturan')
        else : 
            message_container  = st.container(height = 400, border=True)

            for message in st.session_state.messages:
                with message_container.chat_message(message["role"]):
                    st.markdown(message["content"])

            with st.container(border=True):
                selected_choice = generate_choices()
                if selected_choice:
                    process_chat(selected_choice)
                # Manual input from user
                if prompt := st.chat_input("Tanyakan sesuatu..."):
                    process_chat(prompt)

    else : 
        st.error('Tolong buat prediksi terlebih dahulu')
                    