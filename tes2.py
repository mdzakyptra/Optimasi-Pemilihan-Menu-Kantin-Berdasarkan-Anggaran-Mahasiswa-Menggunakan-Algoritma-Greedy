
import sys
import os


class MenuItem:

    def __init__(self, nama, harga, nilai_gizi, kalori=0, kategori="makanan"):
        self.nama = nama
        self.harga = harga
        self.nilai_gizi = nilai_gizi
        self.kalori = kalori
        self.kategori = kategori
        self.rasio = kalori / harga

    def __repr__(self):
        return f"{self.nama} - Rp{self.harga:,}"


def algoritma_greedy_menu(daftar_menu, anggaran):
    # Pisahkan makanan dan minuman
    makanan = [m for m in daftar_menu if m.kategori == "makanan"]
    minuman = [m for m in daftar_menu if m.kategori == "minuman"]

    menu_terpilih = []
    total_harga = 0
    total_nilai_gizi = 0
    total_kalori = 0

    print("\n" + "="*70)
    print("PROSES ALGORITMA GREEDY (Berdasarkan Kalori Maksimum)")
    print("="*70)
    print(f"Anggaran tersedia: Rp{anggaran:,}")
    print()

    # Fase 0: Pastikan ada minimal 1 minuman (pilih minuman termurah dulu)
    minuman_termurah = sorted(minuman, key=lambda x: x.harga)
    if minuman_termurah and total_harga + minuman_termurah[0].harga <= anggaran:
        menu = minuman_termurah[0]
        menu_terpilih.append(menu)
        total_harga += menu.harga
        total_nilai_gizi += menu.nilai_gizi
        total_kalori += menu.kalori

        print(f"✓ Memilih minuman wajib: {menu.nama}")
        print(f"  Harga: Rp{menu.harga:,} | Kalori: {menu.kalori} kkal | Rasio: {menu.rasio:.4f} kkal/Rp")
        print(f"  Sisa anggaran: Rp{anggaran - total_harga:,}\n")

    # Fase 1: Pilih menu dengan kalori tertinggi
    menu_terurut = sorted(daftar_menu, key=lambda x: x.kalori, reverse=True)

    for menu in menu_terurut:
        if total_harga + menu.harga <= anggaran:
            menu_terpilih.append(menu)
            total_harga += menu.harga
            total_nilai_gizi += menu.nilai_gizi
            total_kalori += menu.kalori

            print(f"✓ Memilih: {menu.nama}")
            print(f"  Harga: Rp{menu.harga:,} | Kalori: {menu.kalori} kkal | Rasio: {menu.rasio:.4f} kkal/Rp")
            print(f"  Sisa anggaran: Rp{anggaran - total_harga:,}\n")

    # Fase 2: Maksimalkan penggunaan anggaran dengan menu termurah
    sisa_anggaran = anggaran - total_harga
    if sisa_anggaran > 0:
        print(f"\n{'='*70}")
        print(f"MEMAKSIMALKAN ANGGARAN (Sisa: Rp{sisa_anggaran:,})")
        print(f"{'='*70}\n")

        # Urutkan menu berdasarkan harga termurah
        menu_termurah = sorted(daftar_menu, key=lambda x: x.harga)

        while sisa_anggaran > 0:
            menu_ditambahkan = False
            for menu in menu_termurah:
                if menu.harga <= sisa_anggaran:
                    menu_terpilih.append(menu)
                    total_harga += menu.harga
                    total_nilai_gizi += menu.nilai_gizi
                    total_kalori += menu.kalori
                    sisa_anggaran -= menu.harga

                    print(f"✓ Menambahkan: {menu.nama}")
                    print(f"  Harga: Rp{menu.harga:,} | Kalori: {menu.kalori} kkal")
                    print(f"  Sisa anggaran: Rp{sisa_anggaran:,}\n")

                    menu_ditambahkan = True
                    break

            # Jika tidak ada menu yang bisa ditambahkan, keluar dari loop
            if not menu_ditambahkan:
                break

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

    if len(menu_terpilih) > 3:
        print(f"\n   ... dan {len(menu_terpilih) - 3} menu lainnya")

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
        MenuItem("Nasi Goreng", 15000, 70, 330, "makanan"),
        MenuItem("Mie Goreng", 12000, 65, 350, "makanan"),
        MenuItem("Ayam Goreng + Nasi", 15000, 80, 450, "makanan"),
        MenuItem("Nasi Katsu", 12000, 75, 480, "makanan"),
        MenuItem("Soto Ayam + Nasi", 10000, 65, 350, "makanan"),
        MenuItem("Soto Ayam", 8000, 55, 150, "makanan"),
        MenuItem("Gado-Gado", 10000, 72, 490, "makanan"),
        MenuItem("Nasi Katsu Asam Manis", 15000, 82, 520, "makanan"),
        MenuItem("Nasi Katsu Black Pepper", 15000, 81, 510, "makanan"),
        MenuItem("Mie Ayam", 12000, 68, 400, "makanan"),
        MenuItem("Bakso", 10000, 62, 325, "makanan"),
        MenuItem("Nasi Pecel", 10000, 75, 500, "makanan"),
        MenuItem("Nasi Sayur", 15000, 70, 380, "makanan"),
        MenuItem("Nasi Goreng Spesial", 20000, 78, 450, "makanan"),
        MenuItem("Nasi Pecel Telor", 13000, 82, 580, "makanan"),
        MenuItem("Batagor (isi 10)", 10000, 78, 580, "makanan"),
        MenuItem("Nasi Campur", 10000, 88, 680, "makanan"),
        MenuItem("Sup Ayam + Nasi", 8000, 58, 280, "makanan"),
        MenuItem("Tempe Goreng", 1000, 32, 80, "makanan"),
        MenuItem("Tempura", 1000, 35, 90, "makanan"),
        MenuItem("Teh Manis (hangat/dingin)", 3000, 20, 90, "minuman"),
        MenuItem("Kopi Tubruk (gula)", 5000, 22, 85, "minuman"),
        MenuItem("Jus Mangga", 5000, 32, 150, "minuman"),
        MenuItem("Jus Jeruk", 5000, 28, 110, "minuman"),
        MenuItem("Coca Cola/Fanta/Sprite", 7000, 30, 140, "minuman"),
        MenuItem("Air Mineral (600 ml)", 3000, 10, 0, "minuman"),
        MenuItem("Susu", 5000, 32, 150, "minuman"),
        MenuItem("Teh Tawar", 2000, 8, 2, "minuman"),
        MenuItem("Jus Mangga", 7000, 32, 150, "minuman"),
        MenuItem("Jus Jambu", 7000, 30, 130, "minuman"),
        MenuItem("Jus Wortel", 6000, 25, 80, "minuman"),
        MenuItem("Cimory", 8000, 32, 130, "minuman"),
        MenuItem("Teh Tarik", 8000, 35, 170, "minuman"),
        MenuItem("Es Coklat", 10000, 40, 200, "minuman"),
        MenuItem("Kopi Susu", 5000, 30, 130, "minuman"),
        MenuItem("Minuman Vitamin", 6000, 22, 50, "minuman"),
        MenuItem("Lemon Tea", 5000, 22, 90, "minuman"),
        MenuItem("Nescafe Sachet", 7000, 28, 80, "minuman"),
        MenuItem("Pop Ice", 5000, 32, 150, "minuman"),
        MenuItem("Ultra Milk", 8000, 32, 125, "minuman"),
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

        menu_terpilih, total_harga, total_nilai_gizi, total_kalori = algoritma_greedy_menu(
            daftar_menu, anggaran
        )

        jelaskan_top_3_pilihan(menu_terpilih)

        tampilkan_hasil(menu_terpilih, total_harga, total_nilai_gizi, total_kalori, anggaran)

    except ValueError:
        print("Input tidak valid! Masukkan angka yang benar.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    main()
