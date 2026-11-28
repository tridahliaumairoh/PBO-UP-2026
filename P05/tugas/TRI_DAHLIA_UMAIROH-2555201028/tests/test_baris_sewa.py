import pytest

from src.model.alat_tani import AlatTani
from src.model.baris_sewa import BarisSewa


def buat_alat() -> AlatTani:
    return AlatTani("AT01", "Traktor", 100_000)


def test_baris_sewa_valid() -> None:
    baris = BarisSewa(buat_alat(), 3)
    assert baris.jumlah_hari == 3
    assert baris.kode_alat == "AT01"
    assert baris.nama_alat == "Traktor"


def test_alat_dapat_diakses() -> None:
    alat = buat_alat()
    baris = BarisSewa(alat, 2)
    assert baris.alat is alat


def test_tarif_disimpan_sebagai_snapshot() -> None:
    alat = buat_alat()
    baris = BarisSewa(alat, 2)
    alat.tarif_harian = 200_000
    assert baris.tarif_saat_sewa == 100_000


def test_subtotal_menggunakan_tarif_snapshot() -> None:
    alat = buat_alat()
    baris = BarisSewa(alat, 3)
    alat.tarif_harian = 200_000
    assert baris.subtotal() == 300_000


def test_jumlah_hari_nol_ditolak() -> None:
    with pytest.raises(ValueError):
        BarisSewa(buat_alat(), 0)


def test_jumlah_hari_negatif_ditolak() -> None:
    with pytest.raises(ValueError):
        BarisSewa(buat_alat(), -1)


def test_baris_nota_memuat_nama_alat() -> None:
    baris = BarisSewa(buat_alat(), 2)
    assert "Traktor" in baris.baris_nota()


def test_baris_nota_memuat_subtotal() -> None:
    baris = BarisSewa(buat_alat(), 2)
    assert "Rp200.000" in baris.baris_nota()


def test_kode_alat_snapshot_tidak_berubah() -> None:
    alat = buat_alat()
    baris = BarisSewa(alat, 1)
    assert baris.kode_alat == "AT01"


def test_nama_alat_snapshot_tidak_berubah() -> None:
    baris = BarisSewa(buat_alat(), 1)
    assert baris.nama_alat == "Traktor"
