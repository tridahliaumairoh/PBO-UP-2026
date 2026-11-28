import pytest

from src.model.alamat import Alamat
from src.model.alat_tani import AlatTani
from src.model.penyewa import Penyewa
from src.model.sewa import Sewa


def buat_penyewa() -> Penyewa:
    alamat = Alamat("Dusun I", "Kuok", "Kuok")
    return Penyewa("Budi", "1401010101010001", alamat)


def buat_alat(kode: str = "AT01") -> AlatTani:
    return AlatTani(kode, "Traktor", 100_000)


def buat_sewa() -> Sewa:
    return Sewa("SW001", buat_penyewa())


def test_sewa_valid() -> None:
    sewa = buat_sewa()
    assert sewa.nomor == "SW001"
    assert sewa.penyewa is not None


def test_nomor_kosong_ditolak() -> None:
    with pytest.raises(ValueError):
        Sewa("   ", buat_penyewa())


def test_baris_awalnya_kosong() -> None:
    assert buat_sewa().baris == ()


def test_tambah_satu_alat() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat(), 2)
    assert sewa.jumlah_alat() == 1


def test_tambah_beberapa_alat() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat("AT01"), 2)
    sewa.tambah_alat(buat_alat("AT02"), 3)
    assert sewa.jumlah_alat() == 2


def test_duplikasi_kode_alat_ditolak() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat("AT01"), 2)
    with pytest.raises(ValueError):
        sewa.tambah_alat(buat_alat("AT01"), 3)


def test_batas_maksimal_sepuluh_alat() -> None:
    sewa = buat_sewa()
    for nomor in range(10):
        sewa.tambah_alat(buat_alat(f"AT{nomor:02}"), 1)
    assert sewa.jumlah_alat() == 10


def test_alat_ke_sebelas_ditolak() -> None:
    sewa = buat_sewa()
    for nomor in range(10):
        sewa.tambah_alat(buat_alat(f"AT{nomor:02}"), 1)
    with pytest.raises(ValueError):
        sewa.tambah_alat(buat_alat("AT10"), 1)


def test_jumlah_alat_awal_nol() -> None:
    assert buat_sewa().jumlah_alat() == 0


def test_total_sewa_kosong() -> None:
    assert buat_sewa().total() == 0


def test_total_satu_alat() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat(), 3)
    assert sewa.total() == 300_000


def test_total_beberapa_alat() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat("AT01"), 3)
    sewa.tambah_alat(AlatTani("AT02", "Mesin", 200_000), 2)
    assert sewa.total() == 700_000


def test_baris_berupa_tuple() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat(), 1)
    assert isinstance(sewa.baris, tuple)


def test_nota_memuat_nomor_sewa() -> None:
    assert "SW001" in buat_sewa().nota()


def test_nota_memuat_identitas_penyewa() -> None:
    assert "Budi" in buat_sewa().nota()


def test_nota_memuat_total() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat(), 2)
    assert "Rp200.000" in sewa.nota()


def test_nota_memuat_nama_alat() -> None:
    sewa = buat_sewa()
    sewa.tambah_alat(buat_alat(), 1)
    assert "Traktor" in sewa.nota()


def test_tarif_snapshot_dipakai_dalam_total() -> None:
    alat = buat_alat()
    sewa = buat_sewa()
    sewa.tambah_alat(alat, 2)
    alat.tarif_harian = 200_000
    assert sewa.total() == 200_000
