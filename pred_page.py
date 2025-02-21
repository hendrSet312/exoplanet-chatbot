import streamlit as st
import pandas as pd
from backend.prediction import modelling

st.text('Masukkan mengenai informasi planet yang diprediksi')

with st.expander("🌍 Parameter Fisik Planet"):
    p_detection = st.selectbox("🔭 Metode Deteksi Planet", [
        'Transit',
        'Radial Velocity',
        'Orbital Brightness Modulation'
    ])
    p_type = st.selectbox("🪐 Tipe Planet", [
        'Neptunian','Terran','Superterran','Jovian','Subterran','Miniterran'
    ])

    p_esi = st.number_input("🌎 Indeks Kemiripan Bumi (ESI)",0.0,1.0)
    p_periastron = st.number_input("📏 Jarak Pericenter (Periastron) (AU)", min_value=0.0)
    p_semi_major = st.number_input("📏 Sumbu Semi-Mayor (AU)", min_value=0.0)
    p_distance_eff = st.number_input("📡 Jarak Efektif (juta km)", 0, 1000)
    p_distance = st.number_input("🚀 Jarak dari Bumi (tahun cahaya)", min_value=0.0)
    p_period = st.number_input("⏳ Periode Orbit (hari)", min_value=0.0)
    p_apastron = st.number_input("📏 Jarak Apocenter (Apastron) (AU)", min_value=0.0)
    p_abio_zone = st.number_input('🧪 Batas luar zona bintang abiogenesis (AU)', min_value=0.0)

with st.expander("🌡️ Parameter Suhu"):

    st.text('🌞 Suhu Kesetimbangan', help="""Suhu sebuah planet jika tidak memiliki atmosfer, dihitung berdasarkan keseimbangan antara panas yang diterima dari bintangnya dan panas yang dilepaskan kembali ke luar angkasa. """)

    p_temp_equil_min = st.number_input("❄️ Minimum (K)", 0, 3500, key='temp_equil_min')
    p_temp_equil_max = st.number_input("🔥 Maksimum (K)", 0, 3500, key='temp_equil_max')

    st.text('🌎 Suhu Permukaan', help="""Suhu permukaan planet yang dapat dipengaruhi oleh atmosfer dan faktor internal lainnya.""")

    p_temp_surf_min = st.number_input("❄️ Minimum (K)", 0, 3500, key='temp_surf_min')
    p_temp_surf_max = st.number_input("🔥 Maksimum (K)", 0, 3500, key='temp_surf_max')


if st.button('Prediksi'):
    data_params = {
        'P_ESI': p_esi,
        'P_PERIASTRON':p_periastron,
        'P_SEMI_MAJOR_AXIS': p_semi_major,
        'P_DISTANCE_EFF':p_distance_eff,
        'P_DISTANCE' : p_distance,
        'P_PERIOD' : p_period,
        'P_APASTRON' : 	p_apastron,
        'P_TEMP_SURF_MIN' : p_temp_surf_min,
        'P_TEMP_EQUIL_MIN' : p_temp_equil_min,
        'P_TEMP_SURF_MAX' : p_temp_surf_max,
        'P_TEMP_EQUIL_MAX' : p_temp_surf_max,
        'P_TYPE' : p_type,
        'P_DETECTION' : p_detection,
        'S_ABIO_ZONE' : p_abio_zone
    }

    data_input = modelling(data_parameter=data_params)
    prediction = data_input.predicting_data()

    st.session_state['prediction'] = prediction

    st.switch_page('chatbot_page.py')








    


