"""Model transaksi penyewaan alat pertanian."""

from src.model.alat_tani import AlatTani
from src.model.baris_sewa import BarisSewa
from src.model.penyewa import Penyewa


class Sewa:
    """Transaksi penyewaan yang dimiliki oleh seorang penyewa."""

    BATAS_ALAT_PER_SEWA = 10

    def __init__(self, nomor: str, penyewa: Penyewa) -> None:
        if not nomor.strip():
            raise ValueError("nomor sewa tidak boleh kosong")

        self._nomor = nomor
        self._penyewa = penyewa
        self._baris: list[BarisSewa] = []

    @property
    def nomor(self) -> str:
        return self._nomor

    @property
    def penyewa(self) -> Penyewa:
        return self._penyewa

    @property
    def baris(self) -> tuple[BarisSewa, ...]:
        return tuple(self._baris)

    def tambah_alat(self, alat: AlatTani, jumlah_hari: int) -> None:
        if len(self._baris) >= self.BATAS_ALAT_PER_SEWA:
            raise ValueError("jumlah alat sudah mencapai batas maksimal")

        for baris in self._baris:
            if baris.kode_alat == alat.kode:
                raise ValueError(f"alat {alat.kode} sudah ditambahkan")

        self._baris.append(BarisSewa(alat, jumlah_hari))

    def jumlah_alat(self) -> int:
        return len(self._baris)

    def total(self) -> int:
        return sum(baris.subtotal() for baris in self._baris)

    def nota(self) -> str:
        garis = "-" * 68
        rincian = "\n".join(
            baris.baris_nota() for baris in self._baris
        )
        total = AlatTani.format_rupiah(self.total())

        return (
            f"NOTA SEWA {self._nomor}\n"
            f"Kepada: {self._penyewa.identitas()}\n"
            f"{garis}\n"
            f"{rincian}\n"
            f"{garis}\n"
            f"{'TOTAL':>48}: {total:>12}"
        )
