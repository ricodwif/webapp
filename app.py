import streamlit as st
from sqlalchemy import text
import pandas as pd

list_maskapai = ['Garuda Indonesia', 'Lion Air', 'Citilink', 'Batik Air', 'Sriwijaya Air', 'NAM Air', 'AirAsia Indonesia', 'Wings Air', 'TransNusa', 'Susi Air']
list_status_penerbangan = ['', 'On Time', 'Delayed', 'Last call']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwirico08:6wgkTJSMoL1U@ep-curly-salad-29186979.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SCHEDULE (id serial, maskapai varchar, bandara_asal varchar, bandara_tujuan text, \
                                                       waktu_keberangkatan time, waktu_sampai time, tanggal date, gate_keberangkatan text, status_penerbangan text, layanan_pesawat text, max_capacity varchar);')
    session.execute(query)
st.header('AIRPORT DATA MANAGEMENT SYSTEM ✈️')
menu_options = ["View Data", "Edit Data", "Search Data","Grafik Penerbangan"]
selected_options = st.selectbox("Pilih Menu", menu_options)

if "View Data" in selected_options:
    st.header("View Data")
    pd.options.display.float_format = '{:,.0f}'.format
    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0").set_index('id')
    data['max_capacity'] = data['max_capacity'].astype(str)  
    data = data.dropna()
    st.dataframe(data.style.set_properties(**{'background-color': '#03045E', 'color': 'black'}))
if "Edit Data" in selected_options:
    st.header("Edit Data")
    password_attempt = st.text_input("Masukkan Kata Sandi", type="password")

    if password_attempt == "FPKELOMPOK8":
        data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0")
        for _, result in data.iterrows():        
            id = result['id']
            maskapai_lama = result["maskapai"]
            bandara_asal_lama = result["bandara_asal"]
            bandara_tujuan_lama = result["bandara_tujuan"]
            waktu_keberangkatan_lama = result["waktu_keberangkatan"]
            waktu_sampai_lama = result["waktu_sampai"]
            tanggal_lama = result["tanggal"]
            gate_keberangkatan_lama = result["gate_keberangkatan"]
            status_penerbangan_lama = result["status_penerbangan"]
            layanan_pesawat_lama = result["layanan_pesawat"]
            max_capacity_lama = result["max_capacity"]

            with st.expander(f'Maskapai {maskapai_lama}'):
                with st.form(f'data-{id}'):
                    bandara_asal_baru = st.text_input("bandara_asal", bandara_asal_lama)
                    maskapai_baru = st.selectbox("maskapai_name", list_maskapai, index= list_maskapai.index(maskapai_lama) if maskapai_lama in list_maskapai else 0)
                    bandara_tujuan_baru = st.text_input("bandara_tujuan", bandara_tujuan_lama)
                    waktu_keberangkatan_baru = st.time_input("waktu_keberangkatan", waktu_keberangkatan_lama)
                    waktu_sampai_baru = st.time_input("waktu_sampai", waktu_sampai_lama)
                    tanggal_baru = st.date_input("tanggal", tanggal_lama)
                    gate_keberangkatan_baru = st.text_input("gate_keberangkatan", gate_keberangkatan_lama)
                    status_penerbangan_baru = st.selectbox("status_penerbangan",list_status_penerbangan,index=list_status_penerbangan.index(status_penerbangan_lama) if status_penerbangan_lama in list_status_penerbangan else 0)
                    layanan_pesawat_baru = st.multiselect("layanan_pesawat", ['Ekonomi', 'Bisnis', 'First Class'], eval(layanan_pesawat_lama))
                    max_capacity_baru = st.text_input("max_capacity", max_capacity_lama)
                    max_capacity_baru = str(max_capacity_baru)
                    
                    col1, col2,col3 = st.columns([7, 7,7])

                    with col1:
                        if st.form_submit_button('UPDATE'):
                            with conn.session as session:
                                query = text('UPDATE schedule \
                                              SET maskapai=:1, bandara_asal=:2, bandara_tujuan=:3, waktu_keberangkatan=:4, \
                                              waktu_sampai=:5, tanggal=:6, gate_keberangkatan=:7, status_penerbangan=:8, layanan_pesawat=:9, max_capacity=:10\
                                              WHERE id=:11;')
                                session.execute(query, {'1':maskapai_baru, '2':bandara_asal_baru, '3':bandara_tujuan_baru, '4':waktu_keberangkatan_baru, 
                                                        '5':waktu_sampai_baru, '6':tanggal_baru, '7':gate_keberangkatan_baru, '8':status_penerbangan_baru, '9':str(layanan_pesawat_baru), '10':max_capacity_baru, '11':id})
                                session.commit()
                                st.experimental_rerun()
                    with col2:
                        if st.form_submit_button('DELETE'):
                            query_delete = text(f'DELETE FROM schedule WHERE id=:1;')
                            session.execute(query_delete, {'1': id})
                            session.commit()
                    with col3:
                        if st.form_submit_button('Tambah Data'):
                            with conn.session as session:
                                query = text('INSERT INTO schedule (maskapai, bandara_asal, bandara_tujuan, waktu_keberangkatan, waktu_sampai, tanggal, gate_keberangkatan, status_penerbangan, layanan_pesawat, max_capacity) \
                                             VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10);')
                                session.execute(query, {'1':'', '2':'', '3':'', '4':None, '5':None, '6':None, '7':'', '8':'[]', '9':'[]', '10':'' })
                                session.commit()
                                st.experimental_rerun()
    else:
        st.error("Kata Sandi Salah")
