import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import database_helper
import time

# Fungsi untuk membuka link detail dan mengambil data spesifik
def ambil_detail(link):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Cari alamat di paragraf atau list yang mengandung kata kunci lokasi
        alamat = "Depok (Cek link untuk detail)"
        teks_elemen = soup.find_all(["p", "li", "td"])
        for t in teks_elemen:
            if any(kunci in t.text.lower() for kunci in ["jalan", "jl.", "kecamatan"]):
                alamat = t.text.strip()[:150]
                break
        return alamat
    except:
        return "Depok (Gagal memuat alamat)"

def ambil_data_loker_id():
    print("Mulai scraping Loker.id...")
    base_url = "https://www.loker.id/cari-lowongan-kerja?lokasi=depok&page="
    all_data = []

    # Ambil 3 halaman pertama
    for page in range(1, 4):
        print(f"Memproses Halaman {page}...")
        url = base_url + str(page)
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            cards = soup.find_all("article", class_="card")
            
            links = []
            temp_data = []
            
            for card in cards:
                link = card.find("a")["href"]
                if link.startswith("/"): link = "https://www.loker.id" + link
                
                posisi = card.find("h3").text.strip()
                perusahaan = card.find("span", class_="text-secondary-500").text.strip()
                
                links.append(link)
                temp_data.append((perusahaan, posisi, link))

            # Proses detail secara paralel (Multi-threading)
            with ThreadPoolExecutor(max_workers=10) as executor:
                alamat_list = list(executor.map(ambil_detail, links))
            
            # Gabungkan jadi tuple untuk database
            for i, data in enumerate(temp_data):
                perusahaan, posisi, link = data
                all_data.append((perusahaan, posisi, alamat_list[i], "Lihat di web", "Lamar via Web", link, "LokerID"))
            
            time.sleep(2) # Jeda antar halaman
        except Exception as e:
            print(f"Error di halaman {page}: {e}")

    # Simpan ke DB lewat Helper
    database_helper.simpan_ke_db(all_data)
    print("Loker.id Selesai!")