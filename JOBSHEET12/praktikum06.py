import folium
import datetime
from praktikum02 import baca_data_lokasi
from praktikum04 import buat_objek_lokasi_dari_df

def tulis_log(pesan: str, file_log: str = "proses_peta.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {pesan}\n")
    except IOError as e:
        print(f"ERROR: Gagal menulis ke file log '{file_log}': {e}")

def buat_peta_lokasi_folium_logging(list_objek: list, file_output: str = "peta_lokasi.html"):
    nama_fungsi = "buat_peta_lokasi_folium"
    
    if not list_objek:
        pesan_log = f" [{nama_fungsi}] Gagal: Tidak ada data lokasi untuk dipetakan."
        print(pesan_log)
        tulis_log(pesan_log)
        return

    print(f"\n[{nama_fungsi}] Memulai pembuatan peta dari {len(list_objek)} lokasi...")
    tulis_log(f"[{nama_fungsi}] Memulai pembuatan peta '{file_output}' dengan {len(list_objek)} lokasi.")

    try:
        lat_tengah = list_objek[0].latitude
        lon_tengah = list_objek[0].longitude
    except IndexError:
        lat_tengah, lon_tengah = -6.9929, 110.4200
        
    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=12)
    
    jumlah_marker = 0
    lokasi_dilewati = []
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()
            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama
            ).add_to(peta)
            jumlah_marker += 1
        else:
            lokasi_dilewati.append(lok.nama)

    if lokasi_dilewati:
        pesan_lewat = f" [{nama_fungsi}] Melewati marker untuk: {', '.join(lokasi_dilewati)} (koordinat tidak valid)."
        print(f" -> Peringatan: {pesan_lewat}")
        tulis_log(pesan_lewat)

    try:
        peta.save(file_output)
        pesan_sukses = f" [{nama_fungsi}] Peta '{file_output}' berhasil dibuat dengan {jumlah_marker} marker."
        print(f"-> {pesan_sukses}")
        tulis_log(pesan_sukses)
    except Exception as e:
        pesan_error = f" [{nama_fungsi}] ERROR saat menyimpan peta '{file_output}': {type(e).__name__} {e}"
        print(f"-> {pesan_error}")
        tulis_log(pesan_error)

if __name__ == "__main__":
    print("--- Memulai Praktikum 6: File Handling Tambahan (Log) ---")
    df_lokasi = baca_data_lokasi("lokasi_semarang.csv")
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)
    
    buat_peta_lokasi_folium_logging(list_semua_lokasi, "peta_interaktif_semarang.html")
    
    print("\nMenjalankan pembuatan peta lagi untuk demo log append...")
    buat_peta_lokasi_folium_logging(list_semua_lokasi, "peta_kedua.html")
    
    print("\nSilakan periksa isi file log 'proses_peta.log' untuk melihat catatan proses.")
    print("\n--- Praktikum 6 Selesai ---")