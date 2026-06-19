import folium
from praktikum02 import baca_data_lokasi
from praktikum04 import buat_objek_lokasi_dari_df

def buat_peta_lokasi_folium(list_objek: list, file_output: str = "peta_lokasi.html"):
    if not list_objek:
        print("Tidak ada objek lokasi untuk dipetakan.")
        return

    print(f"\nMemulai pembuatan peta Folium dari {len(list_objek)} lokasi...")
    
    try:
        lat_tengah = list_objek[0].latitude
        lon_tengah = list_objek[0].longitude
    except IndexError:
        lat_tengah, lon_tengah = -6.9929, 110.4200
        
    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=13)
    
    jumlah_marker_valid = 0
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup() # Polimorfisme mengambil html popup
            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama
            ).add_to(peta)
            jumlah_marker_valid += 1

    try:
        peta.save(file_output)
        print(f"\n-> Peta berhasil dibuat dan disimpan sebagai '{file_output}'.")
        print(f"   Total marker ditambahkan: {jumlah_marker_valid}")
    except Exception as e:
        print(f"\nERROR saat menyimpan peta Folium: {type(e).__name__} {e}")

if __name__ == "__main__":
    print("--- Memulai Praktikum 5: Visualisasi Peta dengan Folium ---")
    df_lokasi = baca_data_lokasi("lokasi_semarang.csv")
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)
    
    buat_peta_lokasi_folium(list_semua_lokasi, "peta_interaktif_semarang.html")
    print("\n--- Praktikum 5 Selesai ---")