import pandas as pd

NAMA_FILE_CSV = "lokasi_semarang.csv"

def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    print(f"Mencoba membaca file CSV: {nama_file}")
    try:
        dataframe = pd.read_csv(nama_file)
        print(" -> File CSV berhasil dibaca.")
        return dataframe
    except FileNotFoundError:
        print(f" -> ERROR: File '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f" -> ERROR saat membaca file CSV: {type(e).__name__} ({e})")
        return None

if __name__ == "__main__":
    print("--- Memulai Praktikum 2: Membaca CSV ---")
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)
    
    if df_lokasi is not None:
        print("\n--- Inspeksi Awal DataFrame ---")
        print("\n1. Lima Baris Pertama (head()):")
        print(df_lokasi.head())
        
        print("\n2. Informasi DataFrame (info()):")
        df_lokasi.info()
        
        jumlah_baris, jumlah_kolom = df_lokasi.shape
        print(f"\n3. Dimensi Data:")
        print(f"   Jumlah Lokasi (Baris)   : {jumlah_baris}")
        print(f"   Jumlah Atribut (Kolom)  : {jumlah_kolom}")
        
        print(f"\n4. Nama Kolom:")
        print(list(df_lokasi.columns))
    else:
        print("\nTidak dapat melanjutkan inspeksi karena gagal membaca file CSV.")
    print("\n--- Praktikum 2 Selesai ---")