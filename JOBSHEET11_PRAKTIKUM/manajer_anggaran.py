# manajer_anggaran.py
import datetime
import pandas as pd
from model import Transaksi
import database  # Impor modul database kita


class AnggaranHarian:
    """Mengelola logika bisnis pengeluaran harian (Repository Pattern)."""

    _db_setup_done = False  # Flag setup DB hanya dicek sekali per sesi

    def __init__(self):
        if not AnggaranHarian._db_setup_done:
            print("[AnggaranHarian] Melakukan pengecekan/setup database awal...")
            if database.setup_database_initial():
                AnggaranHarian._db_setup_done = True
                print("[AnggaranHarian] Database siap.")
            else:
                print("[AnggaranHarian] KRITICAL: Setup database awal GAGAL!")

    # ------------------------------------------------------------------ #
    #  TAMBAH TRANSAKSI                                                    #
    # ------------------------------------------------------------------ #
    def tambah_transaksi(self, transaksi: Transaksi) -> bool:
        """Menyimpan satu objek Transaksi baru ke database."""
        if not isinstance(transaksi, Transaksi) or transaksi.jumlah <= 0:
            return False
        sql = ("INSERT INTO transaksi (deskripsi, jumlah, kategori, tanggal) "
               "VALUES (?, ?, ?, ?)")
        params = (
            transaksi.deskripsi,
            transaksi.jumlah,
            transaksi.kategori,
            transaksi.tanggal.strftime("%Y-%m-%d")
        )
        last_id = database.execute_query(sql, params)
        if last_id is not None:
            transaksi.id = last_id
            return True
        return False

    # ------------------------------------------------------------------ #
    #  HAPUS TRANSAKSI                                                   #
    # ------------------------------------------------------------------ #
    def hapus_transaksi(self, id_transaksi: int) -> bool:
        """
        Menghapus satu transaksi berdasarkan ID dari database.

        Parameter:
            id_transaksi (int): ID unik transaksi yang ingin dihapus.

        Return:
            True  – jika penghapusan berhasil dieksekusi tanpa error SQLite.
            False – jika id tidak valid, atau terjadi error saat eksekusi.

        Cara kerja:
            Memanggil database.execute_query() dengan perintah SQL:
            DELETE FROM transaksi WHERE id = ?
            Menggunakan placeholder (?) untuk mencegah SQL Injection.
            execute_query() mengembalikan None jika error, atau angka jika sukses.
        """
        if not isinstance(id_transaksi, int) or id_transaksi <= 0:
            print(f"[AnggaranHarian] ID tidak valid: {id_transaksi}")
            return False

        sql = "DELETE FROM transaksi WHERE id = ?"
        params = (id_transaksi,)
        hasil = database.execute_query(sql, params)

        # execute_query mengembalikan None jika ada error SQLite,
        # dan angka (lastrowid) jika perintah berhasil dieksekusi.
        if hasil is not None:
            print(f"[AnggaranHarian] Transaksi ID={id_transaksi} berhasil dihapus.")
            return True
        else:
            print(f"[AnggaranHarian] Gagal menghapus transaksi ID={id_transaksi}.")
            return False

    # ------------------------------------------------------------------ #
    #  READ DATA                                                           #
    # ------------------------------------------------------------------ #
    def get_semua_transaksi_obj(self) -> list:
        """Mengambil semua transaksi sebagai list objek Transaksi."""
        sql = ("SELECT id, deskripsi, jumlah, kategori, tanggal "
               "FROM transaksi ORDER BY tanggal DESC, id DESC")
        rows = database.fetch_query(sql, fetch_all=True)
        transaksi_list = []
        if rows:
            for row in rows:
                transaksi_list.append(
                    Transaksi(
                        id_transaksi=row['id'],
                        deskripsi=row['deskripsi'],
                        jumlah=row['jumlah'],
                        kategori=row['kategori'],
                        tanggal=row['tanggal']
                    )
                )
        return transaksi_list

    def get_dataframe_transaksi(self, filter_tanggal=None) -> pd.DataFrame:
        """
        Mengambil data transaksi sebagai DataFrame Pandas.
        PENTING: Kolom 'id' SELALU disertakan agar fitur hapus bisa bekerja.
        Kolom yang dikembalikan: id, tanggal, kategori, deskripsi, Jumlah (Rp)
        """
        # Pastikan kolom id ikut dalam SELECT
        query = "SELECT id, tanggal, kategori, deskripsi, jumlah FROM transaksi"
        params = None
        if filter_tanggal:
            query += " WHERE tanggal = ?"
            params = (filter_tanggal.strftime("%Y-%m-%d"),)
        query += " ORDER BY tanggal DESC, id DESC"

        df = database.get_dataframe(query, params=params)

        if df.empty:
            return df

        # Format kolom jumlah menjadi rupiah
        try:
            import locale
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
            df['Jumlah (Rp)'] = df['jumlah'].map(
                lambda x: locale.currency(x or 0, grouping=True, symbol='Rp ')[:-3]
            )
        except Exception:
            df['Jumlah (Rp)'] = df['jumlah'].map(
                lambda x: f"Rp {x or 0:,.0f}".replace(",", ".")
            )

        # Kembalikan kolom yang diperlukan — 'id' WAJIB ada untuk fitur hapus
        df = df[['id', 'tanggal', 'kategori', 'deskripsi', 'Jumlah (Rp)']]
        return df

    def hitung_total_pengeluaran(self, tanggal=None) -> float:
        """Menghitung total pengeluaran, opsional difilter per tanggal."""
        sql = "SELECT SUM(jumlah) FROM transaksi"
        params = None
        if tanggal:
            sql += " WHERE tanggal = ?"
            params = (tanggal.strftime("%Y-%m-%d"),)
        result = database.fetch_query(sql, params=params, fetch_all=False)
        if result and result[0] is not None:
            return float(result[0])
        return 0.0

    def get_pengeluaran_per_kategori(self, tanggal=None) -> dict:
        """Menghitung total pengeluaran per kategori."""
        hasil = {}
        sql = "SELECT kategori, SUM(jumlah) FROM transaksi"
        params = []
        if tanggal:
            sql += " WHERE tanggal = ?"
            params.append(tanggal.strftime("%Y-%m-%d"))
        sql += " GROUP BY kategori HAVING SUM(jumlah) > 0 ORDER BY SUM(jumlah) DESC"
        rows = database.fetch_query(
            sql,
            params=tuple(params) if params else None,
            fetch_all=True
        )
        if rows:
            for row in rows:
                kategori = row['kategori'] if row['kategori'] else "Lainnya"
                jumlah = float(row[1]) if row[1] is not None else 0.0
                hasil[kategori] = jumlah
        return hasil