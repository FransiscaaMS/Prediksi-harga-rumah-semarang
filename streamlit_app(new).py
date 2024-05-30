import pickle
import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO
import os
import tempfile
import numpy as np

# Load model from a zip file
filename = 'prediksi_harga_rumah_smg.zip'
with zipfile.ZipFile(filename, 'r') as zip_ref:
    file_list = zip_ref.namelist()
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_ref.extractall(temp_dir)
        for file_name in file_list:
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, 'rb') as f:
                model_RF = pickle.load(f)

# Membuat sidebar
test = st.sidebar.radio("Menu", ["Beranda", "Data", "Labelling", "Prediksi", "Kontak"])

# Halaman Beranda
if test == "Beranda":
    st.header("Halo semuanya selamat datang :wave:")
    st.markdown("#### Ini merupakan website yang dapat memprediksi harga rumah di Kota Semarang sesuai dengan kriteria yang diinginkan oleh calon pembeli.")
    st.image('Poster Peta Kota Semarang.png')
    st.markdown("#### Dengan adanya website ini, diharapkan dapat membantu para calon pembeli dalam menentukan harga rumah yang sesuai dan memenuhi kriteria rumah impiannya.")
    st.markdown("#### Selamat mencoba!")

# Halaman Data
if test == "Data":
    st.header("Data Bersih")
    st.write("Berikut merupakan data yang digunakan dalam prediksi harga rumah di Kota Semarang.") 
    data = pd.read_csv("df_cleaning.csv")
    st.write(data)
    st.write("Sumber Data : Rumah123.com (Kota Semarang) per Maret 2024")

# Halaman Labelling
if test == "Labelling":
    st.subheader("Labelling")
    st.markdown("##### Untuk variabel 'Jenis Rumah' dan 'Lokasi' merupakan variabel kategorik sehingga harus dikonversi kedalam variabel numerik agar dapat di prediksi")
    st.markdown("###### Variabel jenis rumah")
    st.text("0 = jenis rumah biasa")
    st.text("1 = jenis rumah featured")
    st.text("2 = jenis rumah premier")
    st.markdown("###### Variabel lokasi")
    st.text("0 = Banyumanik, Semarang")
    st.text("1 = Candisari, Semarang")
    st.text("2 = Gajah Mungkur, Semarang")
    st.text("3 = Gayamsari, Semarang")
    st.text("4 = Genuk, Semarang")
    st.text("5 = Gunung Pati, Semarang")
    st.text("6 = Mijen, Semarang")
    st.text("7 = Ngaliyan, Semarang")
    st.text("8 = Pedurungan, Semarang")
    st.text("9 = Semarang Barat, Semarang")
    st.text("10 = Semarang Selatan, Semarang")
    st.text("11 = Semarang Tengah, Semarang")
    st.text("12 = Semarang Timur, Semarang")
    st.text("13 = Semarang Utara, Semarang")
    st.text("14 = Tembalang, Semarang")
    st.text("15 = Tugu, Semarang")
    st.text("16 = Semarang lainnya")

# Fungsi prediksi harga
def predict_house_price(Jenis_Rumah, Lokasi, KT, KM, Garasi, LT, LB):
    # Memasukkan data
    input_data = [[Jenis_Rumah, Lokasi, KT, KM, Garasi, LT, LB]]
    # Konversi list ke array numpy
    input_data_array = np.array(input_data)
    # Lakukan prediksi menggunakan model RandomForestRegressor
    prediction = model_RF.predict(input_data_array)
    # Konversi prediksi ke dalam bentuk miliar rupiah
    prediction_in_billions = prediction * 1_000_000_000
    # Membulatkan hasil prediksi dengan menghapus bagian desimal
    prediction_rounded = int(prediction_in_billions[0])
    # Format hasil prediksi dengan pemisah ribuan dan tambah "Rp."
    prediction_formatted = f"Rp. {prediction_rounded:,}".replace(",", ".")
    return prediction_formatted

# Halaman Prediksi
if test == "Prediksi":
    st.subheader("Prediksi harga rumah di Kota Semarang")
    
    # Membuat kolom prediksi
    col1, col2 = st.columns(2)

    with col1:
        Jenis_Rumah = st.selectbox("Jenis Rumah", [0, 1, 2])
    with col2:
        Lokasi = st.selectbox("Lokasi", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    with col1:
        KT = st.number_input('Input Jumlah Kamar Tidur (min=1)')
    with col2:
        KM = st.number_input('Input Jumlah Kamar Mandi (min=1)')
    with col1:
        Garasi = st.number_input('Input Garasi (menampung berapa mobil) (min=1)')
    with col2:
        LT = st.number_input('Input Luas Tanah (m2) (min=28)')
    with col1:
        LB = st.number_input('Input Luas Bangunan (m2) (min=29)')

    predict = ''

    if st.button("Prediksi Harga Rumah (miliar)"):
        predict = predict_house_price(Jenis_Rumah, Lokasi, KT, KM, Garasi, LT, LB)
        st.markdown(f"Prediksi harga rumah sesuai dengan kriteria di Kota Semarang:<br><h2>{predict}</h2>", unsafe_allow_html=True)

# Halaman Kontak
if test == "Kontak":
    st.subheader("Hai, mari terhubung! :wave:")
    st.write("Nama     : Fransisca Mulya Sari")
    st.write("LinkedIn : https://www.linkedin.com/in/fransisca-mulya-sari-a51853260/")
    st.write("Github   : https://github.com/FransiscaaMS")
    st.write("Email    : fransiscaams@gmail.com")