if "Search Data" in selected_options:
    st.header("Search Data")
    search_option = st.selectbox("Select Search Option", ["Maskapai", "Tanggal", "Bandara Asal", "Bandara Tujuan"])
    maskapai_search = ""
    tanggal_search = ""
    bandara_asal_search = ""
    bandara_tujuan_search = ""

    if search_option == "Maskapai":
        maskapai_search = st.text_input("Search by Maskapai:", "")
    elif search_option == "Tanggal":
        tanggal_search = st.date_input("Search by Tanggal:")
    elif search_option == "Bandara Asal":
        bandara_asal_search = st.text_input("Search by Bandara Asal:")
    elif search_option == "Bandara Tujuan":
        bandara_tujuan_search = st.text_input("Search by Bandara Tujuan:")

    if st.button("Search"):
        conditions = []
        parameters = {}
        if search_option == "Maskapai" and maskapai_search:
            conditions.append("maskapai ILIKE :maskapai")  # Menggunakan ILIKE untuk pencarian case-insensitive
            parameters['maskapai'] = f'%{maskapai_search}%'

        elif search_option == "Tanggal" and tanggal_search:
            conditions.append("tanggal = :tanggal")
            parameters['tanggal'] = tanggal_search

        elif search_option == "Bandara Asal" and bandara_asal_search:
            conditions.append("bandara_asal ILIKE :bandara_asal")
            parameters['bandara_asal'] = f'%{bandara_asal_search}%'

        elif search_option == "Bandara Tujuan" and bandara_tujuan_search:
            conditions.append("bandara_tujuan ILIKE :bandara_tujuan")
            parameters['bandara_tujuan'] = f'%{bandara_tujuan_search}%'

        if conditions:
            condition_str = " AND ".join(conditions)
            query = f"SELECT * FROM schedule WHERE {condition_str} ORDER BY id;"
            with conn.session as session:
                result = session.execute(text(query), parameters)
                data = result.fetchall()
                if not data:
                    st.warning("DATA TIDAK DITEMUKAN!")
                else:
                    st.dataframe(data)
        else:
            st.warning("Pilih opsi pencarian dan isi kolom pencarian.")
if "Grafik Penerbangan" in selected_options:
    st.header("Grafik Penerbangan")
    with conn.session as session:
        result = session.execute(text('SELECT * FROM schedule;'))
        data = result.fetchall()
    df = pd.DataFrame(data, columns=result.keys())
    selected_aspect = st.selectbox("Grafik penerbangan berdasarkan", ["Maskapai", "Tanggal Keberangkatan", "Bandara Asal", "Bandara Tujuan"])
    st.subheader(f"Visualisasi Data per {selected_aspect}")
    if selected_aspect == "Maskapai":
        aspect_counts = df['maskapai'].value_counts()
        st.bar_chart(aspect_counts)
    elif selected_aspect == "Tanggal Keberangkatan":
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        filtered_df = df[(df['tanggal'] >= start_date) & (df['tanggal'] <= end_date)]
        st.line_chart(filtered_df['tanggal'].value_counts())
    elif selected_aspect == "Bandara Asal":
        aspect_counts = df['bandara_asal'].value_counts()
        st.bar_chart(aspect_counts)
    elif selected_aspect == "Bandara Tujuan":
        aspect_counts = df['bandara_tujuan'].value_counts()
        st.bar_chart(aspect_counts)