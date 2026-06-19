import pandas as pd
import folium
from abc import ABC, abstractmethod

# ==========================================
# 1. KELAS OOP (Ditambah Kelas Baru)
# ==========================================
class Lokasi(ABC):
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            self.latitude = 0.0
            self.longitude = 0.0

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

class TempatWisata(Lokasi):
    def __init__(self, nama, latitude, longitude, jenis, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Kuliner(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak diketahui"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TempatIbadah(Lokasi):
    def __init__(self, nama, latitude, longitude, agama, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

# --- Kelas Baru untuk Penugasan ---
class KantorPemerintahan(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Kantor Pemerintahan"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kantor Pemerintahan</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Museum(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Museum"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Museum</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TamanKota(Lokasi):
    def __init__(self, nama, latitude, longitude, deskripsi):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Taman Kota"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Taman Kota</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


# ==========================================
# 2. BACA DATA CSV & BUAT OBJEK
# ==========================================
def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty: return list_objek_lokasi
    
    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')
        
        if nama is None or lat is None or lon is None: continue
            
        objek = None
        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                objek = TempatIbadah(nama, lat, lon, "Umum", deskripsi)
            # --- Modifikasi Penugasan: Deteksi tipe baru ---
            elif tipe == 'Kantor Pemerintahan':
                objek = KantorPemerintahan(nama, lat, lon, deskripsi)
            elif tipe == 'Museum':
                objek = Museum(nama, lat, lon, deskripsi)
            elif tipe == 'Taman Kota':
                objek = TamanKota(nama, lat, lon, deskripsi)
            
            if objek: list_objek_lokasi.append(objek)
        except Exception as e:
            print(f"GAGAL membuat objek: {e}")
            
    return list_objek_lokasi


# ==========================================
# 3. KUSTOMISASI PETA FOLIUM & BACA CONFIG
# ==========================================
def buat_peta_lokasi_folium(list_objek: list, file_output: str = "peta_penugasan.html"):
    # --- Modifikasi Penugasan: Baca konfigurasi ---
    lat_tengah, lon_tengah, zoom_awal = -6.9929, 110.4200, 13 # Nilai Default
    try:
        with open("config_peta.txt", 'r') as f:
            lines = f.readlines()
            lat_tengah = float(lines[0].strip())
            lon_tengah = float(lines[1].strip())
            zoom_awal = int(lines[2].strip())
        print("-> Berhasil membaca konfigurasi dari config_peta.txt")
    except (FileNotFoundError, ValueError, IndexError) as e:
        print(f"-> Peringatan: Gagal membaca config_peta.txt ({e}). Menggunakan default.")

    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=zoom_awal)
    
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()
            
            # --- Modifikasi Penugasan: Kustomisasi Marker (isinstance) ---
            warna_marker = 'blue'
            ikon_marker = 'info-sign'
            
            if isinstance(lok, TempatWisata):
                warna_marker = 'blue'
                ikon_marker = 'camera'
            elif isinstance(lok, Kuliner):
                warna_marker = 'red'
                ikon_marker = 'cutlery'
            elif isinstance(lok, TempatIbadah):
                warna_marker = 'purple'
                ikon_marker = 'bookmark'
            elif isinstance(lok, KantorPemerintahan):
                warna_marker = 'gray'
                ikon_marker = 'briefcase'
            elif isinstance(lok, Museum):
                warna_marker = 'orange'
                ikon_marker = 'book'
            elif isinstance(lok, TamanKota):
                warna_marker = 'green'
                ikon_marker = 'tree-conifer'

            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama,
                icon=folium.Icon(color=warna_marker, icon=ikon_marker)
            ).add_to(peta)

    peta.save(file_output)
    print(f"-> Peta berhasil dibuat: '{file_output}'")


# ==========================================
# 4. KODE UTAMA
# ==========================================
if __name__ == "__main__":
    print("--- Memulai Eksekusi Penugasan Akhir ---")
    
    try:
        df_lokasi = pd.read_csv("lokasi_semarang.csv")
        print("-> Data CSV berhasil dibaca.")
    except Exception as e:
        print(f"-> GAGAL membaca CSV: {e}")
        df_lokasi = None
        
    if df_lokasi is not None:
        list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)
        print(f"-> {len(list_semua_lokasi)} Objek berhasil direpresentasikan.")
        buat_peta_lokasi_folium(list_semua_lokasi, "peta_penugasan.html")
        
    print("--- Penugasan Selesai ---")