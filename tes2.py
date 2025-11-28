
import sys
import os


class MenuItem:
    """Kelas untuk merepresentasikan item menu kantin"""

    def __init__(self, nama, harga, nilai_gizi, kalori=0):
        self.nama = nama
        self.harga = harga
        self.nilai_gizi = nilai_gizi
        self.kalori = kalori
        self.rasio = kalori / harga

    def __repr__(self):
        return f"{self.nama} - Rp{self.harga:,}"


def algoritma_greedy_menu(daftar_menu, anggaran, jumlah_makanan=None):
    """
    Algoritma Greedy untuk memilih menu optimal berdasarkan anggaran dan kalori

    Args:
        daftar_menu: List dari objek MenuItem
        anggaran: Budget yang tersedia (dalam Rupiah)
        jumlah_makanan: Jumlah maksimal makanan yang diinginkan (opsional)

    Returns:
        tuple: (menu_terpilih, total_harga, total_nilai_gizi, total_kalori)
    """
    menu_terurut = sorted(daftar_menu, key=lambda x: x.rasio, reverse=True)

    menu_terpilih = []
    total_harga = 0
    total_nilai_gizi = 0
    total_kalori = 0

    print("\n" + "="*70)
    print("PROSES ALGORITMA GREEDY (Berdasarkan Rasio Kalori/Harga)")
    print("="*70)
    print(f"Anggaran tersedia: Rp{anggaran:,}")
    if jumlah_makanan:
        print(f"Jumlah makanan maksimal: {jumlah_makanan} item")
    print()

    for menu in menu_terurut:
        if jumlah_makanan and len(menu_terpilih) >= jumlah_makanan:
            print(f"✓ Sudah mencapai jumlah makanan maksimal ({jumlah_makanan} item)")
            break

        if total_harga + menu.harga <= anggaran:
            menu_terpilih.append(menu)
            total_harga += menu.harga
            total_nilai_gizi += menu.nilai_gizi
            total_kalori += menu.kalori

            print(f"✓ Memilih: {menu.nama}")
            print(f"  Harga: Rp{menu.harga:,} | Kalori: {menu.kalori} kkal | Rasio: {menu.rasio:.4f} kkal/Rp")
            print(f"  Sisa anggaran: Rp{anggaran - total_harga:,}\n")
        else:
            print(f"✗ Melewati: {menu.nama} (Harga: Rp{menu.harga:,} - Melebihi anggaran)")

    return menu_terpilih, total_harga, total_nilai_gizi, total_kalori


def tampilkan_hasil(menu_terpilih, total_harga, total_nilai_gizi, total_kalori, anggaran):
    """Menampilkan hasil optimasi dalam format yang rapi"""

    print("\n" + "="*70)
    print("HASIL OPTIMASI PEMILIHAN MENU")
    print("="*70)

    if not menu_terpilih:
        print("Tidak ada menu yang dapat dipilih dengan anggaran tersebut.")
        return

    print(f"\nAnggaran: Rp{anggaran:,}")
    print(f"Total Pengeluaran: Rp{total_harga:,}")
    print(f"Sisa Anggaran: Rp{anggaran - total_harga:,}")
    print(f"\nJumlah Makanan: {len(menu_terpilih)} item")
    print(f"Total Kalori: {total_kalori} kkal")

    print("\n" + "-"*70)
    print("MENU YANG TERPILIH:")
    print("-"*70)
    print(f"{'No':<4} {'Nama Menu':<30} {'Harga':<15} {'Kalori':<10}")
    print("-"*70)

    for idx, menu in enumerate(menu_terpilih, 1):
        print(f"{idx:<4} {menu.nama:<30} Rp{menu.harga:<13,} {menu.kalori} kkal")

    print("="*70)
    print(f"\nEfisiensi Anggaran: {(total_harga/anggaran)*100:.1f}%")
    print(f"Rata-rata Kalori per Menu: {total_kalori/len(menu_terpilih):.1f} kkal")
    print("="*70)


def input_anggaran():
    """Fungsi untuk input anggaran dengan format pemisah ribuan"""
    print("\nMasukkan anggaran Anda (bisa pakai titik/koma sebagai pemisah)")
    print("Contoh: 50.000 atau 50000")
    anggaran_str = input("\nAnggaran (Rp): ")

    anggaran_str = anggaran_str.replace(".", "").replace(" ", "").replace(",", "")

    return int(anggaran_str)


def main():
    """Fungsi utama program"""

    print("\n" + "="*70)
    print("OPTIMASI PEMILIHAN MENU KANTIN")
    print("Menggunakan Algoritma Greedy (Berdasarkan Kalori)")
    print("="*70)

    daftar_menu = [
        MenuItem("Nasi Goreng", 15000, 85, 600),
        MenuItem("Mie Ayam", 12000, 70, 550),
        MenuItem("Ayam Geprek + Nasi", 18000, 90, 750),
        MenuItem("Soto Ayam", 13000, 75, 500),
        MenuItem("Nasi Pecel", 10000, 65, 450),
        MenuItem("Bakso", 12000, 68, 480),
        MenuItem("Gado-gado", 11000, 72, 400),
        MenuItem("Nasi Uduk", 9000, 60, 520),
        MenuItem("Bubur Ayam", 8000, 55, 350),
        MenuItem("Nasi Kuning", 10000, 62, 480),
        MenuItem("Es Teh Manis", 3000, 15, 100),
        MenuItem("Es Jeruk", 4000, 20, 120),
        MenuItem("Air Mineral", 2000, 10, 0),
        MenuItem("Jus Alpukat", 8000, 35, 200),
        MenuItem("Pisang Goreng", 5000, 25, 250),
    ]

    print("\nDAFTAR MENU KANTIN:")
    print("-"*70)
    for menu in daftar_menu:
        print(f"  {menu}")

    print("\n" + "-"*70)
    try:
        anggaran = input_anggaran()

        if anggaran <= 0:
            print("Anggaran harus lebih dari 0!")
            return

        jumlah_input = input("Berapa jumlah makanan yang ingin Anda beli? (tekan Enter untuk unlimited): ")
        jumlah_makanan = None
        if jumlah_input.strip():
            jumlah_makanan = int(jumlah_input)
            if jumlah_makanan <= 0:
                print("Jumlah makanan harus lebih dari 0!")
                return

        menu_terpilih, total_harga, total_nilai_gizi, total_kalori = algoritma_greedy_menu(
            daftar_menu, anggaran, jumlah_makanan
        )

        tampilkan_hasil(menu_terpilih, total_harga, total_nilai_gizi, total_kalori, anggaran)

    except ValueError:
        print("Input tidak valid! Masukkan angka yang benar.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    main()
