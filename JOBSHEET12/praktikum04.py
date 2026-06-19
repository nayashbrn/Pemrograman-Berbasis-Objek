import pandas as pd
from praktikum02 import baca_data_lokasi
from praktikum03 import TempatWisata, Kuliner, TempatIbadah

def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty:
        print("DataFrame kosong atau None, tidak ada objek dibuat.")
        return list_objek_lokasi
    
    print("\nMembuat objek dari DataFrame...")
    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')
        
        if nama is None or lat is None or lon is None:
            continue
            
        objek = None
        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                agama_info = "Umum"
                if "Islam" in tipe: agama_info = "Islam"
                elif "Kristen" in tipe: agama_info = "Kristen"
                elif "Klenteng" in tipe: agama_info = "Tridharma"
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)
            
            if objek:
                list_objek_lokasi.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")
            
    print(f"Total {len(list_objek_lokasi)} objek lokasi berhasil dibuat dari {len(dataframe)} baris data.")
    return list_objek_lokasi

if __name__ == "__main__":
    print("--- Memulai Praktikum 4: Membuat Objek dari Data Pandas ---")
    df_lokasi = baca_data_lokasi("lokasi_semarang.csv")
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)
    
    print("\n--- Daftar Objek Lokasi yang Berhasil Dibuat (Hasil __repr__) ---")
    if list_semua_lokasi:
        for idx, lok in enumerate(list_semua_lokasi):
            print(f" {idx+1}. {repr(lok)}")
    else:
        print("Tidak ada objek lokasi yang dibuat.")
    print("\n--- Praktikum 4 Selesai ---")