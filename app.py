import streamlit as st
from sqlalchemy import text

maskapai = ['', 'Garuda Indonesia', 'Lion Air', 'Citilink', 'Batik Air', 'Sriwijaya Air', 'NAM Air', 'AirAsia Indonesia', 'Wings Air', 'TransNusa', 'Susi Air']
status_penerbangan = ['', 'On time', 'Delay', 'Last call']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwirico08:6wgkTJSMoL1U@ep-curly-salad-29186979.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SCHEDULE (id serial, maskapai varchar, bandara_asal varchar, bandara_tujuan text, \
                                                       waktu_keberangkatan time, waktu_sampai time, tanggal date, gate_keberangkatan text, status_penerbangan text, layanan_pesawat text, max_capacity varchar);')
    session.execute(query)

st.header('AIRPORT DATA MANAGEMENT SYS')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO schedule (maskapai, bandara_asal, bandara_tujuan, waktu_keberangkatan, waktu_sampai, tanggal, gate_keberangkatan, status_penerbangan, layanan_pesawat, max_capacity) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':None, '5':None, '6':None, '7':'[]', '8':'[]', '9':'[]', '10':''})
            session.commit()

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

        with st.expander(f'a.n. {maskapai_lama}'):
            with st.form(f'data-{id}'):
                bandara_asal_baru = st.text_input("bandara_asal", bandara_asal)
                maskapai_baru = st.selectbox("maskapai_name",list_maskapai, list_maskapai.index(maskapai_lama))
                bandara_tujuan_baru = st.text_input("bandara_tujuan", bandara_tujuan)
                waktu_keberangkatan_baru = st.time_input("waktu_keberangkatan", waktu_keberangkatan)
                waktu_sampai_baru = st.time_input("waktu_sampai", waktu_sampai)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                gate_keberangkatan_baru = st.text_input("gate_keberangkatan", gate_keberangkatan)
                status_penerbangan_baru = st.selectbox("status_penerbangan", list_status_penerbangan, list_status_penerbangan.index(status_penerbangan_lama))
                layanan_pesawat_baru = st.multiselect("layanan_pesawat", ['Ekonomi', 'Bisnis', 'First Class'], eval(layanan_pesawat_lama))
                max_capacity_baru = st.text_input("max_capacity", max_capacity_lama)
                
                col1, col2 = st.columns([1, 7])

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
                        query = text(f'DELETE FROM schedule WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()