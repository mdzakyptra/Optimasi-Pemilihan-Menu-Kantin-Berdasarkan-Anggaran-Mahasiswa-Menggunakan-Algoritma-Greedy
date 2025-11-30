
import sys
import os


class MenuItem:

    def __init__(self, nama, harga, nilai_gizi, kalori=0):
        self.nama = nama
        self.harga = harga
        self.nilai_gizi = nilai_gizi
        self.kalori = kalori
        self.rasio = kalori / harga

    def __repr__(self):
        return f"{self.nama} - Rp{self.harga:,}"


def algoritma_greedy_menu(daftar_menu, anggaran, jumlah_makanan=None):
    menu_terurut = sorted(daftar_menu, key=lambda x: x.kalori, reverse=True)

    menu_terpilih = []
    total_harga = 0
    total_nilai_gizi = 0
    total_kalori = 0

    print("\n" + "="*70)
    print("PROSES ALGORITMA GREEDY (Berdasarkan Kalori Maksimum)")
    print("="*70)
    print(f"Anggaran tersedia: Rp{anggaran:,}")
    if jumlah_makanan:
        print(f"Jumlah makanan maksimal: {jumlah_makanan} item")
    print()

    for menu in menu_terurut:
        if total_harga + menu.harga <= anggaran:
            if jumlah_makanan and len(menu_terpilih) >= jumlah_makanan:
                print(f"✗ Melewati: {menu.nama} (Sudah mencapai jumlah maksimal {jumlah_makanan} item)")
                continue

            menu_terpilih.append(menu)
            total_harga += menu.harga
            total_nilai_gizi += menu.nilai_gizi
            total_kalori += menu.kalori

            print(f"✓ Memilih: {menu.nama}")
            print(f"  Harga: Rp{menu.harga:,} | Kalori: {menu.kalori} kkal | Rasio: {menu.rasio:.4f} kkal/Rp")
            print(f"  Sisa anggaran: Rp{anggaran - total_harga:,}\n")

    print(f"\n✓ Selesai memilih menu. Total pengeluaran: Rp{total_harga:,}")
    print(f"  Sisa anggaran: Rp{anggaran - total_harga:,}")

    return menu_terpilih, total_harga, total_nilai_gizi, total_kalori


def jelaskan_top_3_pilihan(menu_terpilih):
    print("\n" + "="*70)
    print("PENJELASAN MENGAPA SISTEM MEMILIH MENU TERSEBUT")
    print("="*70)

    if not menu_terpilih:
        print("Tidak ada menu yang terpilih.")
        return

    top_3 = menu_terpilih[:3]

    for i, menu in enumerate(top_3, 1):
        print(f"\n{i}. {menu.nama}")
        print(f"   Harga: Rp{menu.harga:,}")
        print(f"   Kalori: {menu.kalori} kkal")
        print(f"   Rasio Efisiensi: {menu.rasio:.4f} kkal/Rp")
        print(f"   \n   Alasan Pemilihan:")

        if menu.rasio >= 0.06:
            efisiensi = "SANGAT TINGGI"
            keterangan = "memberikan kalori yang sangat banyak dengan harga yang murah"
        elif menu.rasio >= 0.04:
            efisiensi = "TINGGI"
            keterangan = "memberikan kalori yang cukup banyak dengan harga yang terjangkau"
        elif menu.rasio >= 0.02:
            efisiensi = "SEDANG"
            keterangan = "memberikan kalori yang cukup dengan harga yang wajar"
        else:
            efisiensi = "RENDAH"
            keterangan = "dipilih karena masih sesuai anggaran meskipun efisiensi rendah"

        print(f"   - Menu ini memiliki rasio efisiensi kalori/harga {efisiensi}")
        print(f"   - Setiap Rp1.000 yang dikeluarkan menghasilkan {menu.rasio*1000:.2f} kkal")
        print(f"   - Menu ini {keterangan}")

        if menu.harga <= 5000:
            print(f"   - Harga sangat terjangkau (≤ Rp5.000)")
        elif menu.harga <= 10000:
            print(f"   - Harga terjangkau (Rp5.000 - Rp10.000)")
        elif menu.harga <= 15000:
            print(f"   - Harga sedang (Rp10.000 - Rp15.000)")
        else:
            print(f"   - Harga premium (> Rp15.000) namun sebanding dengan kalori yang didapat")

    if len(menu_terpilih) > 3:
        print(f"\n   ... dan {len(menu_terpilih) - 3} menu lainnya dipilih dengan prinsip yang sama")

    print("\n" + "="*70)


