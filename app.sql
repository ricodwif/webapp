DROP TABLE IF EXISTS schedule;
CREATE TABLE schedule (
    id serial,
    maskapai text,
    bandara_asal text,
    bandara_tujuan text,
    waktu_keberangkatan time,
    waktu_sampai time,
    tanggal date,
    gate_keberangkatan text,
    status_penerbangan text,
    Layanan_pesawat text,
    max_capacity integer);
insert into schedule (	maskapai, bandara_asal,bandara_tujuan,tanggal, waktu_keberangkatan, waktu_sampai, gate_keberangkatan,
    status_penerbangan,Layanan_pesawat,max_capacity)
values
	('Garuda Indonesia', 'Soekarno-Hatta', 'Ngurah Rai', '2023-11-22', '08:30', '10:30', 'Gate A1', 'On Time', '["Ekonomi", "Bisnis", "First Class"]', 300),
    ('Lion Air', 'Juanda', 'Sultan Hasanuddin', '2023-11-22', '09:15', '11:30', 'Gate B2', 'Delayed', '["Ekonomi", "Bisnis", "First Class"]', 250),
    ('Citilink', 'Ngurah Rai', 'Minangkabau International', '2023-11-22', '10:00', '12:00', 'Gate C3', 'On Time', '["Ekonomi", "Bisnis", "First Class"]', 200),
    ('Batik Air', 'Adisutjipto', 'Kuala Namu International', '2023-11-22', '11:45', '14:00', 'Gate D4', 'Delay','["Ekonomi", "Bisnis", "First Class"]', 280),
    ('Sriwijaya Air', 'Minangkabau International', 'Adisutjipto', '2023-11-22', '12:30', '14:45', 'Gate E5', 'On Time', '["Ekonomi", "Bisnis", "First Class"]', 230),
    ('NAM Air', 'Sultan Hasanuddin', 'Ngurah Rai', '2023-11-22', '13:15', '15:30', 'Gate F6', 'Last Call', '["Ekonomi", "Bisnis", "First Class"]', 260),
    ('AirAsia Indonesia', 'Ngurah Rai', 'Juanda', '2023-11-22', '14:00', '16:00', 'Gate G7', 'Delayed', '["Ekonomi", "Bisnis", "First Class"]', 220),
    ('Wings Air', 'Sultan Aji Muhammad Sulaiman', 'Sultan Hasanuddin', '2023-11-22', '15:45', '18:00', 'Gate H8', 'On Time','["Ekonomi", "Bisnis", "First Class"]', 180),
    ('TransNusa', 'Adisutjipto', 'Sultan Syarif Kasim II', '2023-11-22', '16:30', '18:45', 'Gate I9', 'On Time', '["Ekonomi", "Bisnis", "First Class"]', 150),
    ('Susi Air', 'Sultan Hasanuddin', 'Sentani International', '2023-11-23', '07:00', '10:15', 'Gate X24', 'On Time', '["Ekonomi", "Bisnis", "First Class"]', 50);

SELECT * FROM schedule;