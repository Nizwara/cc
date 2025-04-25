import random
from datetime import datetime
import os  # Import modul os untuk clear screen
import time  # Import modul time untuk animasi loading
import requests  # Import modul requests untuk HTTP request

# Warna ANSI escape sequences
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
MAGENTA = "\033[1;35m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"  # No Color (reset)

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# URL API BIN Checker
API_URL = "https://bin.zerostore.web.id"

# Fungsi untuk cek BIN dengan API
def check_bin(bin_number):
    try:
        response = requests.post(API_URL, json={"bin": bin_number})
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                return f"❌ BIN {bin_number} tidak valid."
            
            return f"""
✅ BIN: {bin_number}
🏦 Bank: {data.get("bank", "Unknown")}
💳 Brand: {data.get("scheme", "Unknown")}
📌 Tipe: {data.get("type", "Unknown")}
🌎 Negara: {data.get("country_name", "Unknown")} {data.get("country_emoji", "")}
"""
        else:
            return f"❌ Error API untuk BIN {bin_number}"
    except Exception as e:
        return f"⚠️ Gagal mengecek BIN {bin_number}: {e}"

# Fungsi untuk animasi loading sederhana
def show_loading():
    print(f"{YELLOW}Memuat...", end="", flush=True)
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.1)
    print(NC)

