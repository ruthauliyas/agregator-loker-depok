from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def halaman_utama():
    # Ambil nomor halaman dari URL (default ke 1)
    page = int(request.args.get('page', 1))
    per_page = 10  # Jumlah loker per halaman
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect('loker.db')
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    
    # Ambil total data untuk hitung jumlah halaman
    c.execute("SELECT COUNT(*) FROM lowongan")
    total_data = c.fetchone()[0]
    total_pages = (total_data // per_page) + (1 if total_data % per_page > 0 else 0)
    
    # Ambil data sesuai halaman (limit 10, skip sesuai offset)
    c.execute("SELECT * FROM lowongan ORDER BY id ASC LIMIT ? OFFSET ?", (per_page, offset))
    data_loker = c.fetchall()
    conn.close()
    
    return render_template('index.html', loker=data_loker, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)