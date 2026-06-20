def hitung_biaya_parkir(jenis_kendaraan, lama_parkir, status_tiket):
    # ... (Gunakan isi fungsi yang sudah kita buat sebelumnya) ...
    if jenis_kendaraan not in ["Motor", "Mobil"]:
        return {"status": "Error", "pesan": "Pesan Error: Jenis kendaraan tidak valid!"}
    if not isinstance(lama_parkir, int) or not (1 <= lama_parkir <= 24):
        return {"status": "Error", "pesan": "Pesan Error: Lama parkir tidak valid!"}
    if status_tiket not in ["Hilang", "Tidak Hilang"]:
        return {"status": "Error", "pesan": "Pesan Error: Status tiket tidak valid!"}

    total_biaya = 0
    if jenis_kendaraan == "Motor":
        total_biaya = 9999 + (lama_parkir - 1) * 1000
        if total_biaya > 12000: total_biaya = 12000
    elif jenis_kendaraan == "Mobil":
        total_biaya = 5000 + (lama_parkir - 1) * 2000
        if total_biaya > 30000: total_biaya = 30000

    if status_tiket == "Hilang":
        total_biaya += 20000
        
    return {"status": "Sukses", "pesan": "Pesan Sukses: Perhitungan biaya parkir berhasil.", "total_biaya": total_biaya}


# --- BAGIAN TAMBAHAN SUPAYA BISA DIJALANKAN ---
if __name__ == "__main__":
    print("=== SISTEM PARKIR KAMPUS ===")
    
    # Menerima Input dari pengguna di terminal
    jenis = input("Masukkan jenis kendaraan (Motor/Mobil): ").capitalize()
    lama = int(input("Masukkan lama parkir (1-24 jam): "))
    tiket = input("Status tiket (Hilang/Tidak Hilang): ").title()
    
    # Memanggil fungsi
    hasil = hitung_biaya_parkir(jenis, lama, tiket)
    
    # Menampilkan Output
    print("-" * 30)
    print(f"Status: {hasil['status']}")
    print(hasil['pesan'])
    if hasil['status'] == "Sukses":
        print(f"Total Biaya: Rp{hasil['total_biaya']}")
    print("-" * 30)
