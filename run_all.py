import scraper_lokerid
# import scraper_glints  # Nanti kita buka kalau sudah dibuat
# import scraper_indeed

def jalankan_semua():
    print("--- MEMULAI PROSES UPDATE DATA ---")
    try:
        scraper_lokerid.ambil_data_loker_id()
        # scraper_glints.ambil_data_glints()
        # scraper_indeed.ambil_data_indeed()
    except Exception as e:
        print(f"Terjadi error saat menjalankan scraper: {e}")
    print("--- UPDATE SELESAI ---")

if __name__ == '__main__':
    jalankan_semua()