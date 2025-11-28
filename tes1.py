from typing import List, Tuple

# Dataset menu: list of tuples (nama, harga, kalori)
MenuItem = Tuple[str, int, int]
menu_items: List[MenuItem] = [
    ("Nasi Goreng", 15000, 550),
    ("Mie Goreng", 12000, 400),
    ("Ayam Goreng + Nasi", 15000, 450),
    ("Pecel Lele + Nasi", 12000, 300),
    # ... (data lain hingga total 40 item seperti Tabel 1 & 2) ...
    ("Es Buah", 10000, 120),
    ("Soda Gembira", 8000, 160),
]


def greedy_recommendation(budget: int, items: List[MenuItem] | None = None) -> Tuple[List[MenuItem], int, int]:
    """Pilih menu dengan rasio kalori/harga terbaik hingga budget habis."""
    items = items or menu_items
    ranked_items = sorted(items, key=lambda x: x[2] / x[1], reverse=True)
    selected: List[MenuItem] = []
    total_price = 0
    total_cal = 0

    for (name, price, cal) in ranked_items:
        if total_price + price <= budget:
            selected.append((name, price, cal))
            total_price += price
            total_cal += cal

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


def print_report(selected_items: List[MenuItem], total_price: int, total_cal: int) -> None:
    """Cetak ringkasan rekomendasi dalam format yang rapi."""
    print("\nRekomendasi menu terbaik:")
    if not selected_items:
        print("- Tidak ada menu yang dapat dipilih untuk budget tersebut.")
    for (name, price, cal) in selected_items:
        print(f"- {name:<20} | Rp{price:>6} | {cal} kkal")
    print("-" * 45)
    print(f"Total Harga = Rp{total_price}")
    print(f"Total Kalori = {total_cal} kkal")


def main() -> None:
    budget = prompt_budget()
    selected_items, total_price, total_cal = greedy_recommendation(budget)
    print_report(selected_items, total_price, total_cal)


if __name__ == "__main__":
    main()
