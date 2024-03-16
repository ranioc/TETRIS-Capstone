import pickle
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca Model
regression_model = pickle.load(open('regression_model.sav', 'rb'))

# Judul Web
st.title('Harga Rumah dan Karakteristik Properti di Provinsi DKI Jakarta')

# Teks Pembuka
welcome_text = """
Selamat datang di Dashboard "Harga Rumah dan Karakteristik Properti di Provinsi DKI Jakarta"! Melalui visualisasi interaktif yang disajikan, Anda dapat menjelajahi tren harga properti dan karakteristik properti di berbagai kota dan kecamatan di DKI Jakarta, hingga mencoba fitur prediksi harga rumah berdasarkan karakteristik tertentu. Dengan menggunakan model regresi linear, Anda dapat menginputkan variabel-variabel seperti luas bangunan, luas tanah, jumlah kamar tidur, dan lainnya untuk memperoleh estimasi harga properti. Selamat mengeksplorasi!
"""

st.write(f'<div style="text-align: justify">{welcome_text}</div>', unsafe_allow_html=True)

st.markdown("---")

visualisasi, prediksi, about = st.tabs(['Visualisasi Data', 'Prediksi Harga Rumah', 'Author'])

with visualisasi:
    # Header analisis data harga jual rumah
    st.header("Visualisasi Data")
    st.markdown("---")

    # Load data
    df = pd.read_csv('rumah_jakarta_clean.csv')

    # Analisis Level Kota
    # Visualisasi: Banyaknya rumah yang dijual di masing-masing kota
    st.subheader('Banyaknya Rumah yang Dijual di Masing-Masing Kota')
    city_count_chart = alt.Chart(df).mark_bar().encode(
        x='count():N',
        y=alt.Y('Kota:N', title='Kota'),
        tooltip=['count():N']
    ).properties(width=600)
    st.altair_chart(city_count_chart, use_container_width=True)
    st.write('<div style="text-align: justify">Jakarta Selatan merupakan kota dengan jumlah rumah dijual terbanyak, sedangkan Jakarta Utara adalah yang paling sedikit. Hal ini mungkin disebabkan karena tingginya permintaan rumah di Jakarta Selatan yang disebabkan oleh terpusatnya pertumbuhan ekonomi di wilayah tersebut yang dapat diindikasikan oleh banyaknya pengembang properti di daerah ini.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Visualisasi: Distribusi Luas Tanah
        st.subheader('Distribusi Luas Tanah')
        land_area_distribution_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Luas Tanah:Q', bin=True),
            y='count():N',
            tooltip=['count():N']
        ).properties(width=600)
        st.altair_chart(land_area_distribution_chart, use_container_width=True)

    with col2:   
        # Visualisasi: Distribusi Luas Bangunan
        st.subheader('Distribusi Luas Bangunan')
        building_area_distribution_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Luas Bangunan:Q', bin=True),
            y='count():N',
            tooltip=['count():N']
        ).properties(width=600)
        st.altair_chart(building_area_distribution_chart, use_container_width=True)

    st.write('<div style="text-align: justify">Rumah berukuran kecil adalah rumah yang paling banyak dijual. Hal ini juga menandakan segmentasi pasar di DKI Jakarta yang masih didominasi kalangan menengah, hingga menengah ke bawah.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)

    with col3:
        # Visualisasi: Distribusi Kamar Tidur
        st.subheader('Distribusi Kamar Tidur')
        bed_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Kamar Tidur:N', title='Kamar Tidur'),
            y='count():Q',
            color='Kamar Tidur:N',
            tooltip=['count():Q']
        ).properties(width=600)
        st.altair_chart(bed_chart, use_container_width=True)

    with col4:
        # Visualisasi: Distribusi Kamar Mandi
        st.subheader('Distribusi Kamar Mandi')
        bath_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Kamar Mandi:N', title='Kamar Mandi'),
            y='count():Q',
            color='Kamar Mandi:N',
            tooltip=['count():Q']
        ).properties(width=600)
        st.altair_chart(bath_chart, use_container_width=True)

    st.write('<div style="text-align: justify">Rumah dengan 2 Kamar Mandi dan 3 Kamar Tidur merupakan rumah yang paling banyak dijual. Hal ini dapat menandakan bahwa minat pasar yang banyak tertuju pada rumah dengan 3 Kamar TIdur dan 2 Kamar Mandi</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    #Analisis Level Kecamatan
    
    # Visualisasi: Banyaknya rumah yang dijual di tiap kecamatan
    st.subheader('Banyaknya Rumah yang Dijual di Tiap Kecamatan')
    kecamatan_count_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('count():N', title='Jumlah Rumah'),
        y=alt.Y('Kecamatan:N', title='Kecamatan', sort='-x'),
        tooltip=['count():N']
    ).properties(width=600)
    st.altair_chart(kecamatan_count_chart, use_container_width=True)
    st.write('<div style="text-align: justify">Kecamatan Duren Sawit merupakan kecamatan dengan rumah yang paling banyak dijual, disusul oleh Kelapa Gading. Dalam hal ini, kemungkinan pada daerah tersebut banyak pengembang properti.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        # Visualisasi: Top 5 Kecamatan dengan Harga Rata-Rata Tertinggi
        st.subheader('Top 5 Kecamatan dengan Harga Rumah Rata-Rata Tertinggi')
        top5_expensive_chart = alt.Chart(df.groupby('Kecamatan')['Harga'].mean().sort_values(ascending=False).head(5).reset_index()).mark_bar().encode(
            x='Harga:Q',
            y=alt.Y('Kecamatan:N', sort='-x', title='Kecamatan'),
            tooltip=['Harga:Q']
        ).properties(width=600)
        st.altair_chart(top5_expensive_chart, use_container_width=True)
        st.write('<div style="text-align: justify">Kecamatan pada grafik tersebut dapat menandakan kawasan elite yang biasanya dihuni oleh orang-orang dengan pendapatan tinggi karena rata-rata harga rumah pada daerah tersebut adalah yang paling mahal.</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with col6:
        # Visualisasi: Top 5 Kecamatan dengan Harga Rata-Rata Terendah
        st.subheader('Top 5 Kecamatan dengan Harga Rumah Rata-Rata Terendah')
        top5_cheap_chart = alt.Chart(df.groupby('Kecamatan')['Harga'].mean().sort_values().head(5).reset_index()).mark_bar().encode(
            x='Harga:Q',
            y=alt.Y('Kecamatan:N', title='Kecamatan'),
            tooltip=['Harga:Q']
        ).properties(width=600)
        st.altair_chart(top5_cheap_chart, use_container_width=True)
        st.write('<div style="text-align: justify">Pada grafik ini, dapat disimpulkan bahwa kecamatan Ciracas, Jagakarsa, Kalideres, Pasar Rebo, dan Tanjung Barat merupakan kecamatan yang berada di daerah pinggiran Provinsi DKI Jakarta yang agak jauh dari pusat kota, sehingga rata-rata harga rumahnya paling rendah dibandingkan kecamatan lain.</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


    col7, col8 = st.columns(2)

    with col7:
        # Visualisasi: Top 5 Kecamatan dengan Luas Bangunan Terbesar
        st.subheader('Top 5 Kecamatan dengan Luas Bangunan Terbesar')
        top5_large_chart = alt.Chart(df.groupby('Kecamatan')['Luas Bangunan'].mean().sort_values(ascending=False).head(5).reset_index()).mark_bar().encode(
            x='Luas Bangunan:Q',
            y=alt.Y('Kecamatan:N', sort='-x', title='Kecamatan'),
            tooltip=['Luas Bangunan:Q']
        ).properties(width=600)
        st.altair_chart(top5_large_chart, use_container_width=True)

    with col8:
        # Visualisasi: Top 5 Kecamatan dengan Luas Bangunan Terkecil
        st.subheader('Top 5 Kecamatan dengan Luas Bangunan Terkecil')
        top5_small_chart = alt.Chart(df.groupby('Kecamatan')['Luas Bangunan'].mean().sort_values().head(5).reset_index()).mark_bar().encode(
            x='Luas Bangunan:Q',
            y=alt.Y('Kecamatan:N', title='Kecamatan'),
            tooltip=['Luas Bangunan:Q']
        ).properties(width=600)
        st.altair_chart(top5_small_chart, use_container_width=True)

    st.write('<div style="text-align: justify">Keberadaan kecamatan Tomang dan Pademangan pada grafik ini yang sebelumnya juga berada pada grafik Top 5 Kecamatan dengan Harga Rumah Rata-Rata tertinggi dan Keberadaan kecamatan Jagakarsa dan Pasar Rebo pad grafik ini yang sebelumnya juga berada pada grafik Top 5 Kecamatan dengan Harga Rumah Rata-Rata Terendah menandakan bahwa semakin besar luas bangunannya, maka semakin besar pula harga rumahnya. Sebaliknya semakin kecil luas bangunannya, semakin murah pula harga rumahnya.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Visualisasi: Harga Rata-Rata Properti Berdasarkan Kota dan Kecamatan
    average_price_by_city_district = df.groupby(['Kota', 'Kecamatan'])['Harga'].mean().reset_index()

    # Membuat grafik harga rata-rata properti berdasarkan kota dan kecamatan
    st.subheader('Harga Rata-rata Properti Berdasarkan Kota dan Kecamatan')

    # Pilih Kota menggunakan multiselect
    selected_city = st.multiselect('Pilih Kota', average_price_by_city_district['Kota'].unique())

    # Filter data berdasarkan Kota yang dipilih
    filtered_data = average_price_by_city_district[average_price_by_city_district['Kota'].isin(selected_city)]

    # Buat chart Altair
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X('Harga:Q', axis=alt.Axis(title='Harga Rata-rata')),
        y=alt.Y('Kecamatan:N', axis=alt.Axis(title='Kecamatan'), sort='-x'),
        color='Kota:N',
        tooltip=['Harga:Q']
    ).properties(width=800)

    # Tampilkan chart
    st.altair_chart(chart, use_container_width=True)

with prediksi:
    # Header Prediksi Harga Rumah
    st.header("Prediksi Harga Rumah dengan Linear Regression")
    st.write("""Silakan masukkan spesifikasi rumah yang ingin diprediksi harganya di bawah ini.""")

    # Input data menggunakan input text
    col1, col2, col3 = st.columns(3)

    with col1:
        lb = st.text_input('Luas Bangunan (m2)')
    with col2:   
        lt = st.text_input('Luas Tanah (m2)')
    with col3:    
        kt = st.text_input('Jumlah Kamar Tidur')

    col4, col5 = st.columns(2)

    with col4:
        km = st.text_input('Jumlah Kamar Mandi')
    with col5:
        lnt = st.text_input('Jumlah Lantai')


    col6, col7 = st.columns(2)

    with col6:
        # Menggunakan radio button untuk tipe sertifikat
        serti_options = ['SHM', 'HGB', 'Lainnya (PPJB, Girik, Adat, dll)']
        serti = st.radio('Tipe Sertifikat', serti_options)
    with col7:
        # Menggunakan radio button untuk kota
        kota_options = ['Jakarta Selatan', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Pusat', 'Jakarta Utara']
        kota = st.radio('Kota', kota_options)

    # Membuat tombol untuk prediksi
    if st.button('Prediksi Harga Rumah'):
        # Konversi input ke tipe data numerik
        lb = int(lb)
        lt = int(lt)
        kt = int(kt)
        km = int(km)
        lnt = int(lnt)

        # Membuat dataframe untuk prediksi
        new_data = pd.DataFrame({'Luas Bangunan': [lb], 'Luas Tanah': [lt], 'Kamar Tidur': [kt],
                                'Kamar Mandi': [km], 'Lantai': [lnt], 'HGB': [1 if serti == 'HGB' else 0],
                                'Lainnya (PPJB, Girik, Adat, dll)': [1 if serti == 'Lainnya (PPJB, Girik, Adat, dll)' else 0],
                                'SHM': [1 if serti == 'SHM' else 0],
                                'Kota_Jakarta Barat': [1 if kota == 'Jakarta Barat' else 0],
                                'Kota_Jakarta Pusat': [1 if kota == 'Jakarta Pusat' else 0],
                                'Kota_Jakarta Selatan': [1 if kota == 'Jakarta Selatan' else 0],
                                'Kota_Jakarta Timur': [1 if kota == 'Jakarta Timur' else 0],
                                'Kota_Jakarta Utara': [1 if kota == 'Jakarta Utara' else 0]})

        
        # Membuat prediksi
        predicted_price = regression_model.predict(new_data)

        # Fungsi untuk format mata uang Rupiah tanpa desimal
        def format_rupiah(amount):
            formatted_price = f"Rp {int(amount):,}"
            return formatted_price

        # Format mata uang Rupiah
        formatted_price = format_rupiah(predicted_price[0])

        # Menampilkan hasil prediksi
        st.write(f'Prediksi Harga Rumah: {formatted_price}')


with about:
    # Header
    st.header("About Me")
    st.write("Hi, My name is Tedja Diah Rani Octavia. I am an informatics student at Universitas Pembangunan Nasional Veteran Jakarta. Thank you for visiting my project.")

    # Introduction
    st.write("Recently, I was interested in analyzing data. This was my very first data visualization dashboard project, so I'd love to hear any suggestions.")

    # Contact Information
    st.subheader("Contact Me:")
    st.write("Please contact me for more information about this project or for any suggestions.")
    st.write("Email: raniranoc@gmail.com")
    st.write("LinkedIn: https://www.linkedin.com/in/tedjadiahrani/")
    st.write("GitHub: https://github.com/ranioc")

    # Thank You Message
    st.write("Thank you!")
