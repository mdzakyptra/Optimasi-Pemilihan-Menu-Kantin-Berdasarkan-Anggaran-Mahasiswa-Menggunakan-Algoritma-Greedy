from typing import Dict, List, Tuple

# Dataset menu: list of tuples (nama, harga, kalori, kategori)
# kategori hanya "makanan" atau "minuman" sehingga kita bisa batasi jumlahnya
MenuItem = Tuple[str, int, int, str]
menu_items: List[MenuItem] = [
    ("Nasi Goreng", 15000, 330, "makanan"),
    ("Mie Goreng", 12000, 350, "makanan"),
    ("Ayam Goreng + Nasi", 15000, 450, "makanan"),
    ("Nasi Katsu", 12000, 480, "makanan"),
    ("Soto Ayam + Nasi", 10000, 350, "makanan"),
    ("Soto Ayam", 8000, 150, "makanan"),
    ("Gado-Gado", 10000, 490, "makanan"),
    ("Nasi Katsu Asam Manis", 15000, 520, "makanan"),
    ("Nasi Katsu Black Pepper", 15000, 510, "makanan"),
    ("Mie Ayam", 12000, 400, "makanan"),
    ("Bakso", 10000, 325, "makanan"),
    ("Nasi Pecel", 10000, 500, "makanan"),
    ("Nasi Sayur", 15000, 380, "makanan"),
    ("Nasi Goreng Spesial", 20000, 450, "makanan"),
    ("Nasi Pecel Telor", 13000, 580, "makanan"),
    ("Batagor (isi 10)", 10000, 580, "makanan"),
    ("Nasi Campur", 10000, 680, "makanan"),
    ("Sup Ayam + Nasi", 8000, 280, "makanan"),
    ("Tempe Goreng", 1000, 80, "makanan"),
    ("Tempura", 1000, 90, "makanan"),
    ("Teh Manis (hangat/dingin)", 3000, 90, "minuman"),
    ("Kopi Tubruk (gula)", 5000, 85, "minuman"),
    ("Jus Mangga", 5000, 150, "minuman"),
    ("Jus Jeruk", 5000, 110, "minuman"),
    ("Coca Cola/Fanta/Sprite", 7000, 140, "minuman"),
    ("Air Mineral (600 ml)", 3000, 0, "minuman"),
    ("Susu", 5000, 150, "minuman"),
    ("Teh Tawar", 2000, 2, "minuman"),
    ("Jus Mangga", 7000, 150, "minuman"),
    ("Jus Jambu", 7000, 130, "minuman"),
    ("Jus Wortel", 6000, 80, "minuman"),
    ("Cimory", 8000, 130, "minuman"),
    ("Teh Tarik", 8000, 170, "minuman"),
    ("Es Coklat", 10000, 200, "minuman"),
    ("Kopi Susu", 5000, 130, "minuman"),
    ("Minuman Vitamin", 6000, 50, "minuman"),
    ("Lemon Tea", 5000, 90, "minuman"),
    ("Nescafe Sachet", 7000, 80, "minuman"),
    ("Pop Ice", 5000, 150, "minuman"),
    ("Ultra Milk", 8000, 125, "minuman"),
]


