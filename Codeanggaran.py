"""
Optimasi Pemilihan Menu Kantin Berdasarkan Anggaran Mahasiswa
Menggunakan Algoritma Greedy

Program ini menggunakan algoritma greedy untuk memaksimalkan nilai gizi
atau kepuasan dari menu yang dipilih dalam batas anggaran yang tersedia.
"""

class MenuItem:
    """Kelas untuk merepresentasikan item menu kantin"""

    def __init__(self, nama, harga, nilai_gizi, kalori=0):
        self.nama = nama
        self.harga = harga
        self.nilai_gizi = nilai_gizi  # Bisa berupa skor kepuasan atau nilai nutrisi
        self.kalori = kalori
        self.rasio = nilai_gizi / harga  # Rasio nilai gizi per harga (greedy metric)

    def __repr__(self):
        return f"{self.nama} (Rp{self.harga:,}, Nilai: {self.nilai_gizi}, Rasio: {self.rasio:.2f})"


def algoritma_greedy_menu(daftar_menu, anggaran):
    """
    Algoritma Greedy untuk memilih menu optimal berdasarkan anggaran

    Args:
        daftar_menu: List dari objek MenuItem
        anggaran: Budget yang tersedia (dalam Rupiah)

    Returns:
        tuple: (menu_terpilih, total_harga, total_nilai_gizi, total_kalori)
    """
    # Urutkan menu berdasarkan rasio nilai_gizi/harga (descending)
    menu_terurut = sorted(daftar_menu, key=lambda x: x.rasio, reverse=True)

    menu_terpilih = []
    total_harga = 0
    total_nilai_gizi = 0
    total_kalori = 0

    print("\n" + "="*70)
    print("PROSES ALGORITMA GREEDY")
    print("="*70)
    print(f"Anggaran tersedia: Rp{anggaran:,}\n")

    for menu in menu_terurut:
        if total_harga + menu.harga <= anggaran:
            menu_terpilih.append(menu)
            total_harga += menu.harga
            total_nilai_gizi += menu.nilai_gizi
            total_kalori += menu.kalori

            print(f" Memilih: {menu.nama}")
            print(f"  Harga: Rp{menu.harga:,} | Nilai: {menu.nilai_gizi} | Rasio: {menu.rasio:.2f}")
            print(f"  Sisa anggaran: Rp{anggaran - total_harga:,}\n")
        else:
            print(f" Melewati: {menu.nama} (Harga: Rp{menu.harga:,} - Melebihi anggaran)")

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
    print(f"\nTotal Nilai Gizi/Kepuasan: {total_nilai_gizi}")
    print(f"Total Kalori: {total_kalori} kkal")

    print("\n" + "-"*70)
    print("MENU YANG TERPILIH:")
    print("-"*70)
    print(f"{'No':<4} {'Nama Menu':<25} {'Harga':<15} {'Nilai':<10} {'Rasio':<10}")
    print("-"*70)

    for idx, menu in enumerate(menu_terpilih, 1):
        print(f"{idx:<4} {menu.nama:<25} Rp{menu.harga:<13,} {menu.nilai_gizi:<10} {menu.rasio:<10.2f}")

    print("="*70)
    print(f"\nEfisiensi Anggaran: {(total_harga/anggaran)*100:.1f}%")
    print(f"Rata-rata Nilai per Menu: {total_nilai_gizi/len(menu_terpilih):.2f}")
    print("="*70)


def main():
    """Fungsi utama program"""

    print("\n" + "="*70)
    print("OPTIMASI PEMILIHAN MENU KANTIN")
    print("Menggunakan Algoritma Greedy")
    print("="*70)

    # Data menu kantin (bisa disesuaikan dengan menu kantin sebenarnya)
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

    # Input anggaran dari user
    print("\n" + "-"*70)
    try:
        anggaran = int(input("\nMasukkan anggaran Anda (Rp): "))

        if anggaran <= 0:
            print("Anggaran harus lebih dari 0!")
            return

        # Jalankan algoritma greedy
        menu_terpilih, total_harga, total_nilai_gizi, total_kalori = algoritma_greedy_menu(
            daftar_menu, anggaran
        )

        # Tampilkan hasil
        tampilkan_hasil(menu_terpilih, total_harga, total_nilai_gizi, total_kalori, anggaran)

    except ValueError:
        print("Input tidak valid! Masukkan angka yang benar.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    main()
