from abc import ABC, abstractmethod

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

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"

    def __str__(self) -> str:
        return f"{self.nama} [{type(self).__name__}]"

class TempatWisata(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class Kuliner(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, menu_andalan: str):
        super().__init__(nama, latitude, longitude)
        self.menu_andalan = str(menu_andalan) if menu_andalan else "Tidak diketahui"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>Menu Andalan: {self.menu_andalan}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

class TempatIbadah(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, agama: str = "Umum", deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"

if __name__ == "__main__":
    print("--- Memulai Praktikum 3: Mendesain Kelas OOP ---")
    # Instansiasi manual untuk membuktikan struktur kelas bekerja objeknya
    wisata_test = TempatWisata("Lawang Sewu", -6.9840, 110.4105, "Wisata Sejarah", "Gedung peninggalan Belanda.")
    print("Representasi Objek:")
    print(repr(wisata_test))
    print("\n--- Praktikum 3 Selesai ---")