# Fungsi untuk validasi Luhn
def luhn_check(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    
    return checksum % 10 == 0

# Fungsi untuk menghasilkan tanggal kedaluwarsa (format MM|YYYY)
def generate_expiry():
    month = random.randint(1, 12)
    year = random.randint(2025, 2039)  # Tahun dari 2025 hingga 2039
    return f"{month:02d}|{year:04d}"

# Fungsi untuk menghasilkan CVV
def generate_cvv():
    return f"{random.randint(100, 999):03d}"

# Fungsi untuk menghasilkan BIN acak (6-14 digit)
def generate_bin():
    length = random.randint(6, 14)
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# Fungsi untuk menghasilkan nomor kartu
def generate_card_number(bin_code):
    card_number = [int(digit) for digit in bin_code]
    while len(card_number) < 15:
        card_number.append(random.randint(0, 9))

    checksum_digit = 0
    for i in range(10):
        if luhn_check(int(''.join(map(str, card_number + [i])))):
            checksum_digit = i
            break
    
    card_number.append(checksum_digit)
    return ''.join(map(str, card_number))

# Fungsi untuk menampilkan header yang sesuai untuk layar ponsel
def display_header():
    print(f"{CYAN}╔═══════════════════════════════════════╗{NC}")
    print(f"{CYAN}║{NC}{GREEN}          █▀▀▀▀▀▀▀▀▀▀▀▀▀█              {NC}{CYAN}║{NC}")
    print(f"{CYAN}║{NC}{GREEN}          │ KILLER TOOLS│              {NC}{CYAN}║{NC}")
    print(f"{CYAN}║{NC}{GREEN}          █▄▄▄▄▄▄▄▄▄▄▄▄▄█              {NC}{CYAN}║{NC}")
    print(f"{CYAN}╠═══════════════════════════════════════╣{NC}")
    print(f"{CYAN}║{NC} {MAGENTA}📅 {datetime.now().strftime('%A, %d %B %Y')}           {NC}  {CYAN}║{NC}")
    print(f"{CYAN}║{NC} {MAGENTA}⏰ {datetime.now().strftime('%H:%M:%S')}            {NC}               {CYAN}║{NC}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{NC}")

# Fungsi untuk menampilkan hasil generate kartu
def display_results(cards):
    print(f"{CYAN}╔═══════════════════════════════════════╗{NC}")
    print(f"{CYAN}║{NC}{YELLOW}   HASIL GENERATE KARTU KREDIT         {NC}{CYAN}║{NC}")
    print(f"{CYAN}╠═══════════════════════════════════════╣{NC}")
    print(f"{CYAN}║{NC} No. Kartu       Expiry    CVV  Status {NC}{CYAN}║{NC}")
    print(f"{CYAN}╠═══════════════════════════════════════╣{NC}")
    for card in cards:
        # Pisahkan string kartu dengan benar menggunakan "|"
        parts = card.split("|")
        if len(parts) == 4:
            card_number, month, year, cvv = parts
            expiry = f"{month}|{year}"  # Gabungkan bulan dan tahun
            # Cek validitas kartu menggunakan Luhn Check
            if luhn_check(card_number):
                status = f"{GREEN}Hidup{NC}"
            else:
                status = f"{RED}Mati{NC}"
            # Format output agar rapi
            print(f"{CYAN}║{NC} {card_number.ljust(16)}  {expiry.ljust(7)}  {cvv.ljust(3)}  {status.ljust(6)} {NC}{CYAN}║{NC}")
        else:
            print(f"{CYAN}║{NC} {RED}Format kartu tidak valid!{NC} {CYAN}║{NC}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{NC}")

# Fungsi untuk menampilkan menu
def show_menu():
    print(f"{CYAN}╔═══════════════════════════════════════╗{NC}")
    print(f"{CYAN}║{NC}{YELLOW}         K I L L E R  T O O L S        {NC}{CYAN}║{NC}")
    print(f"{CYAN}╠═══════════════════════════════════════╣{NC}")
    print(f"{CYAN}║{NC} {GREEN}1. Generate Kartu dengan BIN          {NC}{CYAN}║{NC}")
    print(f"{CYAN}║{NC} {GREEN}2. Generate dengan BIN,Exp,CVV        {NC}{CYAN}║{NC}")
    print(f"{CYAN}║{NC} {GREEN}3. Cek BIN                            {NC}{CYAN}║{NC}")
    print(f"{CYAN}║{NC} {RED}4. Keluar                             {NC}{CYAN}║{NC}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{NC}")

# Fungsi untuk menampilkan pesan "Tekan Enter untuk kembali"
def press_enter_to_continue():
    input(f"{CYAN}\nTekan Enter untuk kembali ke menu...{NC}")
    clear_screen()  # Membersihkan layar setelah menekan Enter
    display_header()  # Menampilkan header setelah clear screen

# Fungsi utama
def main():
    clear_screen()  # Membersihkan layar hanya saat program dimulai
    display_header()  # Tampilkan header saat program dimulai
    while True:
        show_menu()
        choice = input("Pilih opsi (1/2/3/4): ")

        if choice == "1":
            show_loading()  # Menampilkan animasi loading
            # Generate dengan BIN (expiry dan CVV di-generate otomatis)
            bin_code = input("Masukkan BIN (6-14 digit): ").strip()
            if len(bin_code) < 6 or len(bin_code) > 14 or not bin_code.isdigit():
                print(f"{RED}BIN harus 6-14 digit angka!{NC}\n")
                press_enter_to_continue()
                continue

            total = int(input("Masukkan jumlah kartu yang ingin digenerate: "))
            cards = []
            for _ in range(total):
                card_number = generate_card_number(bin_code)
                expiry = generate_expiry()  # Tanggal kedaluwarsa di-generate otomatis
                cvv = generate_cvv()  # CVV di-generate otomatis
                cards.append(f"{card_number}|{expiry}|{cvv}")
            clear_screen()
            display_header()
            display_results(cards)  # Menampilkan hasil generate
            press_enter_to_continue()  # Tunggu pengguna menekan Enter

        elif choice == "2":
            show_loading()  # Menampilkan animasi loading
            # Generate dengan BIN, Expiry, dan CVV
            bin_code = input("Masukkan BIN (6-14 digit): ").strip()
            if len(bin_code) < 6 or len(bin_code) > 14 or not bin_code.isdigit():
                print(f"{RED}BIN harus 6-14 digit angka!{NC}\n")
                press_enter_to_continue()
                continue

            expiry = input("Masukkan Expiry Date (MM|YYYY): ").strip()
            if len(expiry) != 7 or expiry[2] != "|" or not expiry.replace("|", "").isdigit():
                print(f"{RED}Format Expiry Date harus MM|YYYY!{NC}\n")
                press_enter_to_continue()
                continue

            cvv = input("Masukkan CVV (3 digit): ").strip()
            if len(cvv) != 3 or not cvv.isdigit():
                print(f"{RED}CVV harus 3 digit angka!{NC}\n")
                press_enter_to_continue()
                continue

            total = int(input("Masukkan jumlah kartu yang ingin digenerate: "))
            cards = []
            for _ in range(total):
                card_number = generate_card_number(bin_code)
                cards.append(f"{card_number}|{expiry}|{cvv}")
            clear_screen()
            display_header()
            display_results(cards)  # Menampilkan hasil generate
            press_enter_to_continue()  # Tunggu pengguna menekan Enter
        
        elif choice == "3":
            bin_input = input("Masukkan BIN untuk dicek: ").strip()
            result = check_bin(bin_input)
            print(result)
            press_enter_to_continue()

        elif choice == "4":
            # Keluar dari program
            print(f"{RED}Terima kasih! Program selesai.{NC}")
            break

        else:
            print(f"{RED}Pilihan tidak valid. Silakan pilih 1, 2, 3, atau 4.{NC}\n")
            press_enter_to_continue()

if __name__ == "__main__":
    main()
