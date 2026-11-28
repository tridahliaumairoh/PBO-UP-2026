from src.model.alamat import Alamat
from src.model.alat_tani import AlatTani
from src.model.penyewa import Penyewa
from src.model.baris_sewa import BarisSewa
from src.model.sewa import Sewa
from src.model.petugas import IdentitasPetugas, Petugas


def main() -> None:
    alamat = Alamat("Kampung Baru", "Kuok", "Kuok")
    penyewa = Penyewa("Budi Santoso", "1401010101010001", alamat)
    alat = AlatTani("AT01", "Traktor", 100_000)
    alat2 = AlatTani("AT02", "Combine Harvester", 250_000)
    petugas = Petugas("PT01", "Andi", IdentitasPetugas("andi@example.com"))

    print("=== DATA PENYEWA ===")
    print(penyewa.identitas())

    print("\n=== DATA PETUGAS ===")
    print(f"Petugas: {petugas.nama} - {petugas.status}")

    print("\n=== PENGUJIAN BARIS SEWA ===")
    baris = BarisSewa(alat, 3)
    print(f"Alat: {baris.nama_alat}")
    print(f"Jumlah hari: {baris.jumlah_hari}")
    print(f"Subtotal: {AlatTani.format_rupiah(baris.subtotal())}")

    print("\n=== PENGUJIAN SEWA ===")
    sewa = Sewa("SW001", penyewa)
    sewa.tambah_alat(alat, 3)
    sewa.tambah_alat(alat2, 2)
    print(f"Nomor sewa: {sewa.nomor}")
    print(f"Jumlah alat: {sewa.jumlah_alat()}")
    print(f"Total: {AlatTani.format_rupiah(sewa.total())}")

    print("\n=== NOTA PENYEWAAN ===")
    print(sewa.nota())


if __name__ == "__main__":
    main()
