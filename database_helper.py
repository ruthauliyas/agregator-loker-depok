import sqlite3

def simpan_ke_db(data_list):
    """
    data_list adalah list berisi tuple:
    (nama_perusahaan, job_desk, alamat, gaji, kontak, sumber, platform)
    """
    conn = sqlite3.connect('loker.db')
    c = conn.cursor()
    # Pastikan tabel ada
    c.execute('''CREATE TABLE IF NOT EXISTS lowongan
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nama_perusahaan TEXT, job_desk TEXT, alamat TEXT, 
                  gaji TEXT, kontak TEXT, sumber TEXT, platform TEXT)''')
    
    c.executemany('''INSERT INTO lowongan (nama_perusahaan, job_desk, alamat, gaji, kontak, sumber, platform) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', data_list)
    conn.commit()
    conn.close()
    print(f"Berhasil menyimpan {len(data_list)} data ke database.")