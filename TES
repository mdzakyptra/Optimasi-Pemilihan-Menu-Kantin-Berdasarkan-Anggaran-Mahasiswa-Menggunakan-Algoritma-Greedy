from typing import List, Tuple

# Dataset menu: list of tuples (nama, harga, kalori, kategori)
# kategori hanya "makanan" atau "minuman" sehingga kita bisa batasi jumlahnya
MenuItem = Tuple[str, int, int, str]
menu_items: List[MenuItem] = [
    # Makanan
    ("Nasi Goreng", 15000, 550, "makanan"),
    ("Mie Goreng", 12000, 400, "makanan"),
    ("Ayam Goreng + Nasi", 15000, 450, "makanan"),
    ("Pecel Lele + Nasi", 12000, 300, "makanan"),
    ("Soto Ayam + Nasi", 10000, 300, "makanan"),
    ("Sate Ayam (10 tusuk + lontong)", 20000, 500, "makanan"),
    ("Gado-Gado (dengan lontong)", 10000, 300, "makanan"),
    ("Nasi Padang (Rendang)", 20000, 600, "makanan"),
    ("Nasi Uduk + Tahu Tempe", 8000, 400, "makanan"),
    ("Mie Ayam", 12000, 450, "makanan"),
    ("Bakso (dengan mi)", 10000, 300, "makanan"),
    ("Nasi Pecel", 8000, 250, "makanan"),
    ("Ayam Bakar + Nasi", 15000, 400, "makanan"),
    ("Nasi Goreng Spesial", 20000, 700, "makanan"),
    ("Spaghetti Bolognaise", 15000, 350, "makanan"),
    ("Burger", 12000, 300, "makanan"),
    ("Nasi Campur", 10000, 500, "makanan"),
    ("Sup Ayam + Nasi", 8000, 250, "makanan"),
    ("Kwetiau Goreng", 12000, 400, "makanan"),
    ("Capcay + Nasi", 12000, 300, "makanan"),
    # Minuman
    ("Teh Manis (hangat/dingin)", 3000, 50, "minuman"),
    ("Kopi Tubruk (gula)", 5000, 30, "minuman"),
    ("Jus Alpukat", 8000, 200, "minuman"),
    ("Jus Jeruk", 5000, 80, "minuman"),
    ("Minuman Bersoda (330 ml)", 7000, 140, "minuman"),
    ("Air Mineral (600 ml)", 3000, 0, "minuman"),
    ("Susu (gelas)", 5000, 120, "minuman"),
    ("Teh Tawar (hangat)", 2000, 0, "minuman"),
    ("Jus Mangga", 7000, 150, "minuman"),
    ("Jus Jambu", 7000, 100, "minuman"),
    ("Jus Wortel", 6000, 50, "minuman"),
    ("Susu Kedelai", 5000, 80, "minuman"),
    ("Teh Tarik (es)", 10000, 150, "minuman"),
    ("Es Coklat (cokelat susu)", 10000, 180, "minuman"),
    ("Kopi Susu (es)", 8000, 100, "minuman"),
    ("Minuman Energi (botol)", 6000, 110, "minuman"),
    ("Lemon Tea (dingin)", 5000, 60, "minuman"),
    ("Es Cendol", 7000, 150, "minuman"),
    ("Es Buah", 10000, 120, "minuman"),
    ("Soda Gembira", 8000, 160, "minuman"),
]


def greedy_recommendation(
    budget: int,
    max_makanan: int | None = None,
    max_minuman: int | None = None,
    items: List[MenuItem] | None = None,
) -> Tuple[List[MenuItem], int, int]:
    """
    Pilih menu dengan rasio kalori/harga terbaik hingga budget habis
    sambil mempertahankan jumlah makanan dan minuman yang diinginkan.
    """
    items = items or menu_items
    ranked_items = sorted(items, key=lambda x: x[2] / x[1], reverse=True)
    selected: List[MenuItem] = []
    total_price = 0
    total_cal = 0
    makanan_dipilih = 0
    minuman_dipilih = 0

    for (name, price, cal, kategori) in ranked_items:
        if kategori == "makanan" and max_makanan is not None and makanan_dipilih >= max_makanan:
            continue
        if kategori == "minuman" and max_minuman is not None and minuman_dipilih >= max_minuman:
            continue

        if total_price + price <= budget:
            selected.append((name, price, cal, kategori))
            total_price += price
            total_cal += cal
            if kategori == "makanan":
                makanan_dipilih += 1
            else:
                minuman_dipilih += 1

        if (
            (max_makanan is None or makanan_dipilih >= max_makanan)
            and (max_minuman is None or minuman_dipilih >= max_minuman)
        ):
            # target jumlah terpenuhi, tidak perlu lanjut
            break

    return selected, total_price, total_cal


def prompt_budget() -> int:
    """Minta input budget dan validasi agar tidak crash saat input salah."""
    while True:
        raw_value = input("Masukkan budget Anda (Rp): ")
        try:
            budget = int(raw_value)
            if budget <= 0:
                print("Budget harus lebih besar dari 0. Coba lagi.\n")
                continue
            return budget
        except ValueError:
            print("Input harus berupa angka. Silakan masukkan kembali.\n")


def print_report(
    selected_items: List[MenuItem],
    total_price: int,
    total_cal: int,
    target_makanan: int | None,
    target_minuman: int | None,
) -> None:
    """Cetak ringkasan rekomendasi dalam format yang rapi."""
    print("\nRekomendasi menu terbaik:")
    if not selected_items:
        print("- Tidak ada menu yang dapat dipilih untuk budget tersebut.")
    food_count = 0
    drink_count = 0
    for (name, price, cal, kategori) in selected_items:
        print(f"- {name:<20} | Rp{price:>6} | {cal} kkal | {kategori}")
        if kategori == "makanan":
            food_count += 1
        else:
            drink_count += 1
    print("-" * 45)
    print(f"Total Harga = Rp{total_price}")
    print(f"Total Kalori = {total_cal} kkal")
    if target_makanan is not None:
        print(f"Makanan dipilih: {food_count}/{target_makanan}")
    if target_minuman is not None:
        print(f"Minuman dipilih: {drink_count}/{target_minuman}")


def prompt_count(label: str, allow_zero: bool = True) -> int | None:
    """Minta jumlah item; user boleh mengosongkan (enter) untuk tanpa batas."""
    while True:
        raw = input(label).strip()
        if raw == "":
            return None
        try:
            value = int(raw)
            if value < 0 or (not allow_zero and value == 0):
                print("Jumlah tidak boleh negatif. Coba lagi.\n")
                continue
            return value
        except ValueError:
            print("Input harus berupa angka atau dikosongkan.\n")


def main() -> None:
    budget = prompt_budget()
    max_food = prompt_count(
        "Masukkan jumlah makanan yang ingin dipilih (Enter jika bebas): "
    )
    max_drink = prompt_count(
        "Masukkan jumlah minuman yang ingin dipilih (Enter jika bebas): "
    )
    selected_items, total_price, total_cal = greedy_recommendation(
        budget, max_food, max_drink
    )
    print_report(selected_items, total_price, total_cal, max_food, max_drink)


if __name__ == "__main__":
    main()
