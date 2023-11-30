import streamlit as st
from sqlalchemy import text

list_maskapai = ['', 'Garuda Indonesia', 'Lion Air', 'Citilink', 'Batik Air', 'Sriwijaya Air', 'NAM Air', 'AirAsia Indonesia', 
                 'Wings Air', 'TransNusa', 'Indonesia AirAsia X', 'Susi Air', 'Kalstar Aviation', 'Trigana Air', 'Pelita Air', 
                 'Aviastar Mandiri']
list_bandara = ['', 'Soekarno-Hatta', 'Ngurah Rai', 'Juanda', 'Sultan Hasanuddin', 'Minangkabau International', 'Adisutjipto', 
                 'Kuala Namu International', 'Sultan Aji Muhammad Sulaiman', 'Sultan Syarif Kasim II', 'El Tari', 'Wamena', 
                 'Sentani International', 'Supadio International', 'Sultan Syarif Qasim II', 'Juwata International', 
                 'Raja Haji Fisabilillah International', 'Frans Kaisiepo International', 'Bali International', 'Sultan Iskandar Muda']

list_gate = ['', 'Gate A1', 'Gate B2', 'Gate C3', 'Gate D4', 'Gate E5', 'Gate F6', 'Gate G7', 'Gate H8', 'Gate I9', 'Gate J10',
              'Gate K11', 'Gate L12', 'Gate M13', 'Gate N14', 'Gate O15', 'Gate P16', 'Gate Q17', 'Gate R18', 'Gate S19', 
              'Gate T20', 'Gate U21', 'Gate V22', 'Gate W23', 'Gate X24']

list_status = ['', 'On Time', 'Delayed']

list_layanan_pesawat = ['', 'Ekonomi', 'Bisnis', 'First Class']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dwirico08:6wgkTJSMoL1U@ep-curly-salad-29186979.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('DROP TABLE IF EXISTS schedule;'
                 'CREATE TABLE schedule (id serial, maskapai text, bandara_asal text, bandara_tujuan text,'
                 'waktu_keberangkatan time, waktu_sampai time, tanggal date, gate_keberangkatan text,'
                 'status_penerbangan text, Layanan_pesawat text, max_capacity integer);')
    session.execute(query)

st.header('AIRLINE FLIGHT SCHEDULE MANAGEMENT SYSTEM')
page = st.sidebar.selectbox("Choose Menu", ["View Data", "Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM schedule ORDER BY id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Add Data'):
        with conn.session as session:
            query = text('INSERT INTO schedule (maskapai, bandara_asal, bandara_tujuan, tanggal, waktu_keberangkatan,'
                         'waktu_sampai, gate_keberangkatan, status_penerbangan, Layanan_pesawat, max_capacity) VALUES'
                         '(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10);')
            session.execute(query, {'1': '', '2': '', '3': '', '4': None, '5': None, '6': None, '7': '', '8': '', '9': '[]', '10': None})
            session.commit()

    data = conn.query('SELECT * FROM schedule ORDER BY id;', ttl="0")
    for _, result in data.iterrows():
        id = result['id']
        maskapai_lama = result["maskapai"]
        bandara_asal_lama = result["bandara_asal"]
        bandara_tujuan_lama = result["bandara_tujuan"]
        tanggal_lama = result["tanggal"]
        waktu_keberangkatan_lama = result["waktu_keberangkatan"]
        waktu_sampai_lama = result["waktu_sampai"]
        gate_keberangkatan_lama = result["gate_keberangkatan"]
        status_penerbangan_lama = result["status_penerbangan"]
        layanan_pesawat_lama = result["Layanan_pesawat"]
        max_capacity_lama = result["max_capacity"]

        with st.expander(f'{maskapai_lama} - {bandara_asal_lama} to {bandara_tujuan_lama}'):
            with st.form(f'data-{id}'):
                maskapai_baru = st.selectbox("Airline", list_maskapai, list_maskapai.index(maskapai_lama))
                bandara_asal_baru = st.selectbox("Departure Airport", list_bandara, list_bandara.index(bandara_asal_lama))
                bandara_tujuan_baru = st.selectbox("Destination Airport", list_bandara, list_bandara.index(bandara_tujuan_lama))
                tanggal_baru = st.date_input("Date", tanggal_lama)
                waktu_keberangkatan_baru = st.time_input("Departure Time", waktu_keberangkatan_lama)
                waktu_sampai_baru = st.time_input("Arrival Time", waktu_sampai_lama)
                gate_keberangkatan_baru = st.selectbox("Departure Gate", list_gate, list_gate.index(gate_keberangkatan_lama))
                status_penerbangan_baru = st.selectbox("Flight Status", list_status, list_status.index(status_penerbangan_lama))
                layanan_pesawat_baru = st.multiselect("Services", list_layanan_pesawat, eval(layanan_pesawat_lama))
                max_capacity_baru = st.number_input("Max Capacity", max_capacity_lama)

                if st.form_submit_button('UPDATE'):
                    with conn.session as session:
                        query = text('UPDATE schedule SET maskapai=:1, bandara_asal=:2, bandara_tujuan=:3,'
                                     'tanggal=:4, waktu_keberangkatan=:5, waktu_sampai=:6, gate_keberangkatan=:7,'
                                     'status_penerbangan=:8, Layanan_pesawat=:9, max_capacity=:10 WHERE id=:11;')
                        session.execute(query, {'1': maskapai_baru, '2': bandara_asal_baru, '3': bandara_tujuan_baru,
                                               '4': tanggal_baru, '5': waktu_keberangkatan_baru, '6': waktu_sampai_baru,
                                               '7': gate_keberangkatan_baru, '8': status_penerbangan_baru,
