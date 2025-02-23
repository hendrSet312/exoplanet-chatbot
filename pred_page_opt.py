import streamlit as st
import pandas as pd
from backend.prediction import modelling

planet_data = pd.read_csv('backend/database/database.csv')

if 'selected_option' not in st.session_state:
    st.session_state.planet_data = None

def option_1():
    planet_names = planet_data['P_NAME'].to_list() 
    selection_planet = st.selectbox('pilih planet yang diinginkan',planet_names)

    if st.button('Mulai prediksi') :  
        filtered_data = planet_data[
            planet_data['P_NAME'] == selection_planet
        ].iloc[0]

        data_input = modelling(data_parameter={col:filtered_data[col] for col in filtered_data.index})
        prediction = data_input.predicting_data()

        st.session_state['prediction'] = prediction
        st.switch_page('chatbot_page.py')

def option_2():
    st.text('Masukkan mengenai informasi planet yang diprediksi')

    with st.expander("🌍 Parameter Fisik Planet"):
        P_ESI = st.number_input("🌎 Indeks Kemiripan Bumi (ESI)", 0.0, 1.0)
        P_SEMI_MAJOR_AXIS = st.number_input("📏 Sumbu Semi-Mayor (AU)", min_value=0.0)
        P_PERIOD = st.number_input("⏳ Periode Orbit (hari)", min_value=0.0)
        P_ECCENTRICITY = st.number_input("🔄 Eksentrisitas Orbit", min_value=0.0, max_value=1.0)
        P_FLUX = st.number_input("☀️ Flux Radiasi", min_value=0.0)
        P_RADIUS = st.number_input("🪐 Radius Planet", min_value=0.0)
        P_MASS = st.number_input("⚖️ Massa Planet", min_value=0.0)
        P_DENSITY = st.number_input("🔬 Densitas Planet (g/cm³)", min_value=0.0)
        P_GRAVITY = st.number_input("🌌 Gravitasi Permukaan (m/s²)", min_value=0.0)


    with st.expander("🌡️ Parameter Suhu"):

        st.text('🌞 Suhu Kesetimbangan', help="""Suhu sebuah planet jika tidak memiliki atmosfer, dihitung berdasarkan keseimbangan antara panas yang diterima dari bintangnya dan panas yang dilepaskan kembali ke luar angkasa. """)

        P_TEMP_EQUIL_MIN = st.number_input("❄️ Minimum (K)", 0, 3500, key='temp_equil_min')
        P_TEMP_EQUIL_MAX = st.number_input("🔥 Maksimum (K)", 0, 3500, key='temp_equil_max')

        st.text('🌎 Suhu Permukaan', help="""Suhu permukaan planet yang dapat dipengaruhi oleh atmosfer dan faktor internal lainnya.""")

        P_TEMP_SURF_MIN = st.number_input("❄️ Minimum (K)", 0, 3500, key='temp_surf_min')
        P_TEMP_SURF_MAX = st.number_input("🔥 Maksimum (K)", 0, 3500, key='temp_surf_max')


    with st.expander("⭐ Parameter Bintang Induk"):
        S_TEMPERATURE = st.number_input("🔥 Suhu Bintang Induk (K)", 0, 10000)
        S_LUMINOSITY = st.number_input("💡 Luminositas Bintang (L☉)", min_value=0.0)
        S_TYPE_TEMP = st.selectbox("🌟 Tipe Spektral berdasarkan Temperatur", ['F', 'G', 'K', 'M','A'])
        S_TIDAL_LOCK = st.number_input("🔄 Terkunci Pasang Surut (Tidal Locking)", min_value=0.0, max_value=1.0)
        
    if st.button('Mulai prediksi'):
        data_params = {
            'P_ESI': P_ESI,
            'P_SEMI_MAJOR_AXIS': P_SEMI_MAJOR_AXIS,
            'P_PERIOD' : P_PERIOD,
            'P_ECCENTRICITY':P_ECCENTRICITY,
            'P_FLUX': P_FLUX,
            'P_RADIUS':P_RADIUS,
            'P_MASS':P_MASS,
            'P_DENSITY':P_DENSITY,
            'P_GRAVITY':P_GRAVITY,
            'P_TEMP_EQUIL_MIN':P_TEMP_EQUIL_MIN,
            'P_TEMP_EQUIL_MAX':P_TEMP_EQUIL_MAX,
            'P_TEMP_SURF_MIN':P_TEMP_SURF_MIN,
            'P_TEMP_SURF_MAX':P_TEMP_SURF_MAX,
            'S_TEMPERATURE':S_TEMPERATURE,
            'S_LUMINOSITY':S_LUMINOSITY,
            'S_TYPE_TEMP':S_TYPE_TEMP,
            'S_TIDAL_LOCK':S_TIDAL_LOCK
        }

        data_input = modelling(data_parameter=data_params)
        prediction = data_input.predicting_data()

        st.session_state['prediction'] = prediction
        st.switch_page('chatbot_page.py')

    

with st.container():
    st.subheader('Masukkan data untuk prediksi')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Pilih planet dari database'):
            st.session_state['selected_option'] = 'database'
    with col2:
        if st.button('Buat data planet sendiri'):
            st.session_state['selected_option'] = 'custom'

    if 'selected_option' in st.session_state:
        if st.session_state.selected_option == 'database':
            option_1()
        elif st.session_state.selected_option == 'custom':
            option_2()
                
        
    
        

    








    