def greedy_recommendation(
    budget: int,
    max_makanan: int | None = None,
    max_minuman: int | None = None,
    items: List[MenuItem] | None = None,
) -> Tuple[List[MenuItem], int, int, List[Dict[str, str]]]:
    """
    Pilih menu secara greedy berdasarkan rasio kalori per rupiah (kkal/Rp)
    paling tinggi hingga anggaran & kuota terpenuhi.

    Inti pengambilan keputusan:
    1. Urutkan semua item dari rasio kkal/Rp tertinggi ke terendah.
    2. Ambil item pertama yang masih muat di anggaran dan belum melampaui kuota kategori.
    3. Catat alasan (rasio, sisa anggaran, kuota) agar proses bisa dijelaskan di output.
    """
    items = items or menu_items
    ranked_items = sorted(items, key=lambda x: x[2] / x[1], reverse=True)
    selected: List[MenuItem] = []
    total_price = 0
    total_cal = 0
    makanan_dipilih = 0
    minuman_dipilih = 0
    steps: List[Dict[str, str]] = []

    for (name, price, cal, kategori) in ranked_items:
        rasio = cal / price
        if kategori == "makanan" and max_makanan is not None and makanan_dipilih >= max_makanan:
            steps.append(
                {
                    "item": name,
                    "aksi": "lewati",
                    "alasan": "Kuota makanan terpenuhi",
                    "rasio": f"{rasio:.4f}",
                }
            )
            continue
        if kategori == "minuman" and max_minuman is not None and minuman_dipilih >= max_minuman:
            steps.append(
                {
                    "item": name,
                    "aksi": "lewati",
                    "alasan": "Kuota minuman terpenuhi",
                    "rasio": f"{rasio:.4f}",
                }
            )
            continue

        if total_price + price <= budget:
            selected.append((name, price, cal, kategori))
            total_price += price
            total_cal += cal
            if kategori == "makanan":
                makanan_dipilih += 1
            else:
                minuman_dipilih += 1
            steps.append(
                {
                    "item": name,
                    "aksi": "pilih",
                    "alasan": "Rasio tinggi & masih dalam anggaran",
                    "rasio": f"{rasio:.4f}",
                    "sisa_anggaran": f"{budget - total_price}",
                }
            )
        else:
            steps.append(
                {
                    "item": name,
                    "aksi": "lewati",
                    "alasan": "Harga melebihi sisa anggaran",
                    "rasio": f"{rasio:.4f}",
                }
            )
            continue

        if (
            (max_makanan is None or makanan_dipilih >= max_makanan)
            and (max_minuman is None or minuman_dipilih >= max_minuman)
        ):
            # target jumlah terpenuhi, tidak perlu lanjut
            break

    return selected, total_price, total_cal, steps


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


def explain_greedy_steps(steps: List[Dict[str, str]]) -> None:
    """Menjelaskan bagaimana algoritma greedy membuat keputusan."""
    print("\nPenjelasan Proses Greedy:")
    if not steps:
        print("- Tidak ada langkah yang dicatat.")
        return
    for idx, step in enumerate(steps, 1):
        base = f"{idx:02d}. {step['item']} | Rasio {step['rasio']} kkal/Rp -> {step['aksi'].upper()}"
        reason = step.get("alasan", "-")
        sisa = step.get("sisa_anggaran")
        if sisa is not None:
            print(f"{base} (Sisa anggaran: Rp{sisa}) | {reason}")
        else:
            print(f"{base} | {reason}")


def validate_solution(
    selected_items: List[MenuItem],
    total_price: int,
    budget: int,
    target_makanan: int | None,
    target_minuman: int | None,
) -> None:
    """Validasi sederhana bahwa solusi memenuhi anggaran & kuota."""
    food_count = sum(1 for _, _, _, cat in selected_items if cat == "makanan")
    drink_count = sum(1 for _, _, _, cat in selected_items if cat == "minuman")
    issues: List[str] = []
    if total_price > budget:
        issues.append("Total harga melebihi anggaran.")
    if target_makanan is not None and food_count > target_makanan:
        issues.append("Jumlah makanan melebihi kuota.")
    if target_minuman is not None and drink_count > target_minuman:
        issues.append("Jumlah minuman melebihi kuota.")

    print("\nValidasi Solusi:")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        utilisation = (total_price / budget * 100) if budget else 0
        print("- Semua kendala terpenuhi.")
        print(f"- Anggaran terpakai {utilisation:.2f}%")
        print(f"- Makanan dipilih {food_count} item, Minuman dipilih {drink_count} item")


def main() -> None:
    budget = prompt_budget()
    max_food = prompt_count(
        "Masukkan jumlah makanan yang ingin dipilih (Enter jika bebas): "
    )
    max_drink = prompt_count(
        "Masukkan jumlah minuman yang ingin dipilih (Enter jika bebas): "
    )
    selected_items, total_price, total_cal, steps = greedy_recommendation(
        budget, max_food, max_drink
    )
    print_report(selected_items, total_price, total_cal, max_food, max_drink)
    explain_greedy_steps(steps)
    validate_solution(selected_items, total_price, budget, max_food, max_drink)


if __name__ == "__main__":
    main()