def tampilkan_hasil(menu_terpilih, total_harga, total_nilai_gizi, total_kalori, anggaran):

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
    print("\nMasukkan anggaran Anda (bisa pakai titik/koma sebagai pemisah)")
    print("Contoh: 50.000 atau 50000")
    anggaran_str = input("\nAnggaran (Rp): ")

    anggaran_str = anggaran_str.replace(".", "").replace(" ", "").replace(",", "")

    return int(anggaran_str)


def main():

    print("\n" + "="*70)
    print("OPTIMASI PEMILIHAN MENU KANTIN")
    print("Menggunakan Algoritma Greedy (Berdasarkan Kalori)")
    print("="*70)

    daftar_menu = [
        MenuItem("Nasi Goreng", 15000, 70, 330),
        MenuItem("Mie Goreng", 12000, 65, 350),
        MenuItem("Ayam Goreng + Nasi", 15000, 80, 450),
        MenuItem("Nasi Katsu", 12000, 75, 480),
        MenuItem("Soto Ayam + Nasi", 10000, 65, 350),
        MenuItem("Soto Ayam", 8000, 55, 150),
        MenuItem("Gado-Gado", 10000, 72, 490),
        MenuItem("Nasi Katsu Asam Manis", 15000, 82, 520),
        MenuItem("Nasi Katsu Black Pepper", 15000, 81, 510),
        MenuItem("Mie Ayam", 12000, 68, 400),
        MenuItem("Bakso", 10000, 62, 325),
        MenuItem("Nasi Pecel", 10000, 75, 500),
        MenuItem("Nasi Sayur", 15000, 70, 380),
        MenuItem("Nasi Goreng Spesial", 20000, 78, 450),
        MenuItem("Nasi Pecel Telor", 13000, 82, 580),
        MenuItem("Batagor (isi 10)", 10000, 78, 580),
        MenuItem("Nasi Campur", 10000, 88, 680),
        MenuItem("Sup Ayam + Nasi", 8000, 58, 280),
        MenuItem("Tempe Goreng", 1000, 32, 80),
        MenuItem("Tempura", 1000, 35, 90),
        MenuItem("Teh Manis (hangat/dingin)", 3000, 20, 90),
        MenuItem("Kopi Tubruk (gula)", 5000, 22, 85),
        MenuItem("Jus Mangga", 5000, 32, 150),
        MenuItem("Jus Jeruk", 5000, 28, 110),
        MenuItem("Coca Cola/Fanta/Sprite", 7000, 30, 140),
        MenuItem("Air Mineral (600 ml)", 3000, 10, 0),
        MenuItem("Susu", 5000, 32, 150),
        MenuItem("Teh Tawar", 2000, 8, 2),
        MenuItem("Jus Mangga", 7000, 32, 150),
        MenuItem("Jus Jambu", 7000, 30, 130),
        MenuItem("Jus Wortel", 6000, 25, 80),
        MenuItem("Cimory", 8000, 32, 130),
        MenuItem("Teh Tarik", 8000, 35, 170),
        MenuItem("Es Coklat", 10000, 40, 200),
        MenuItem("Kopi Susu", 5000, 30, 130),
        MenuItem("Minuman Vitamin", 6000, 22, 50),
        MenuItem("Lemon Tea", 5000, 22, 90),
        MenuItem("Nescafe Sachet", 7000, 28, 80),
        MenuItem("Pop Ice", 5000, 32, 150),
        MenuItem("Ultra Milk", 8000, 32, 125),
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

        jelaskan_top_3_pilihan(menu_terpilih)

        tampilkan_hasil(menu_terpilih, total_harga, total_nilai_gizi, total_kalori, anggaran)

    except ValueError:
        print("Input tidak valid! Masukkan angka yang benar.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    main()
