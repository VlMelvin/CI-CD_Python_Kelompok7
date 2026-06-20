import pytest
from ParkApp import hitung_biaya_parkir


# ============================================================
# TEST SUITE: Continuous Testing - Sistem Parkir Kampus
# Dibuat untuk pipeline CI/CD GitHub Actions
# ============================================================


class TestJenisKendaraanTidakValid:
    """Pengujian validasi input jenis kendaraan."""

    def test_jenis_kendaraan_tidak_valid_mengembalikan_error(self):
        hasil = hitung_biaya_parkir("Bus", 2, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_jenis_kendaraan_string_kosong(self):
        hasil = hitung_biaya_parkir("", 2, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_jenis_kendaraan_huruf_kecil_tidak_valid(self):
        # Input harus "Motor" atau "Mobil" (kapital), bukan "motor"
        hasil = hitung_biaya_parkir("motor", 2, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_pesan_error_jenis_kendaraan(self):
        hasil = hitung_biaya_parkir("Sepeda", 1, "Tidak Hilang")
        assert "tidak valid" in hasil["pesan"].lower()


class TestLamaParkir:
    """Pengujian validasi input lama parkir."""

    def test_lama_parkir_nol_tidak_valid(self):
        hasil = hitung_biaya_parkir("Motor", 0, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_lama_parkir_25_tidak_valid(self):
        hasil = hitung_biaya_parkir("Motor", 25, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_lama_parkir_negatif_tidak_valid(self):
        hasil = hitung_biaya_parkir("Motor", -1, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_lama_parkir_string_tidak_valid(self):
        hasil = hitung_biaya_parkir("Motor", "dua", "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_lama_parkir_float_tidak_valid(self):
        hasil = hitung_biaya_parkir("Motor", 1.5, "Tidak Hilang")
        assert hasil["status"] == "Error"

    def test_lama_parkir_1_valid(self):
        hasil = hitung_biaya_parkir("Motor", 1, "Tidak Hilang")
        assert hasil["status"] == "Sukses"

    def test_lama_parkir_24_valid(self):
        hasil = hitung_biaya_parkir("Motor", 24, "Tidak Hilang")
        assert hasil["status"] == "Sukses"


class TestStatusTiket:
    """Pengujian validasi status tiket."""

    def test_status_tiket_tidak_valid(self):
        hasil = hitung_biaya_parkir("Motor", 2, "Rusak")
        assert hasil["status"] == "Error"

    def test_status_tiket_string_kosong(self):
        hasil = hitung_biaya_parkir("Motor", 2, "")
        assert hasil["status"] == "Error"

    def test_status_tiket_hilang_valid(self):
        hasil = hitung_biaya_parkir("Motor", 2, "Hilang")
        assert hasil["status"] == "Sukses"

    def test_status_tiket_tidak_hilang_valid(self):
        hasil = hitung_biaya_parkir("Motor", 2, "Tidak Hilang")
        assert hasil["status"] == "Sukses"


class TestBiayaMotor:
    """Pengujian perhitungan biaya parkir untuk Motor."""

    def test_motor_1_jam(self):
        # Tarif awal Motor: Rp3.000
        hasil = hitung_biaya_parkir("Motor", 1, "Tidak Hilang")
        assert hasil["status"] == "Sukses"
        assert hasil["total_biaya"] == 3000

    def test_motor_2_jam(self):
        # 3000 + (2-1)*1000 = 4000
        hasil = hitung_biaya_parkir("Motor", 2, "Tidak Hilang")
        assert hasil["total_biaya"] == 4000

    def test_motor_5_jam(self):
        # 3000 + (5-1)*1000 = 7000
        hasil = hitung_biaya_parkir("Motor", 5, "Tidak Hilang")
        assert hasil["total_biaya"] == 7000

    def test_motor_biaya_maksimum(self):
        # Batas maksimum Motor: Rp12.000
        # Dicapai pada jam ke-10: 3000 + 9*1000 = 12000
        hasil = hitung_biaya_parkir("Motor", 10, "Tidak Hilang")
        assert hasil["total_biaya"] == 12000

    def test_motor_melebihi_batas_maksimum_tetap_12000(self):
        # Jam ke-24 seharusnya tidak melebihi Rp12.000
        hasil = hitung_biaya_parkir("Motor", 24, "Tidak Hilang")
        assert hasil["total_biaya"] == 12000

    def test_motor_tiket_hilang_1_jam(self):
        # 3000 + denda 20000 = 23000
        hasil = hitung_biaya_parkir("Motor", 1, "Hilang")
        assert hasil["total_biaya"] == 23000

    def test_motor_tiket_hilang_batas_maksimum(self):
        # Maksimum motor (12000) + denda (20000) = 32000
        hasil = hitung_biaya_parkir("Motor", 24, "Hilang")
        assert hasil["total_biaya"] == 32000


class TestBiayaMobil:
    """Pengujian perhitungan biaya parkir untuk Mobil."""

    def test_mobil_1_jam(self):
        # Tarif awal Mobil: Rp5.000
        hasil = hitung_biaya_parkir("Mobil", 1, "Tidak Hilang")
        assert hasil["status"] == "Sukses"
        assert hasil["total_biaya"] == 5000

    def test_mobil_2_jam(self):
        # 5000 + (2-1)*2000 = 7000
        hasil = hitung_biaya_parkir("Mobil", 2, "Tidak Hilang")
        assert hasil["total_biaya"] == 7000

    def test_mobil_5_jam(self):
        # 5000 + (5-1)*2000 = 13000
        hasil = hitung_biaya_parkir("Mobil", 5, "Tidak Hilang")
        assert hasil["total_biaya"] == 13000

    def test_mobil_biaya_maksimum(self):
        # Batas maksimum Mobil: Rp30.000
        # Dicapai pada jam ke-13: 5000 + 12*2000 = 29000 (belum), jam ke-14: 31000 -> kena cap
        hasil = hitung_biaya_parkir("Mobil", 14, "Tidak Hilang")
        assert hasil["total_biaya"] == 30000

    def test_mobil_melebihi_batas_maksimum_tetap_30000(self):
        hasil = hitung_biaya_parkir("Mobil", 24, "Tidak Hilang")
        assert hasil["total_biaya"] == 30000

    def test_mobil_tiket_hilang_1_jam(self):
        # 5000 + denda 20000 = 25000
        hasil = hitung_biaya_parkir("Mobil", 1, "Hilang")
        assert hasil["total_biaya"] == 25000

    def test_mobil_tiket_hilang_batas_maksimum(self):
        # Maksimum mobil (30000) + denda (20000) = 50000
        hasil = hitung_biaya_parkir("Mobil", 24, "Hilang")
        assert hasil["total_biaya"] == 50000


class TestStrukturReturnValue:
    """Pengujian struktur nilai yang dikembalikan fungsi."""

    def test_sukses_memiliki_key_status(self):
        hasil = hitung_biaya_parkir("Motor", 1, "Tidak Hilang")
        assert "status" in hasil

    def test_sukses_memiliki_key_pesan(self):
        hasil = hitung_biaya_parkir("Motor", 1, "Tidak Hilang")
        assert "pesan" in hasil

    def test_sukses_memiliki_key_total_biaya(self):
        hasil = hitung_biaya_parkir("Motor", 1, "Tidak Hilang")
        assert "total_biaya" in hasil

    def test_error_tidak_memiliki_total_biaya(self):
        hasil = hitung_biaya_parkir("Bus", 1, "Tidak Hilang")
        assert "total_biaya" not in hasil

    def test_total_biaya_adalah_integer(self):
        hasil = hitung_biaya_parkir("Mobil", 3, "Tidak Hilang")
        assert isinstance(hasil["total_biaya"], int)
